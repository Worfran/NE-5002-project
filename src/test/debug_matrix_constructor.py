import numpy as np
from src.classes.Mesh_constructor import Mesh_constructor
from src.classes.Material import Material
from src.classes.Matrix_constructor import Matrix_constructor


def debug_cell(matrix_constructor, i, j):
    """
    Replays the same conditional logic as entries_aij for a single cell (i,j)
    and prints which branch is taken for LEFT, RIGHT, TOP, BOTTOM.
    This does NOT modify A or b.
    """
    n = matrix_constructor.ncells_x
    m = matrix_constructor.ncells_y
    interfaces_x = matrix_constructor.interfaces_x

    ic = n * (m - (i + 1)) + j

    has_left, has_right, has_top, has_bottom = matrix_constructor.check_neighbors(i, j)
    left_vac, right_vac, top_vac, bottom_vac = matrix_constructor.check_boundary(i, j)

    print(f"\n=== Cell (i={i}, j={j}), ic={ic} ===")
    print(f"  has_left={has_left}, has_right={has_right}, has_top={has_top}, has_bottom={has_bottom}")
    print(f"  left_vac={left_vac}, right_vac={right_vac}, top_vac={top_vac}, bottom_vac={bottom_vac}")
    print(f"  interfaces_x={interfaces_x}")

    # ----- LEFT -----
    if has_left and (j in interfaces_x):
        branch = "LEFT: interface"
    elif has_left:
        branch = "LEFT: interior"
    elif left_vac and not has_left:
        branch = "LEFT: vacuum BC"
    elif (not has_left) and (not left_vac):
        branch = "LEFT: reflective BC"
    else:
        branch = "LEFT: ***UNREACHED CASE***"
    print(" ", branch)

    # ----- RIGHT -----
    if has_right and (j in interfaces_x):
        branch = "RIGHT: interface"
    elif has_right:
        branch = "RIGHT: interior"
    elif right_vac and not has_right:
        branch = "RIGHT: vacuum BC"
    elif (not has_right) and (not right_vac):
        branch = "RIGHT: reflective BC"
    else:
        branch = "RIGHT: ***UNREACHED CASE***"
    print(" ", branch)

    # ----- TOP -----
    if has_top:
        branch = "TOP: interior"
    elif top_vac and not has_top:
        branch = "TOP: vacuum BC"
    elif (not has_top) and (not top_vac):
        branch = "TOP: reflective BC"
    else:
        branch = "TOP: ***UNREACHED CASE***"
    print(" ", branch)

    # ----- BOTTOM -----
    if has_bottom:
        branch = "BOTTOM: interior"
    elif bottom_vac and not has_bottom:
        branch = "BOTTOM: vacuum BC"
    elif (not has_bottom) and (not bottom_vac):
        branch = "BOTTOM: reflective BC"
    else:
        branch = "BOTTOM: ***UNREACHED CASE***"
    print(" ", branch)


def test_conditionals_two_materials():
    """
    Test the diffusion conditionals on a small mesh with three materials
    (same structure as your example), and print which branches are used.

    You can tweak ncells_x/ncells_y and bounds to hit different scenarios.
    """

    material1 = Material(
        name="Material1",
        sigma_s=0.99,
        sigma_a=0.01,
        mu_0=0.0,
        sigma_f=0.0,
        s=0.0,
        bounds=(7.0, 3.0),
        bound_type=(1, 1, 1, 1)  # vacuum on all sides
    )

    material2 = Material(
        name="Material2",
        sigma_s=0.8,
        sigma_a=0.2,
        mu_0=0.0,
        sigma_f=0.0,
        s=1.0,
        bounds=(6.0, 3.0),
        bound_type=(1, 1, 1, 1)
    )

    material3 = Material(
        name="Material3",
        sigma_s=0.99,
        sigma_a=0.01,
        mu_0=0.0,
        sigma_f=0.0,
        s=0.0,
        bounds=(7.0, 3.0),
        bound_type=(1, 1, 1, 1)
    )

    materials = [material1, material2, material3]

    # --- Mesh setup ---
    # Keep this small so the output is readable; adjust if needed.
    ncells_x = 25
    ncells_y = 25

    mesh = Mesh_constructor(ncells_x, ncells_y, materials)

    mesh.compute_extrapolated_boundaries_y()
    mesh.compute_extrapolated_boundaries_x()
    mesh.compute_total_size()
    dx, dy = mesh.compute_cell_sizes()

    # Build material matrices
    material_matrix = mesh.create_material_matrices()  
    D_cells, Sigma_a_cells, source_cells = mesh.Dcells, mesh.Sigma_acells, mesh.source_cells

    # Print matrices
    print("Diffusion Coefficient Matrix (D_cells):")
    print(mesh.Dcells)
    print("\nAbsorption Coefficient Matrix (Sigma_a_cells):")
    print(mesh.Sigma_acells)
    print("\nSource Term Matrix (source_cells):")
    print(mesh.source_cells)
    print("\nInterfaces:")
    print(mesh.interfaces_x)


    print("Interfaces at x-indices:", mesh.interfaces_x)

    # --- Matrix constructor ---
    mc = Matrix_constructor(
        ncells_x, ncells_y,
        D_cells, Sigma_a_cells, source_cells,
        dx, dy,
        materials,
        mesh.interfaces_x,
    )

    # --- Debug conditionals for selected cells ---

    mid_i = ncells_y // 2  # some interior row

    # Check:
    #   - left boundary j=0
    #   - just right of boundary j=1
    #   - each interface column
    #   - last two columns
    cols_to_check = [0, 1] + list(mesh.interfaces_x) + [ncells_x - 2, ncells_x - 1]
    # Remove duplicates and keep in-range
    cols_to_check = sorted({j for j in cols_to_check if 0 <= j < ncells_x})

    print("\n--- Debug along middle row (i = mid_i) ---")
    for j in cols_to_check:
        debug_cell(mc, mid_i, j)

    # Also check corners
    print("\n--- Debug corners ---")
    debug_cell(mc, 0, 0)
    debug_cell(mc, 0, ncells_x - 1)
    debug_cell(mc, ncells_y - 1, 0)
    debug_cell(mc, ncells_y - 1, ncells_x - 1)
    np.savetxt("debug_matrix_A.txt", mc.A)

if __name__ == "__main__":
    test_conditionals_two_materials()
