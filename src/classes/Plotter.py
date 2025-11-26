import time
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
        solution_matrix = self.vector_to_matrix(solution, n, m)

        # Check if the solution size matches the specified dimensions
        if solution.size != n * m:
            raise ValueError("Solution size does not match the specified dimensions (n x m).")


        # Plot the heatmap
        plt.figure(figsize=(8, 6))
        plt.imshow(solution_matrix, cmap='viridis', origin='upper')
        plt.colorbar(label='Value')
        plt.title(title)
        plt.xlabel("Column Index")
        plt.ylabel("Row Index")

        # Save files before showing the plot
        timestamp = int(time.time())
        plt.savefig(f"Output/images/solution_heatmap_timestamp_{timestamp}.svg", format='svg')
        np.savetxt(f"Output/data/solution_data_timestamp_{timestamp}.txt", solution_matrix)

        # Show the plot
        plt.show()
    
    def vector_to_matrix(self, vector, n, m):
        """
        Converts a 1D solution vector into a 2D matrix.

        Parameters:
            vector (ndarray): The 1D solution vector.
            n (int): Number of rows in the resulting matrix.
            m (int): Number of columns in the resulting matrix.

        Returns:
            ndarray: The reshaped 2D matrix.
        """
        solution_matrix = np.zeros((n, m))
        vector = np.asarray(vector)
        if vector.size != n * m:
            raise ValueError("Vector size does not match the specified dimensions (n x m).")
        for i in range(n):
            start = i * m
            end = start + m
            solution_matrix[i, :] = vector[start:end]

        return solution_matrix
