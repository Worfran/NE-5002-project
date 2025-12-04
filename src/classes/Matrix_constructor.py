import numpy as np
from src.classes.Material import Material as mat

class Matrix_constructor:
    def __init__(self, ncells_x, ncells_y, Dcell, Sigma_a_cell, source_cells, dx, dy, materials, interfaces_x):

        self.ncells_x = ncells_x
        self.ncells_y = ncells_y
        self.materials = materials
        self.Dcell = Dcell
        self.Sigma_a_cell = Sigma_a_cell
        self.source_cells = source_cells
        self.interfaces_x = interfaces_x
        self.dx = dx
        self.dy = dy
        self.A = np.zeros((self.ncells_y*self.ncells_x, self.ncells_y*self.ncells_x))
        self.b = np.zeros(self.ncells_y * self.ncells_x)
        self.construct_matrix()
        self.source_term()

    def source_term(self):
        self.b = np.zeros(self.ncells_y * self.ncells_x)
        m, n = self.ncells_y, self.ncells_x
        for i in range(m): #m
            for j in range(n): #n
                l = n*(m-(i+1)) + j
                self.b[l] = self.source_cells[i, j]
                if j < n-1 and j in self.interfaces_x and self.source_cells[i, j-1] != self.source_cells[i, j]:
                    self.b[l] = (self.source_cells[i, j] + self.source_cells[i, j-1])/2
                elif j < n-1 and j in self.interfaces_x and self.source_cells[i, j+1] != self.source_cells[i, j]:
                    self.b[l] = (self.source_cells[i, j] + self.source_cells[i, j+1])/2

    def construct_matrix(self):
        m, n = self.ncells_y, self.ncells_x
        for i in range(m):
            for j in range(n):
                self.entries_aij(i, j, self.Dcell, self.Sigma_a_cell)

    def entries_aij(self, i, j, Dcell, Sigma_a_cell):
        dx = self.dx
        dy = self.dy
        n  = self.ncells_x
        m  = self.ncells_y

        ic = n * (m - (i + 1)) + j  # global index

        has_left, has_right, has_top, has_bottom = self.check_neighbors(i, j)
        left_vac, right_vac, top_vac, bottom_vac = self.check_boundary(i, j)

        D_ij = Dcell[i, j]
        sum_aij = 0.0

        # ---------- LEFT FACE ----------
        if has_left:
            # Interior face
            is_interface = (j in self.interfaces_x)
            D_nb = Dcell[i, j - 1]
            if is_interface:
                D_face = 0.5 * (D_ij + D_nb)
            else:
                D_face = D_ij
            coeff = D_face * dy / dx
            self.A[ic, ic - 1] -= coeff
            sum_aij += coeff
        else:
            # Boundary face at left edge
            if left_vac:

                D_face = D_ij
                coeff = D_face * dy / dx
                sum_aij += coeff
            else:
 
                D_face = D_ij
                coeff = D_face * dy / (2.0 * dx)
                sum_aij += coeff

        # ---------- RIGHT FACE ----------
        if has_right:
            # Interior face
            is_interface = (j in self.interfaces_x)
            D_nb = Dcell[i, j + 1]
            if is_interface:
                D_face = 0.5 * (D_ij + D_nb)
            else:
                D_face = D_ij
            coeff = D_face * dy / dx
            self.A[ic, ic + 1] -= coeff
            sum_aij += coeff
        else:
            # Boundary face at right edge
            if right_vac:
                # Vacuum BC
                D_face = D_ij
                coeff = D_face * dy / dx
                sum_aij += coeff
            else:
                # Reflective BC
                D_face = D_ij
                coeff = D_face * dy / (2.0 * dx)
                sum_aij += coeff

        # ---------- TOP FACE (i-1) ----------
        if has_top:
            # Interior face
            D_nb = Dcell[i - 1, j]
            D_face = 0.5 * (D_ij + D_nb)  
            coeff = D_face * dx / dy
            self.A[ic, ic + n] -= coeff
            sum_aij += coeff
        else:
            # Boundary at top edge
            if top_vac:
                D_face = D_ij
                coeff = D_face * dx / dy
                sum_aij += coeff
            else:
                D_face = D_ij
                coeff = D_face * dx / (2.0 * dy)
                sum_aij += coeff

        # ---------- BOTTOM FACE (i+1) ----------
        if has_bottom:
            # Interior face
            D_nb = Dcell[i + 1, j]
            D_face = 0.5 * (D_ij + D_nb)
            coeff = D_face * dx / dy
            self.A[ic, ic - n] -= coeff
            sum_aij += coeff
        else:
            # Boundary at bottom edge
            if bottom_vac:
                D_face = D_ij
                coeff = D_face * dx / dy
                sum_aij += coeff
            else:
                D_face = D_ij
                coeff = D_face * dx / (2.0 * dy)
                sum_aij += coeff


        Sigma_a_cell_ij = Sigma_a_cell[i, j]
        self.A[ic, ic] = Sigma_a_cell_ij + sum_aij
        if ic == 4:  # or any of the indices where row was zero
            print("DEBUG dead cell (i,j):", i, j,
                "D=", D_ij, "Sigma=", Sigma_a_cell_ij)


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
        a_right_vaccum, a_top_vaccum = bound_type_r[1], bound_type_r[3]
        a_left_vaccum, a_bottom_vaccum = bound_type_l[0], bound_type_l[2]

        return a_left_vaccum, a_right_vaccum, a_top_vaccum, a_bottom_vaccum