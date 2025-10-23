import re
from typing import List, Tuple
from src.classes.Material import Material  # Import the Material class

def _parse_floats_tuple(s: str) -> Tuple[float, ...]:
    s = s.strip()
    s = s.lstrip('([').rstrip('])')
    parts = [p.strip() for p in re.split(r'[,\s]+', s) if p.strip() != '']
    try:
        return tuple(float(x) for x in parts)
    except ValueError as e:
        raise ValueError(f"Invalid float in tuple '{s}': {e}")

def _parse_bools_tuple_strict(s: str) -> Tuple[bool, ...]:
    """
    Parse a tuple of booleans where only '1' (true) and '0' (false) are allowed.
    Accepts formats like: (1,0,1,0) or 1 0 1 0
    """
    s = s.strip()
    s = s.lstrip('([').rstrip('])')
    parts = [p.strip() for p in re.split(r'[,\s]+', s) if p.strip() != '']
    if not parts:
        raise ValueError("Empty boolean tuple")
    result = []
    for p in parts:
        if p == '1':
            result.append(True)
        elif p == '0':
            result.append(False)
        else:
            raise ValueError(f"Boolean values must be '1' or '0' (found '{p}')")
    return tuple(result)

def _normalize_key(k: str) -> str:
    return k.strip().lower().replace('-', '_')

def parse_materials_from_string(text: str) -> List[Material]:
    """
    Parse materials from a string. Blocks start with lines like "Material 1:".
    Each following non-empty line in the block should be "key: value".
    Recognized keys (case-insensitive):
      name, sigma_tr (or sigma__tr), sigma_a, mu_0, sigma_f, s, bounds, bound_type
    bounds -> four floats (x0, x1, y0, y1)
    bound_type -> four booleans as 1 or 0 (x0, x1, y0, y1)
    """
    lines = text.splitlines()
    blocks = []
    current = None
    header_re = re.compile(r'^\s*Material\s*\d+\s*:\s*$', re.IGNORECASE)
    for ln in lines:
        if header_re.match(ln):
            if current is not None:
                blocks.append(current)
            current = []
            continue
        if current is not None:
            # strip comments after '#'
            line = ln.split('#', 1)[0].rstrip()
            if line.strip() == '' and (not current or all(l.strip() == '' for l in current)):
                # skip leading blank lines inside block
                continue
            current.append(line)
    if current:
        blocks.append(current)

    materials: List[Material] = []
    for blk in blocks:
        props = {}
        for ln in blk:
            if ':' not in ln:
                continue
            key, val = ln.split(':', 1)
            props[_normalize_key(key)] = val.strip()

        # required or defaulted values
        name = props.get('name', 'material')
        try:
            sigma__tr = float(props.get('sigma__tr') or props.get('sigma_tr') or 1.0)
            sigma_a = float(props.get('sigma_a', 0.0))
            mu_0 = float(props.get('mu_0', 0.0))
            sigma_f = float(props.get('sigma_f', 0.0))
            s = float(props.get('s', 0.0))
        except ValueError as e:
            raise ValueError(f"Invalid numeric value in material '{name}': {e}")

        bounds_raw = props.get('bounds', '(0.0, 1.0, 0.0, 1.0)')
        bounds = _parse_floats_tuple(bounds_raw)
        if len(bounds) != 4:
            raise ValueError(f"bounds must contain 4 floats for material '{name}': '{bounds_raw}'")

        bound_type_raw = props.get('bound_type', '(0, 0, 0, 0)')
        bound_type = _parse_bools_tuple_strict(bound_type_raw)
        if len(bound_type) != 4:
            raise ValueError(f"bound_type must contain 4 boolean entries (1/0) for material '{name}': '{bound_type_raw}'")

        mat = Material(
            name=name,
            sigma__tr=sigma__tr,
            sigma_a=sigma_a,
            mu_0=mu_0,
            sigma_f=sigma_f,
            s=s,
            bounds=(bounds[0], bounds[1], bounds[2], bounds[3]),
            bound_type=(bound_type[0], bound_type[1], bound_type[2], bound_type[3])
        )
        materials.append(mat)

    return materials

def parse_materials_from_file(path: str) -> List[Material]:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    return parse_materials_from_string(text)