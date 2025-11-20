import numpy as np
from src.classes.Mesh_constructor import Mesh_constructor
from src.classes.Material import Material

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
        s=0.0,
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
    ncells_x = 4  # 4 cells in x direction
    ncells_y = 3  # 3 cells in y direction
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
    D_cells, Sigma_a_cells = mesh.Dcells, mesh.Sigma_acells

    # Verify diffusion coefficients
    assert np.isclose(D_cells[0, 0], 1.0), f"Expected diffusion coefficient for Material1 to be 1.0, got {D_cells[0, 0]}"
    assert np.isclose(D_cells[-1, -1], 0.5), f"Expected diffusion coefficient for Material2 to be 0.5, got {D_cells[-1, -1]}"

    print("Test for small mesh with two materials passed!")

if __name__ == "__main__":
    test_small_mesh_with_two_materials()

    # Create a small mesh and materials for testing
    ncells_x = 4
    ncells_y = 3
    sigma_tr_material1 = 1 / (3 * 1.0)
    sigma_tr_material2 = 1 / (3 * 0.5)

    material1 = Material(
        name="Material1",
        sigma_s=sigma_tr_material1 - 0.01,
        sigma_a=0.01,
        mu_0=0.0,
        sigma_f=0.0,
        s=1,
        bounds=(2.0, 3.0),
        bound_type=(0, 0, 0, 0)
    )

    material2 = Material(
        name="Material2",
        sigma_s=sigma_tr_material2 - 0.02,
        sigma_a=0.02,
        mu_0=0.0,
        sigma_f=0.0,
        s=0.0,
        bounds=(2.0, 3.0),
        bound_type=(0, 0, 0, 0)
    )

    materials = [material1, material2]
    mesh = Mesh_constructor(ncells_x, ncells_y, materials)

    # Compute matrices
    mesh.compute_extrapolated_boundaries_y()
    mesh.compute_extrapolated_boundaries_x()
    mesh.compute_total_size()
    mesh.compute_cell_sizes()
    mesh.create_material_matrices()

    # Print matrices
    print("Diffusion Coefficient Matrix (D_cells):")
    print(mesh.Dcells)
    print("\nAbsorption Coefficient Matrix (Sigma_a_cells):")
    print(mesh.Sigma_acells)
    print("\nSource Term Matrix (source_cells):")
    print(mesh.source_cells)
    print("\nInterfaces:")
    print(mesh.interfaces_x)