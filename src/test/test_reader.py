import os 
import tempfile
import ultraimport

# Dynamically import the File_reader module using ultraimport
File_reader = ultraimport('__dir__/../classes/File_reader.py')

def test_parse_materials():
    # Create a temporary file with two materials
    materials_data = """\
Material 1:
  name: Water
  sigma_tr: 0.21
  sigma_a: 0.01
  mu_0: 0.0
  sigma_f: 0.0
  s: 1.0
  bounds: (0.0, 10.0, 0.0, 10.0)
  bound_type: (1, 1, 0, 0)

Material 2:
  name: Fuel
  sigma__tr: 0.5
  sigma_a: 0.02
  mu_0: 0.1
  sigma_f: 0.05
  s: 0.0
  bounds: (10.0, 20.0, 0.0, 10.0)
  bound_type: (0, 0, 0, 0)
"""
    # Write the materials data to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as temp_file:
        temp_file.write(materials_data)
        temp_file_path = temp_file.name

    try:
        # Parse the materials from the file
        materials = File_reader.parse_materials_from_file(temp_file_path)

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