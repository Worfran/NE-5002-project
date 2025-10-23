import numpy as np
from src.classes.Solvers import Solvers

A = np.array([[4., 3., 0.],
              [3., 4., -1.],
              [0., -1., 4.]])

b = np.array([24., 30., -24.])

x0 = np.array([1., 1., 1.])

omega = 1.25

steps = 4 

fmt = lambda v: f"{v:.6g}"

def run_method(method_name):
    s = Solvers(A, b, x0=x0.copy())
    xs = [s.x0.copy()]
    for _ in range(steps):
        if method_name == "jacobi":
            x = s.jacobi(max_iter=1)
        elif method_name == "gauss_seidel":
            x = s.gauss_seidel(max_iter=1)
        elif method_name == "sor":
            x = s.sor(omega=omega, max_iter=1)
        else:
            raise ValueError(method_name)
        xs.append(x.copy())
        s.x0 = x.copy()
    return xs

x_star = np.linalg.solve(A, b)

def print_table(name, xs):
    print(f"\n{name}")
    print("k  " + "  ".join(str(k) for k in range(len(xs))))
    for i in range(len(xs[0])):
        print(f"x{i+1}  " + "  ".join(fmt(xs[k][i]) for k in range(len(xs))))
    x4 = xs[4]
    comp_err = np.abs(x4 - x_star)
    print("error |x^(4)-x*|  " + "  ".join(fmt(v) for v in comp_err) + f"   inf-norm={fmt(np.max(comp_err))}")

for name in ("jacobi", "gauss_seidel", "sor"):
    xs = run_method(name)
    print_table(name, xs)

print("\nExact solution x*  " + "  ".join(fmt(v) for v in x_star))