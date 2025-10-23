import os
import tempfile
from src.classes.File_reader import parse_materials_from_file

def test_parse_materials():

    materials_data = "../../input_files_examples/test_1.txt"
    # Write the materials data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
        temp_file.write(materials_data)
        temp_file_path = temp_file.name

    try:
        # Parse the materials from the file
        materials = parse_materials_from_file(temp_file_path)

        # Assertions for Material 1
        assert len(materials) == 2, "Expected 2 materials to be parsed"
        material1 = materials[0]
        assert material1.get_name() == "Water"
        assert material1.get_sigma__tr() == 0.21
        assert material1.get_sigma_a() == 0.01
        assert material1.get_mu_0() == 0.0
        assert material1.get_sigma_f() == 0.0
        assert material1.get_s() == 1.0
        assert material1.get_bounds() == (0.0, 10.0, 0.0, 10.0)
        assert material1.get_bound_type() == (True, True, False, False)

        # Assertions for Material 2
        material2 = materials[1]
        assert material2.get_name() == "Fuel"
        assert material2.get_sigma__tr() == 0.5
        assert material2.get_sigma_a() == 0.02
        assert material2.get_mu_0() == 0.1
        assert material2.get_sigma_f() == 0.05
        assert material2.get_s() == 0.0
        assert material2.get_bounds() == (10.0, 20.0, 0.0, 10.0)
        assert material2.get_bound_type() == (False, False, False, False)

        print("All tests passed!")

    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)

if __name__ == "__main__":
    test_parse_materials()