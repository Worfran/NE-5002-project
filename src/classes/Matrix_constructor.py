import numpy as np
import Material as mat

class Matrix_constructor:
    def __init__(self, ncells_x, ncells_y, Dcell, Sigma_a_cell, dx, dy, materials):

        self.ncells_x = ncells_x
        self.ncells_y = ncells_y
        self.materials = materials
        self.Dcell = Dcell
        self.Sigma_a_cell = Sigma_a_cell
        self.dx = dx
        self.dy = dy
        self.A = np.zeros((self.ncells_y*self.ncells_x, self.ncells_y*self.ncells_x))
        self.b = np.zeros(self.ncells_y * self.ncells_x)

    def entries_aij(self, i, j, Dcell, Sigma_a_cell):
        a_ij = 0
        a_ij1, a_ij_1, a_i1j, a_i_1j = 0, 0, 0, 0
        sum_aij = 0
        dx = self.dx
        dy = self.dy
        n = self.ncells_x
        m = self.ncells_y

        a_left, a_right, a_top, a_bottom = self.check_neighbors(i, j)
        a_left_vaccum, a_right_vaccum, a_top_vaccum, a_bottom_vaccum = self.check_boundary(i, j)

        if a_left:
            sum_aij += (Dcell[i, j]*dx + Dcell[i, j-1]*dx) / 2*dx
            self.A[(n-j)*m+i%n,(n-j)*m+i%n-1] = - (Dcell[i, j]*dx + Dcell[i, j-1]*dx) / 2*dx
        elif a_left_vaccum:
            self.A[(n-j)*m+i%n,(n-j)*m+i%n-1] = - Dcell[i, j] / dx
            sum_aij += Dcell[i, j] / dx
        else:
            pass

        if a_right:
            sum_aij += (Dcell[i, j]*dx + Dcell[i, j+1]*dx) / 2*dx
        elif a_right_vaccum:
            sum_aij += Dcell[i, j] / dx
        else:
            pass

        if a_top:
            sum_aij += (Dcell[i, j]*dy + Dcell[i-1, j]*dy) / 2*dy
        elif a_top_vaccum:
            sum_aij += Dcell[i, j] / dy
        else:
            pass

        if a_bottom:
            sum_aij += (Dcell[i, j]*dy + Dcell[i+1, j]*dy) / 2*dy
        elif a_bottom_vaccum:
            sum_aij += Dcell[i, j] / dy
        else:
            pass

        a_ij = Sigma_a_cell[i, j] - sum_aij

        return a_ij

def check_neighbors(self, i, j):
    None

def check_boundary(self, i, j):
    None
 