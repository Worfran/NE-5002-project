from src.classes.Material import Material as mat
import numpy as np

class Mesh_constructor:
    def __init__(self, ncells_x, ncells_y, materials):

        self.ncells_x = ncells_x
        self.ncells_y = ncells_y
        self.N = ncells_x * ncells_y
        self.materials = materials
    
    def compute_extrapolated_boundaries_y(self):
        # Ensure all materials have the same height
        material_heights = [material.get_hight() for material in self.materials]
        if len(set(material_heights)) > 1:
            raise ValueError("All materials must have the same height.")

        self.extrapolated_distances_top = []  
        self.extrapolated_distances_bottom = []  
        max_extrapolated_distance_top = 0
        max_extrapolated_distance_bottom = 0

        for material in self.materials:
            bound_type = material.get_bound_type()

            if bound_type[3]:
                extrapolated_distance = material.extrapolated_boundary_parameter()
                self.extrapolated_distances_top.append(extrapolated_distance)
                if extrapolated_distance > max_extrapolated_distance_top:
                    max_extrapolated_distance_top = extrapolated_distance
            else:
                self.extrapolated_distances_top.append(0)  
            
            if bound_type[2]:
                extrapolated_distance = material.extrapolated_boundary_parameter()
                self.extrapolated_distances_bottom.append(extrapolated_distance)
                if extrapolated_distance > max_extrapolated_distance_bottom:
                    max_extrapolated_distance_bottom = extrapolated_distance
            else:
                self.extrapolated_distances_bottom.append(0)


        # Check boundary consistency along the x-axis
        for i in range(len(self.materials) - 1):
            current_material = self.materials[i]
            next_material = self.materials[i + 1]

            # Check top boundary consistency between adjacent materials
            if current_material.get_bound_type()[2] != next_material.get_bound_type()[2]:
                raise ValueError(
                    f"Boundary inconsistency detected: Top boundaries of adjacent materials at index {i} and {i+1} must match."
                )

            # Check bottom boundary consistency between adjacent materials
            if current_material.get_bound_type()[3] != next_material.get_bound_type()[3]:
                raise ValueError(
                    f"Boundary inconsistency detected: Bottom boundaries of adjacent materials at index {i} and {i+1} must match."
                )

        self.max_extrapolated_distance_top = max_extrapolated_distance_top
        self.max_extrapolated_distance_bottom = max_extrapolated_distance_bottom

    def compute_extrapolated_boundaries_x(self):

        self.extrapolated_distances_left = 0 
        self.extrapolated_distances_right = 0  

        material_left = self.materials[0]
        material_right = self.materials[-1]

        bound_type_right = material_right.get_bound_type()
        bound_type_left = material_left.get_bound_type()


        if bound_type_left[0]:
            extrapolated_distance = material_left.extrapolated_boundary_parameter()
            self.extrapolated_distances_left += extrapolated_distance

        else:
            self.extrapolated_distances_left += 0

        if bound_type_right[1]:
            extrapolated_distance = material_right.extrapolated_boundary_parameter()
            self.extrapolated_distances_right += extrapolated_distance

        else:
            self.extrapolated_distances_right += 0
    
    def compute_total_size(self):
        total_width = 0
        total_height = 0

        for material in self.materials:
            bounds = material.get_bounds()
            width = bounds[0] 
            height = bounds[1] 
            total_width += width
            total_height = max(total_height, height)

        self.total_width = total_width + self.extrapolated_distances_left + self.extrapolated_distances_right
        self.total_height = total_height + self.max_extrapolated_distance_top + self.max_extrapolated_distance_bottom

    def compute_cell_sizes(self):
        self.compute_total_size()
        self.dx = self.total_width / self.ncells_x
        self.dy = self.total_height / self.ncells_y
        return self.dx, self.dy

    def create_material_matrices(self):
        self.Dcells = np.zeros((self.ncells_y, self.ncells_x))
        self.Sigma_acells = np.zeros((self.ncells_y, self.ncells_x))
        self.source_cells = np.zeros((self.ncells_y, self.ncells_x))

        self.compute_cell_sizes()
        current_x = 0
        n, m = self.ncells_x, self.ncells_y

        for material in self.materials:
            W, H = material.get_bounds()  # Get the width and height of the material


            # Fill the grid with the material properties
            for i in range(0, m):                
                material_cells_x = int(W // self.dx)  # Number of cells the material spans in x-direction
                
                # Determine how many cells in x-d
                for j in range(current_x, current_x + material_cells_x):
                    self.Dcells[i, j] = material.diffusion_coefficient()
                    self.Sigma_acells[i, j] = material.get_sigma_a()
                    self.source_cells[i, j] = material.get_s()
                
            current_x += material_cells_x  # Move to the next position in x-d
            self.mark_interfaces()

    def mark_interfaces(self):
        self.interfaces_x = []

        current_x = 0
        for material in self.materials:
            material_cells_x = int(material.get_bounds()[0] // self.dx)  # Number of cells the material spans in x-direction
            next_x = current_x + material_cells_x

            # Mark the interface at the boundary between this material and the next
            if next_x < self.ncells_x:  # Ensure we don't go out of bounds
                self.interfaces_x.append(next_x)

            current_x = next_x
        print(f"Interfaces at x-indices: {self.interfaces_x}")