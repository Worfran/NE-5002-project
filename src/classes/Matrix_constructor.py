import numpy as np
import Material as mat

class Matrix_constructor:
    def __init__(self, ncells_x, ncells_y, materials):

        self.ncells_x = ncells_x
        self.ncells_y = ncells_y
        self.N = ncells_x * ncells_y
        self.materials = materials
        self.A = np.zeros((self.N, self.N))
        self.b = np.zeros(self.N)

    def entry_aii(self, i, j, Dcell, Sigma_a_cell):
        a_ij = None
        a_ij1, a_ij_1, a_i1j, a_i_1j = 0, 0, 0, 0
        sum_aij = 0


        a_left, a_right, a_top, a_bottom = self.check_neighbors(i, j)
        a_left_vaccum, a_right_vaccum, a_top_vaccum, a_bottom_vaccum = self.check_boundary(i, j)

        dx_1, dy_1, dx, dy, dx1, dy1 = self.compute_dx_dy(i, j)

        if a_left:
            sum_aij += (Dcell[i, j]*dx + Dcell[i, j-1]*dx_1) / 2*dx
        elif a_left_vaccum:
            sum_aij += Dcell[i, j] / dx

        if a_right:
            sum_aij += (Dcell[i, j]*dx + Dcell[i, j+1]*dx1) / 2*dx
        elif a_right_vaccum:
            sum_aij += Dcell[i, j] / dx

        if a_top:
            sum_aij += (Dcell[i, j]*dy + Dcell[i-1, j]*dy1) / 2*dy
        elif a_top_vaccum:
            sum_aij += Dcell[i, j] / dy

        if a_bottom:
            sum_aij += (Dcell[i, j]*dy + Dcell[i+1, j]*dy_1) / 2*dy
        elif a_bottom_vaccum:
            sum_aij += Dcell[i, j] / dy

        a_ij = Sigma_a_cell[i, j] - sum_aij

        return a_ij
    
    def check_neighbors(self, i, j):
        a_left = j > 0
        a_right = j < self.ncells_x - 1
        a_top = i > 0
        a_bottom = i < self.ncells_y - 1
        return a_left, a_right, a_top, a_bottom

    def check_boundary(self, i, j):
        material = self.get_material_at_cell(i, j)
        return material.get_bound_type()
       
    def get_material_at_cell(self, i, j):
        x = j * self.dx 
        y = i * self.dy
        for material in self.materials:
            x_min, x_max, y_min, y_max = material.bounds
            if x_min <= x <= x_max and y_min <= y <= y_max:
                return material
        raise ValueError(f"No material found at cell ({i}, {j}) with center ({x}, {y})")
    
    def compute_dx_dy(self, i, j):
        material_cell = self.get_material_at_cell(i, j)
        material_neighbors = self.get_neighboring_materials(i, j)
        # Compute dx
        (x0, x1, y0, y1) = material_cell.get_x_bounds()
        dx = (x1 - x0)/self.ncells_x
        dy = (y1 - y0)/self.ncells_y

        dx1 = (x1 - x0)/self.ncells_x
        dy1 = (y1 - y0)/self.ncells_y

        if 'right' in material_neighbors:
            neighbor = material_neighbors['right']
            (nx0, nx1, _, _) = neighbor.get_x_bounds()
            dx1 = (nx1 - nx0)/self.ncells_x
        
        if 'top' in material_neighbors:
            neighbor = material_neighbors['top']
            (_, _, ny0, ny1) = neighbor.get_x_bounds()
            dy1 = (ny1 - ny0)/self.ncells_y
        
        dx_1 = (x1 + x0) / 2
        dy_1 = (y1 + y0) / 2

        if 'left' in material_neighbors:
            neighbor = material_neighbors['left']
            (nx0, nx1, _, _) = neighbor.get_x_bounds()
            dx_1 = (nx1 - nx0)/self.ncells_x
        
        if 'bottom' in material_neighbors:
            neighbor = material_neighbors['bottom']
            (_, _, ny0, ny1) = neighbor.get_x_bounds()
            dy_1 = (ny1 - ny0)/self.ncells_y
        
        return (dx_1, dy_1, dx, dy, dx1, dy1)


    def get_neighboring_materials(self, i, j):
        neighbors = {}
        a_left, a_right, a_top, a_bottom = self.check_neighbors(i, j)
        if a_left:
            neighbors['left'] = self.get_material_at_cell(i, j-1)
        if a_right:
            neighbors['right'] = self.get_material_at_cell(i, j+1)
        if a_top:
            neighbors['top'] = self.get_material_at_cell(i-1, j)
        if a_bottom:
            neighbors['bottom'] = self.get_material_at_cell(i+1, j)
        return neighbors
