import numpy as np
from src.classes.Material import Material as mat

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
        self.construct_matrix()


    def construct_matrix(self):
        for i in range(self.Dcell.shape[0]):
            for j in range(self.Dcell.shape[1]):
                self.entries_aij(i, j, self.Dcell, self.Sigma_a_cell)

    def entries_aij(self, i, j, Dcell, Sigma_a_cell):
        a_ij = 0

        sum_aij = 0
        dx = self.dx
        dy = self.dy
        n = self.ncells_x
        m = self.ncells_y

        a_left, a_right, a_top, a_bottom = self.check_neighbors(i, j)
        a_left_vaccum, a_right_vaccum, a_top_vaccum, a_bottom_vaccum = self.check_boundary(i, j)

        ic = (m-i)*n - (m-j) - 1 # Index of the diagonal element in A

        if a_left:
            sum_aij -= (Dcell[i, j]*dy + Dcell[i, j-1]*dy) / 2*dx
            self.A[ic-1, ic] = - (Dcell[i, j]*dy + Dcell[i, j-1]*dy) / 2*dx
        elif a_left_vaccum:
            sum_aij -= Dcell[i, j]*dy / dx
        elif not a_left and not a_left_vaccum:
            sum_aij -= Dcell[i, j]*dy / 2*dx

        if a_right:
            self.A[ic+1, ic] = - (Dcell[i, j]*dy + Dcell[i, j+1]*dy) / 2*dx
            sum_aij -= (Dcell[i, j]*dy + Dcell[i, j+1]*dy) / 2*dx
        elif a_right_vaccum:
            self.A[ic+1, ic] = - Dcell[i, j] *dy/ 2*dx
            sum_aij -= Dcell[i, j] *dy/ dx
        elif not a_right and not a_right_vaccum:
            sum_aij -= Dcell[i, j] *dy/ 2*dx

        if a_top:
            self.A[ic, ic+n] = - (Dcell[i, j]*dx + Dcell[i-1, j]*dx) / 2*dy
            sum_aij -= (Dcell[i, j]*dx + Dcell[i-1, j]*dx) / 2*dy
        elif a_top_vaccum:
            sum_aij -= Dcell[i, j] *dx/ dy
        elif not a_top and not a_top_vaccum:
            sum_aij -= Dcell[i, j] *dx/ 2*dy

        if a_bottom:
            self.A[ic, ic-n] = - (Dcell[i, j]*dx + Dcell[i+1, j]*dx) / 2*dy
            sum_aij -= (Dcell[i, j]*dx + Dcell[i+1, j]*dx) / 2*dy
        elif a_bottom_vaccum:
            sum_aij -= Dcell[i, j] *dx/ dy
        elif not a_bottom and not a_bottom_vaccum:
            sum_aij -= Dcell[i, j] *dy/ 2*dy

        a_ij = Sigma_a_cell[i, j] - sum_aij

        self.A[ic, ic] = a_ij

    def check_neighbors(self, i, j):
        n = self.ncells_x
        m = self.ncells_y

        has_left = j > 0
        has_right = j < n - 1
        has_top = i > 0
        has_bottom = i < m - 1

        return has_left, has_right, has_top, has_bottom

    def check_boundary(self, i, j):
        n = self.ncells_x
        m = self.ncells_y
        material_r = self.materials[0]
        material_l = self.materials[-1]
        bound_type_r = material_r.get_bound_type()
        bound_type_l = material_l.get_bound_type()
        a_right_vaccum, a_top_vaccum = bound_type_r[0], bound_type_r[3]
        a_left_vaccum, a_bottom_vaccum = bound_type_l[1], bound_type_l[2]

        return a_left_vaccum, a_right_vaccum, a_top_vaccum, a_bottom_vaccum
    