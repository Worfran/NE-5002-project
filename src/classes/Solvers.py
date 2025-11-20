import numpy as np

class Solvers:
    """
    Simple container for stationary iterative linear solvers: Jacobi, Gauss-Seidel, and SOR.
    Usage:
        s = Solvers(A, b, x0=None, tol=1e-10, max_iter=1000)
        x = s.jacobi()
        x = s.gauss_seidel()
        x = s.sor(omega=1.25)
    """

    def __init__(self, A, b, x0=None, tol=1e-10, max_iter=1000):
        self.A = np.asarray(A, dtype=float)
        self.b = np.asarray(b, dtype=float)

        if self.A.ndim != 2 or self.A.shape[0] != self.A.shape[1]:
            raise ValueError("A must be a square matrix")
        if self.b.ndim == 1:
            if self.b.shape[0] != self.A.shape[0]:
                raise ValueError("b must have compatible dimensions with A")
        else:
            self.b = self.b.ravel()
            if self.b.shape[0] != self.A.shape[0]:
                raise ValueError("b must have compatible dimensions with A")
        if x0 is None:
            x0 = np.zeros_like(self.b, dtype=float)
            
        self.x0 = np.asarray(x0, dtype=float)
        self.tol = tol
        self.max_iter = int(max_iter)

    @staticmethod
    def err_rel(x_new, x_old):
        err = np.linalg.norm(x_new - x_old)
        denom = np.linalg.norm(x_old)
        if denom != 0:
            err /= denom
        return err

    def jacobi(self, x0=None, tol=None, max_iter=None):
        A = self.A
        b = self.b
        x = self.x0 if x0 is None else np.asarray(x0, dtype=float)
        tol = self.tol if tol is None else tol
        max_iter = self.max_iter if max_iter is None else int(max_iter)

        d = np.diag(A)
        if np.any(d == 0):
            raise np.linalg.LinAlgError("Zero on diagonal — Jacobi not applicable")
        D_inv = 1.0 / d
        D = np.diag(d)
        R = A - D 

        for _ in range(max_iter):
            x_new = D_inv * (b - R.dot(x))
            if self.err_rel(x_new, x) < tol:
                return x_new
            x = x_new
        return x

    def gauss_seidel(self, x0=None, tol=None, max_iter=None):
        A = self.A
        b = self.b
        x = self.x0 if x0 is None else np.asarray(x0, dtype=float)
        tol = self.tol if tol is None else tol
        max_iter = self.max_iter if max_iter is None else int(max_iter)

        L = np.tril(A)  # includes diagonal
        U = A - L

        for _ in range(max_iter):
            rhs = b - U.dot(x)
            # solve L x_new = rhs
            x_new = np.linalg.solve(L, rhs)
            if self.err_rel(x_new, x) < tol:
                return x_new
            x = x_new
        return x

    def sor(self, omega=1.25, x0=None, tol=1e-6, max_iter=1e12):
        A = self.A
        b = self.b
        x = self.x0 if x0 is None else np.asarray(x0, dtype=float)
        tol = self.tol if tol is None else tol
        max_iter = self.max_iter if max_iter is None else int(max_iter)

        D = np.diagflat(np.diag(A))
        L = np.tril(A, -1)  
        U = np.triu(A, 1)  

        M = D + omega * L
        for _ in range(max_iter):
            rhs = ((1 - omega) * D - omega * U).dot(x) + omega * b
            x_new = np.linalg.solve(M, rhs)
            if self.err_rel(x_new, x) < tol:
                return x_new
            x = x_new
        return x

