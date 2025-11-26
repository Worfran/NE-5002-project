import numpy as np
import matplotlib.pyplot as plt

class Plotter:
    """
    A class to plot the solution of a linear system as a heatmap.
    Usage:
        p = Plotter()
        p.plot_heatmap(solution, n, m, title="Heatmap of Solution")
    """

    def __init__(self):
        pass

    def plot_heatmap(self, solution, n, m, title="Heatmap"):
        """
        Plots a heatmap of the solution vector.

        Parameters:
            solution (ndarray): The solution vector to be reshaped into a matrix.
            n (int): Number of rows in the reshaped matrix.
            m (int): Number of columns in the reshaped matrix.
            title (str): Title of the heatmap.
        """
        # Ensure the solution is a numpy array
        solution = np.asarray(solution)

        # Check if the solution size matches the specified dimensions
        if solution.size != n * m:
            raise ValueError("Solution size does not match the specified dimensions (n x m).")

        # Reshape the solution into an n x m matrix
        solution_matrix = solution.reshape((n, m))

        # Plot the heatmap
        plt.figure(figsize=(8, 6))
        plt.imshow(solution_matrix, cmap='viridis', origin='upper')
        plt.colorbar(label='Value')
        plt.title(title)
        plt.xlabel("Column Index")
        plt.ylabel("Row Index")
        plt.show()