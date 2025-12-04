import time
from src.classes.Material import Material
from src.classes.Mesh_constructor import Mesh_constructor
from src.classes.Matrix_constructor import Matrix_constructor
from src.classes.Solvers import Solvers
from src.classes.Reader import DocumentReader
from src.classes.Plotter import Plotter
import numpy as np

class ProblemModel:
    def __init__(self):
        self.materials = []
        self.mesh = None
        self.matrix_constructor = None
        self.solver = None

    def create_materials_from_file(self, file_path):
        reader = DocumentReader(file_path)
        reader.read_file()
        reader.parse_materials()
        self.materials = reader.get_materials()

    def create_materials_manually(self, materials_data):
        self.materials = [
            Material(
                name=data["name"],
                sigma_s=data["sigma_s"],
                sigma_a=data["sigma_a"],
                mu_0=data["mu_0"],
                sigma_f=data["sigma_f"],
                s=data["s"],
                bounds=data["bounds"],
                bound_type=data["bound_type"]
            )
            for data in materials_data
        ]

    def create_mesh(self, ncells_x, ncells_y):
        self.mesh = Mesh_constructor(ncells_x, ncells_y, self.materials)
        self.mesh.compute_extrapolated_boundaries_y()
        self.mesh.compute_extrapolated_boundaries_x()
        self.mesh.compute_total_size()
        self.mesh.compute_cell_sizes()
        self.mesh.create_material_matrices()

    def create_matrix(self):
        if not self.mesh:
            raise ValueError("Mesh must be created before constructing the matrix.")
        self.matrix_constructor = Matrix_constructor(
            self.mesh.ncells_x,
            self.mesh.ncells_y,
            self.mesh.Dcells,
            self.mesh.Sigma_acells,
            self.mesh.source_cells,
            self.mesh.dx,
            self.mesh.dy,
            self.materials,
            self.mesh.interfaces_x
        )
        np.savetxt(f"Output/data/matrix_A.txt-timestamp_{int(time.time())}", self.matrix_constructor.A)
        np.savetxt(f"Output/data/vector_b.txt-timestamp_{int(time.time())}", self.matrix_constructor.b)


    def solve(self, method="sor", omega=1.25, max_iter=1000):
        if not self.matrix_constructor:
            raise ValueError("Matrix must be created before solving.")
        A = self.matrix_constructor.A
        b = self.matrix_constructor.b
        x0 = [0] * len(b)
        self.solver = Solvers(A, b, x0=x0, max_iter=max_iter)
        if method == "jacobi":
            return self.solver.jacobi()
        elif method == "gauss_seidel":
            return self.solver.gauss_seidel()
        elif method == "sor":
            return self.solver.sor(omega=omega)
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def plot_solution(self, solution):
        if not self.mesh:
            raise ValueError("Mesh must be created before plotting the solution.")
        plotter = Plotter()
        plotter.plot_heatmap(
            solution,
            n=self.mesh.ncells_y,
            m=self.mesh.ncells_x,
            dx=self.mesh.dx,
            dy=self.mesh.dy,
            title="Scalar flux",
            flux_units="n/cm$^2$/s"
        )

    
    