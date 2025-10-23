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

    def entry_aij(self, i, j, value):
        a_ij = None
        top, bottom, left, right = self.check_boundaries(i, j)
        if top:
            a_ij = value / self.dy**2
        if bottom:
            a_ij = value / self.dy**2
        if left:
            a_ij = value / self.dx**2
        if right:
            a_ij = value / self.dx**2
        
        

