from src.classes.Material import Material as mat
import numpy as np

class Mesh_constructor:
    def __init__(self, ncells_x, ncells_y, materials):

        self.ncells_x = ncells_x
        self.ncells_y = ncells_y
        self.N = ncells_x * ncells_y
        self.materials = materials

    def compute_extrapolated_boundaries_y(self):
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
                max_extrapolated_distance_top = max(
                    max_extrapolated_distance_top, extrapolated_distance
                )
            else:
                self.extrapolated_distances_top.append(0)  
            
            if bound_type[2]:
                extrapolated_distance = material.extrapolated_boundary_parameter()
                self.extrapolated_distances_bottom.append(extrapolated_distance)
                max_extrapolated_distance_bottom = max(
                    max_extrapolated_distance_bottom, extrapolated_distance
                )
            else:
                self.extrapolated_distances_bottom.append(0)

        # Consistency along x
        for i in range(len(self.materials) - 1):
            current_material = self.materials[i]
            next_material = self.materials[i + 1]

            if current_material.get_bound_type()[2] != next_material.get_bound_type()[2]:
                raise ValueError(
                    f"Boundary inconsistency detected: Top boundaries of adjacent "
                    f"materials at index {i} and {i+1} must match."
                )

            if current_material.get_bound_type()[3] != next_material.get_bound_type()[3]:
                raise ValueError(
                    f"Boundary inconsistency detected: Bottom boundaries of adjacent "
                    f"materials at index {i} and {i+1} must match."
                )

        self.max_extrapolated_distance_top = max_extrapolated_distance_top
        self.max_extrapolated_distance_bottom = max_extrapolated_distance_bottom

    def compute_extrapolated_boundaries_x(self):

        self.extrapolated_distances_left = 0.0 
        self.extrapolated_distances_right = 0.0  

        material_left = self.materials[0]
        material_right = self.materials[-1]

        bound_type_right = material_right.get_bound_type()
        bound_type_left = material_left.get_bound_type()

        if bound_type_left[0]:
            self.extrapolated_distances_left += material_left.extrapolated_boundary_parameter()

        if bound_type_right[1]:
            self.extrapolated_distances_right += material_right.extrapolated_boundary_parameter()
    
    def compute_total_size(self):
        total_width = 0.0
        total_height = 0.0

        for material in self.materials:
            bounds = material.get_bounds()
            width = bounds[0] 
            height = bounds[1] 
            total_width += width
            total_height = max(total_height, height)

        self.total_width = (
            total_width
            + self.extrapolated_distances_left
            + self.extrapolated_distances_right
        )
        self.total_height = (
            total_height
            + self.max_extrapolated_distance_top
            + self.max_extrapolated_distance_bottom
        )

    def compute_cell_sizes(self):
        self.compute_total_size()
        self.dx = self.total_width / self.ncells_x
        self.dy = self.total_height / self.ncells_y
        return self.dx, self.dy

    def _compute_cells_per_material(self):
        """
        Compute how many x-cells each material occupies, in a way that:
          - Is proportional to its physical width.
          - Sums exactly to ncells_x.
          - Uses a largest-remainder style rule for fairness.
        """
        n = self.ncells_x

        # Physical widths of each material (exclude extrapolated distances)
        widths = [mat.get_bounds()[0] for mat in self.materials]
        total_width_materials = sum(widths)

        if total_width_materials <= 0.0:
            raise ValueError("Total material width must be positive.")

        # Ideal (non-integer) cell count per material based only on material widths
        ideal_cells = [n * (w / total_width_materials) for w in widths]

        # Base integer cells and remainders
        base_cells = [int(np.floor(c)) for c in ideal_cells]
        cells_used = sum(base_cells)
        leftover = n - cells_used

        # Distribute leftover cells according to largest remainders
        remainders = [ideal_cells[k] - base_cells[k] for k in range(len(widths))]
        order = np.argsort(remainders)[::-1] 

        for idx in order[:max(0, leftover)]:
            base_cells[idx] += 1


        if sum(base_cells) != n:
            diff = n - sum(base_cells)
            base_cells[-1] += diff

        self.cells_per_material = base_cells

    def create_material_matrices(self):
        self.Dcells = np.zeros((self.ncells_y, self.ncells_x))
        self.Sigma_acells = np.zeros((self.ncells_y, self.ncells_x))
        self.source_cells = np.zeros((self.ncells_y, self.ncells_x))

        self.compute_cell_sizes()

        self._compute_cells_per_material()   

        current_x = 0
        n, m = self.ncells_x, self.ncells_y

        for k, material in enumerate(self.materials):
            material_cells_x = self.cells_per_material[k]
            end_x = current_x + material_cells_x

            D_val = material.diffusion_coefficient()
            Sigma_val = material.get_sigma_a()
            s_val = material.get_s()

            for i in range(m):
                for j in range(current_x, end_x):
                    self.Dcells[i, j] = D_val
                    self.Sigma_acells[i, j] = Sigma_val
                    self.source_cells[i, j] = s_val

            current_x = end_x

        # mark interface indices
        self.mark_interfaces()

        # average interface columns directly in the world mesh
        self._apply_interface_cell_averaging()


    def mark_interfaces(self):
        """
        Mark x-indices where there is an interface between two different materials.
        """
        self.interfaces_x = []
        current_x = 0
        n = self.ncells_x

        # Iterate over all but the last material to mark interior interfaces
        for k in range(len(self.materials) - 1):
            material_cells_x = self.cells_per_material[k]
            next_x = current_x + material_cells_x

            if 0 < next_x < n:
                self.interfaces_x.append(next_x)

            current_x = next_x
    
    def _apply_interface_cell_averaging(self):
        m, n = self.ncells_y, self.ncells_x

        for j_if in getattr(self, "interfaces_x", []):
            if not (0 < j_if < n): 
                continue

            for i in range(m):
                # left and right values as currently filled
                D_left   = self.Dcells[i, j_if - 1]
                D_right  = self.Dcells[i, j_if]
                Sa_left  = self.Sigma_acells[i, j_if - 1]
                Sa_right = self.Sigma_acells[i, j_if]
                s_left   = self.source_cells[i, j_if - 1]
                s_right  = self.source_cells[i, j_if]

                # average for the interface column
                self.Dcells[i, j_if]       = 0.5 * (D_left + D_right)
                self.Sigma_acells[i, j_if] = 0.5 * (Sa_left + Sa_right)
                self.source_cells[i, j_if] = 0.5 * (s_left + s_right)
