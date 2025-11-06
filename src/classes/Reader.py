from src.classes.Material import Material
import re

class DocumentReader:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.materials = []

    def read_file(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.file_content = f.read()

    def parse_materials(self):
        material_blocks = self.file_content.split("Material")
        for block in material_blocks:
            if not block.strip():
                continue
            data = {}
            # use full parameter names to prevent substring collisions
            name = self._extract_parameter(block, 'name', default='unknown')
            sigma_s = float(self._extract_parameter(block, 'sigma_s', default=0.0))
            sigma_a = float(self._extract_parameter(block, 'sigma_a', default=0.0))
            mu_0 = float(self._extract_parameter(block, 'mu_0', default=0.0))
            sigma_f = float(self._extract_parameter(block, 'sigma_f', default=0.0))
            s = float(self._extract_parameter(block, 's', default=0.0))
            bounds = self._extract_tuple(block, 'bounds', expected_length=2)
            bound_type = self._extract_tuple(block, 'bound_type', expected_length=4, is_bool=True)

            material = Material(name, sigma_s, sigma_a, mu_0, sigma_f, s, bounds, bound_type)
            self.materials.append(material)

    def _extract_parameter(self, block: str, key: str, default=None):
        pattern = rf'(?<!\w){re.escape(key)}(?!\w)\s*:\s*(.+)$'
        match = re.search(pattern, block, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
        return default

    def _extract_tuple(self, block: str, key: str, expected_length: int, is_bool=False):
        pattern = rf'{key}\s*:\s*\((.+?)\)'
        match = re.search(pattern, block, re.IGNORECASE)
        if match:
            values = match.group(1).split(',')
            if len(values) != expected_length:
                raise ValueError(f"{key} must have {expected_length} values.")
            if is_bool:
                result = []
                for v in values:
                    v = v.strip()
                    if v == '1':
                        result.append(True)
                    elif v == '0':
                        result.append(False)
                    else:
                        raise ValueError(f"Boolean values must be '1' or '0' (found '{v}')")
                return tuple(result)
            return tuple(float(v.strip()) for v in values)
        raise ValueError(f"{key} not found or invalid.")

    def get_materials(self):
        return self.materials