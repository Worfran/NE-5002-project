import numpy as np
from src.classes.Mesh_constructor import Mesh_constructor
from src.classes.Material import Material
from src.classes.Matrix_constructor import Matrix_constructor

def test_small_mesh_with_two_materials():
    # Create materials with specific diffusion coefficients
    sigma_tr_material1 = 1 / (3 * 1.0)  # D = 1.0 -> sigma_tr = 1 / (3 * D)
    sigma_tr_material2 = 1 / (3 * 0.5)  # D = 0.5 -> sigma_tr = 1 / (3 * D)

    material1 = Material(
        name="Material1",
        sigma_s=sigma_tr_material1 - 0.01,  # sigma_s = sigma_tr - sigma_a (assuming sigma_a = 0.01)
        sigma_a=0.01,
        mu_0=0.0,
        sigma_f=0.0,
        s=1.0,
        bounds=(2.0, 3.0),  # Material 1 occupies 2x3 region
        bound_type=(0, 0, 0, 0)
    )

    material2 = Material(
        name="Material2",
        sigma_s=sigma_tr_material2 - 0.02,  # sigma_s = sigma_tr - sigma_a (assuming sigma_a = 0.02)
        sigma_a=0.02,
        mu_0=0.0,
        sigma_f=0.0,
        s=0.0,
        bounds=(2.0, 3.0),  # Material 2 occupies 2x3 region
        bound_type=(0, 0, 0, 0)
    )

    materials = [material1, material2]

    # Create Mesh_constructor instance
    ncells_x = 8  # 4 cells in x direction
    ncells_y = 8  # 3 cells in y direction
    mesh = Mesh_constructor(ncells_x, ncells_y, materials)

    # Compute extrapolated boundaries
    mesh.compute_extrapolated_boundaries_y()
    mesh.compute_extrapolated_boundaries_x()

    # Compute total size
    mesh.compute_total_size()

    # Compute cell sizes
    dx, dy = mesh.compute_cell_sizes()

    # Create material matrix
    material_matrix = mesh.create_material_matrices()
    D_cells, Sigma_a_cells, source_cells = mesh.Dcells, mesh.Sigma_acells, mesh.source_cells

    # Create Matrix_constructor instance
    matrix_constructor = Matrix_constructor(ncells_x, ncells_y, D_cells, Sigma_a_cells, source_cells, dx, dy, materials, mesh.interfaces_x)

    # Print the matrix A
    print("Matrix A:")
    print(matrix_constructor.A)

    print("Source term b:")
    print(matrix_constructor.b)

    # Write the matrix A to a txt file
    with open("matrix_A.txt", "w") as f:
        for row in matrix_constructor.A:
            f.write("\t".join(map(str, row)) + "\n")

if __name__ == "__main__":
    test_small_mesh_with_two_materials()
