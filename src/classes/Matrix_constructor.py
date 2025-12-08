import numpy as np
from src.classes.Material import Material as mat

class Matrix_constructor:
    def __init__(self, ncells_x, ncells_y,
                 Dcell, Sigma_a_cell, source_cells,
                 dx, dy, materials, interfaces_x):

        self.ncells_x = ncells_x
        self.ncells_y = ncells_y
        self.materials = materials
        self.Dcell = Dcell
        self.Sigma_a_cell = Sigma_a_cell
        self.source_cells = source_cells
        self.interfaces_x = interfaces_x

        self.dx = dx
        self.dy = dy

        N = self.ncells_y * self.ncells_x
        self.A = np.zeros((N, N))
        self.b = np.zeros(N)

        self.construct_matrix()
        self.source_term()
        self.apply_vacuum()


    def source_term(self):
        """
        Map source_cells (i,j) directly into b[l]
        using the same global indexing as A.
        """
        m, n = self.ncells_y, self.ncells_x
        self.b = np.zeros(m * n)

        for i in range(m):
            for j in range(n):
                l = n * (m - (i + 1)) + j
                self.b[l] = self.source_cells[i, j]

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

        ic = n * (m - (i + 1)) + j  # index in A,b

        has_left, has_right, has_top, has_bottom = self.check_neighbors(i, j)
        left_vac, right_vac, top_vac, bottom_vac = self.check_boundary(i, j)

        D_ij = Dcell[i, j]
        sum_aij = 0.0

        # ---------- LEFT FACE ----------
        if has_left:
            D_face = D_ij
            coeff = D_face * dy / dx
            self.A[ic, ic - 1] -= coeff
            sum_aij += coeff
        else:
            # Boundary face at left edge
            if left_vac:
                # Vacuum BC: flux = 0 outside
                D_face = D_ij
                coeff = D_face * dy / dx
                sum_aij += coeff
            else:
                # Reflective BC
                D_face = D_ij
                coeff = D_face * dy / (2.0 * dx)
                sum_aij += coeff

        # ---------- RIGHT FACE ----------
        if has_right:
            # Interior face
            D_face = D_ij
            coeff = D_face * dy / dx
            self.A[ic, ic + 1] -= coeff
            sum_aij += coeff
        else:
            # Boundary face at right edge
            if right_vac:
                D_face = D_ij
                coeff = D_face * dy / dx
                sum_aij += coeff
            else:
                D_face = D_ij
                coeff = D_face * dy / (2.0 * dx)
                sum_aij += coeff

        # ---------- TOP FACE (i-1) ----------
        if has_top:
            D_face = D_ij
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
            D_face = D_ij
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

        # Diagonal: absorption + sum of outflow coefficients
        Sigma_a_cell_ij = Sigma_a_cell[i, j]
        self.A[ic, ic] = Sigma_a_cell_ij + sum_aij


    def check_neighbors(self, i, j):
        n = self.ncells_x
        m = self.ncells_y

        has_left   = j > 0
        has_right  = j < n - 1
        has_top    = i > 0
        has_bottom = i < m - 1

        return has_left, has_right, has_top, has_bottom

    def check_boundary(self, i, j):
        """
        Return (left_vac, right_vac, top_vac, bottom_vac)
        consistent with Mesh_constructor:
          - materials[0]  = left material
          - materials[-1] = right material
        bound_type = (left, right, bottom, top).
        """
        material_left  = self.materials[0]
        material_right = self.materials[-1]

        bound_type_left  = material_left.get_bound_type()
        bound_type_right = material_right.get_bound_type()

        a_left_vac   = bound_type_left[0]
        a_right_vac  = bound_type_right[1]
        a_bottom_vac = bound_type_left[2]
        a_top_vac    = bound_type_right[3]

        return a_left_vac, a_right_vac, a_top_vac, a_bottom_vac


    def apply_vacuum(self):
        """
        Enforce φ = 0 on vacuum boundaries by turning those cells into
        A[row,:]=0, A[row,row]=1, b[row]=0.
        """
        m, n = self.ncells_y, self.ncells_x

        left_vac, right_vac, top_vac, bottom_vac = self.check_boundary(0, 0)

        # Left edge
        if left_vac:
            for i in range(m):
                self.set_flux_zero(i, 0)

        # Right edge
        if right_vac:
            for i in range(m):
                self.set_flux_zero(i, n - 1)

        # Top edge (i = 0)
        if top_vac:
            for j in range(n):
                self.set_flux_zero(0, j)

        # Bottom edge (i = m - 1)
        if bottom_vac:
            for j in range(n):
                self.set_flux_zero(m - 1, j)

    def set_flux_zero(self, i, j):
        """
        Apply φ=0 at a single cell (i,j).
        """
        ic = self.ncells_x * (self.ncells_y - (i + 1)) + j
        self.A[ic, :] = 0.0
        self.A[:, ic] = 0.0
        self.A[ic, ic] = 1.0
        self.b[ic] = 0.0
