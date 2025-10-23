import numpy as np

class Matrix_constructor:
    def __init__(self, ncells_x, ncells_y, dx, dy):
        self.ncells_x = ncells_x
        self.ncells_y = ncells_y
        self.dx = dx
        self.dy = dy
        self.N = ncells_x * ncells_y
        self.A = np.zeros((self.N, self.N))
        self.b = np.zeros(self.N)

    def entry_aii(self, i, j, Dcell, Sigma_a_cell):
        a_ij = None
        sum_aij = 0
        a_left, a_right, a_top, a_bottom = self.check_neighbors(i, j)
        if a_left:
            sum_aij += (Dcell[i, j] + Dcell[i, j+1]) / self.dx**2
        if a_right:
            sum_aij += (Dcell[i, j] + Dcell[i, j-1]) / self.dx**2
        if a_top:
            sum_aij += (Dcell[i, j] + Dcell[i-1, j]) / self.dy**2
        if a_bottom:
            sum_aij += (Dcell[i, j] + Dcell[i+1, j]) / self.dy**2
        
        a_ij = Sigma_a_cell[i, j] - sum_aij

        return a_ij
    
    def check_neighbors(self, i, j):
        a_left = j > 0
        a_right = j < self.ncells_x - 1
        a_top = i > 0
        a_bottom = i < self.ncells_y - 1
        return a_left, a_right, a_top, a_bottom

        


