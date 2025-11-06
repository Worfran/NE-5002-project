import os
from src.classes.Reader import DocumentReader

def test_document_reader_with_test_1():
    file_path = "input_files_examples/test_1.txt"
    reader = DocumentReader(file_path)
    reader.read_file()
    reader.parse_materials()
    materials = reader.get_materials()

    # Assertions for Material 1
    assert len(materials) == 2, "Expected 2 materials to be parsed"
    material1 = materials[0]
    assert material1.get_name() == "Water"
    assert material1.get_sigma_s() == 0.21
    assert material1.get_sigma_a() == 0.01
    assert material1.get_mu_0() == 0.0
    assert material1.get_sigma_f() == 0.0
    assert material1.get_s() == 1.0
    assert material1.get_bounds() == (10.0, 10.0)
    assert material1.get_bound_type() == (True, True, False, False)

    # Assertions for Material 2
    material2 = materials[1]
    assert material2.get_name() == "Fuel"
    assert material2.get_sigma_s() == 0.5
    assert material2.get_sigma_a() == 0.02
    assert material2.get_mu_0() == 0.1
    assert material2.get_sigma_f() == 0.05
    assert material2.get_s() == 0.0
    assert material2.get_bounds() == (20.0, 10.0)
    assert material2.get_bound_type() == (False, False, False, False)

    print("Test 1 passed!")


def test_document_reader_with_test_2():
    file_path = "input_files_examples/test_2.txt"
    reader = DocumentReader(file_path)
    reader.read_file()
    reader.parse_materials()
    materials = reader.get_materials()

    # Assertions for Material 1
    assert len(materials) == 3, "Expected 3 materials to be parsed"
    material1 = materials[0]
    assert material1.get_name() == "Water"
    assert material1.get_sigma_s() == 0.21
    assert material1.get_sigma_a() == 0.01
    assert material1.get_mu_0() == 0.0
    assert material1.get_sigma_f() == 0.0
    assert material1.get_s() == 1.0
    assert material1.get_bounds() == (10.0, 10.0)
    assert material1.get_bound_type() == (True, True, False, False)

    # Assertions for Material 2
    material2 = materials[1]
    assert material2.get_name() == "Fuel"
    assert material2.get_sigma_s() == 0.5
    assert material2.get_sigma_a() == 0.02
    assert material2.get_mu_0() == 0.1
    assert material2.get_sigma_f() == 0.01
    assert material2.get_s() == 0.0
    assert material2.get_bounds() == (20.0,10.0)
    assert material2.get_bound_type() == (False, False, False, False)

    # Assertions for Material 3
    material3 = materials[2]
    assert material3.get_name() == "Water"
    assert material3.get_sigma_s() == 0.21
    assert material3.get_sigma_a() == 0.01
    assert material3.get_mu_0() == 0.0
    assert material3.get_sigma_f() == 0.0
    assert material3.get_s() == 1.0
    assert material3.get_bounds() == (10.0, 10.0)
    assert material3.get_bound_type() == (True, True, False, False)

    print("Test 2 passed!")


def test_document_reader_with_test_3():
    file_path = "input_files_examples/test_3.txt"
    reader = DocumentReader(file_path)
    reader.read_file()

    try:
        reader.parse_materials()
        assert False, "Expected an error due to invalid input in test_3.txt"
    except ValueError as e:
        # Check that the error message is related to the invalid bound_type
        assert "Boolean values must be '1' or '0'" in str(e), f"Unexpected error message: {e}"

    print("Test 3 failed as expected due to invalid input!")


if __name__ == "__main__":
    test_document_reader_with_test_1()
    test_document_reader_with_test_2()
    test_document_reader_with_test_3()