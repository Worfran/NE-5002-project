class ProblemView:
    def display_menu(self):
        print("Welcome to the Problem Solver!")
        print("1. Load materials from file")
        print("2. Enter materials manually")
        print("3. Exit")

    def get_menu_choice(self):
        return input("Enter your choice: ")

    def get_file_path(self):
        return input("Enter the file path: ")

    def get_material_data(self):
        materials = []
        while True:
            print("Enter material properties:")
            name = input("Name: ")
            sigma_s = float(input("Sigma_s: "))
            sigma_a = float(input("Sigma_a: "))
            mu_0 = float(input("Mu_0: "))
            sigma_f = float(input("Sigma_f: "))
            s = float(input("Source term: "))
            bounds = tuple(map(float, input("Bounds (width, height): ").split(",")))
            bound_type = tuple(map(int, input("Bound type (x0, x1, y0, y1): ").split(",")))
            materials.append({
                "name": name,
                "sigma_s": sigma_s,
                "sigma_a": sigma_a,
                "mu_0": mu_0,
                "sigma_f": sigma_f,
                "s": s,
                "bounds": bounds,
                "bound_type": bound_type
            })
            more = input("Add another material? (y/n): ")
            if more.lower() != "y":
                break
        return materials

    def get_mesh_dimensions(self):
        ncells_x = int(input("Enter number of cells in x-direction: "))
        ncells_y = int(input("Enter number of cells in y-direction: "))
        return ncells_x, ncells_y

    def display_solution(self, solution):
        print("Solution:")
        print(solution)

    def display_error(self, error_message):
        print(f"Error: {error_message}")

    def display_solution(self, solution):
        print("Solution:")
        print(solution)
        print("Displaying solution plot...")