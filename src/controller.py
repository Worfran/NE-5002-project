from src.model import ProblemModel
from src.view import ProblemView

class ProblemController:
    def __init__(self):
        self.model = ProblemModel()
        self.view = ProblemView()

    def run(self):
        while True:
            self.view.display_menu()
            choice = self.view.get_menu_choice()
            if choice == "1":
                self.load_materials_from_file()
            elif choice == "2":
                self.enter_materials_manually()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def load_materials_from_file(self):
        try:
            file_path = self.view.get_file_path()
            self.model.create_materials_from_file(file_path)
            self.create_problem()
        except Exception as e:
            self.view.display_error(str(e))

    def enter_materials_manually(self):
        try:
            materials_data = self.view.get_material_data()
            self.model.create_materials_manually(materials_data)
            self.create_problem()
        except Exception as e:
            self.view.display_error(str(e))

    def create_problem(self):
        try:
            ncells_x, ncells_y = self.view.get_mesh_dimensions()
            self.model.create_mesh(ncells_x, ncells_y)
            self.model.create_matrix()
            solution = self.model.solve()
            self.view.display_solution(solution)
        except Exception as e:
            self.view.display_error(str(e))
    
    def create_problem(self):
        try:
            ncells_x, ncells_y = self.view.get_mesh_dimensions()
            self.model.create_mesh(ncells_x, ncells_y)
            self.model.create_matrix()
            solution = self.model.solve()
            self.view.display_solution(solution)
            self.model.plot_solution(solution)  # Plot the solution
        except Exception as e:
            self.view.display_error(str(e))

if __name__ == "__main__":
    controller = ProblemController()
    controller.run()