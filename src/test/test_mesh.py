import numpy as np
from src.classes.Mesh_constructor import Mesh_constructor
from src.classes.Material import Material

def test_mesh_constructor_with_test_1():
    # Create materials based on test_1.txt
    material1 = Material(
        name="Water",
        sigma_s=0.21,
        sigma_a=0.01,
        mu_0=0.0,
        sigma_f=0.0,
        s=1.0,
        bounds=(10.0, 10.0),
        bound_type=(0, 0, 0, 0)
    )

    material2 = Material(
        name="Fuel",
        sigma_s=0.5,
        sigma_a=0.02,
        mu_0=0.1,
        sigma_f=0.05,
        s=0.0,
        bounds=(20.0, 10.0),
        bound_type=(0, 0, 0, 0)
    )

    materials = [material1, material2]

    # Create Mesh_constructor instance
    ncells_x = 30
    ncells_y = 10
    mesh = Mesh_constructor(ncells_x, ncells_y, materials)

    # Compute extrapolated boundaries
    mesh.compute_extrapolated_boundaries_y()
    mesh.compute_extrapolated_boundaries_x()

    # Verify extrapolated boundaries
    assert mesh.max_extrapolated_distance_top == 0, "Expected max extrapolated distance top to be 0"
    assert mesh.max_extrapolated_distance_bottom == 0, "Expected max extrapolated distance bottom to be 0"
    assert mesh.extrapolated_distances_left == 0, "Expected extrapolated distances left to be 0"
    assert mesh.extrapolated_distances_right == 0, "Expected extrapolated distances right to be 0"

    # Compute total size
    mesh.compute_total_size()
    assert mesh.total_width == 30.0, f"Expected total width to be 30.0, got {mesh.total_width}"
    assert mesh.total_height == 10.0, f"Expected total height to be 10.0, got {mesh.total_height}"

    # Compute cell sizes
    dx, dy = mesh.compute_cell_sizes()
    assert dx == 1.0, f"Expected dx to be 1.0, got {dx}"
    assert dy == 1.0, f"Expected dy to be 1.0, got {dy}"

    # Create material matrix
    material_matrix = mesh.create_material_matrices()
    D_cells, Sigma_a_cells = mesh.Dcells, mesh.Sigma_acells
    assert D_cells.shape[0] == ncells_y, f"Expected material matrix to have {ncells_y} rows"
    assert D_cells.shape[1] == ncells_x, f"Expected material matrix to have {ncells_x} columns"
    assert Sigma_a_cells.shape[0] == ncells_y, f"Expected material matrix to have {ncells_y} rows"
    assert Sigma_a_cells.shape[1] == ncells_x, f"Expected material matrix to have {ncells_x} columns"

    print("Test for Mesh_constructor with test_1.txt passed!")

def test_mesh_constructor_with_reflecting_boundaries():
    # Create materials with reflecting boundaries for bottom and left, vacuum for top and right
    material1 = Material(
        name="Water",
        sigma_s=0.21,
        sigma_a=0.01,
        mu_0=0.0,
        sigma_f=0.0,
        s=1.0,
        bounds=(10.0, 10.0),
        bound_type=(0, 1, 0, 1)  # Reflecting bottom and left, vacuum top and right
    )

    material2 = Material(
        name="Fuel",
        sigma_s=0.5,
        sigma_a=0.02,
        mu_0=0.0,
        sigma_f=0.05,
        s=0.0,
        bounds=(20.0, 10.0),
        bound_type=(0, 1, 0, 1)  # Reflecting bottom and left, vacuum top and right
    )

    materials = [material1, material2]

    sigma_tr_watter = 0.01 + 0.21 * (1 - 0.0)  # sigma_tr = sigma_a + sigma_s * (1 - mu_0)
    D_watter = 1 / (3 * sigma_tr_watter)  # D = 1 / (3 * sigma_tr)
    sigma_tr_fuel = 0.02 + 0.5 * (1 - 0.0)
    D_fuel = 1 / (3 * sigma_tr_fuel)

    max_extrapolated_distance = max(0.7104 / sigma_tr_watter, 0.7104 / sigma_tr_fuel)
    
    # Create Mesh_constructor instance
    ncells_x = 30
    ncells_y = 10
    mesh = Mesh_constructor(ncells_x, ncells_y, materials)

    # Compute extrapolated boundaries
    mesh.compute_extrapolated_boundaries_y()
    mesh.compute_extrapolated_boundaries_x()

    # Verify extrapolated boundaries
    assert mesh.max_extrapolated_distance_top == max_extrapolated_distance, f"Expected max extrapolated distance top to be {max_extrapolated_distance}, got {mesh.max_extrapolated_distance_top}"
    assert mesh.max_extrapolated_distance_bottom == 0, "Expected max extrapolated distance bottom to be 0"
    assert mesh.extrapolated_distances_left == 0, "Expected extrapolated distances left to be 0"
    assert mesh.extrapolated_distances_right == 0.7104 / sigma_tr_fuel, f"Expected extrapolated distances right to be {0.7104 / sigma_tr_fuel}, got {mesh.extrapolated_distances_right}"

    # Compute total size
    mesh.compute_total_size()
    assert mesh.total_width == 30.0, f"Expected total width to be 30.0, got {mesh.total_width}"
    assert mesh.total_height == 10.0, f"Expected total height to be 10.0, got {mesh.total_height}"

    # Compute cell sizes
    dx, dy = mesh.compute_cell_sizes()
    assert dx == 1.0, f"Expected dx to be 1.0, got {dx}"
    assert dy == 1.0, f"Expected dy to be 1.0, got {dy}"


    # Create material matrix
    material_matrix = mesh.create_material_matrices()
    D_cells, Sigma_a_cells = mesh.Dcells, mesh.Sigma_acells
    assert D_cells.shape[0] == ncells_y, f"Expected material matrix to have {ncells_y} rows"
    assert D_cells.shape[1] == ncells_x, f"Expected material matrix to have {ncells_x} columns"
    assert Sigma_a_cells.shape[0] == ncells_y, f"Expected material matrix to have {ncells_y} rows"
    assert Sigma_a_cells.shape[1] == ncells_x, f"Expected material matrix to have {ncells_x} columns"

    print("Test for Mesh_constructor with reflecting boundaries passed!")


if __name__ == "__main__":
    test_mesh_constructor_with_test_1()
    test_mesh_constructor_with_reflecting_boundaries()