import unittest
from src.controller import ProblemController 

class TestApp(unittest.TestCase):
    def setUp(self):
        # Initialize the app controller
        self.controller = ProblemController()

    def test_load_materials(self):
        # Test loading materials from a file
        materials_file = "test_app_1.txt"
        result = self.controller.load_materials(materials_file)
        self.assertTrue(result, "Failed to load materials")
        self.assertGreater(len(self.controller.materials), 0, "Materials list is empty after loading")

    def test_verify_materials(self):
        # Test verifying the loaded materials
        materials_file = "test_app_1.txt"
        self.controller.load_materials(materials_file)
        verification_result = self.controller.verify_materials()
        self.assertTrue(verification_result, "Materials verification failed")

    def test_apply_solution(self):
        # Test applying the solution after loading and verifying materials
        materials_file = "test_app_1.txt"
        self.controller.load_materials(materials_file)
        self.controller.verify_materials()
        solution_result = self.controller.apply_solution()
        self.assertTrue(solution_result, "Solution application failed")

if __name__ == "__main__":
    unittest.main()