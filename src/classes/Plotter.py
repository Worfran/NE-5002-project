import time
import numpy as np
import matplotlib.pyplot as plt

class Plotter:
    """
    Plot the solution of a linear system as a heatmap.
    """

    def __init__(self):
        pass

    def plot_heatmap(self, solution, n, m,
                    dx=1.0, dy=1.0,
                    title="Heatmap",
                    flux_units=""):

        solution = np.asarray(solution)
        if solution.size != n * m:
            raise ValueError(
                f"Solution size ({solution.size}) does not match n*m = {n*m}."
            )

        solution_matrix = self.vector_to_matrix(solution, n, m)

        # Use constrained_layout to avoid overlaps
        fig, ax = plt.subplots(constrained_layout=True)  # Enable constrained layout

        # Heatmap
        im = ax.imshow(
            solution_matrix,
            cmap='viridis',
            origin='lower',
            extent=[-0.5, m - 0.5, -0.5, n - 0.5],
            aspect='auto'
        )

        ax.set_xlabel("Cell index (x)")
        ax.set_ylabel("Cell index (y)")
        ax.set_title(title)

        # Adjust ticks to avoid overlap
        ax.set_xticks(np.arange(0, m, max(1, m // 10)))  
        ax.set_yticks(np.arange(0, n, max(1, n // 10))) 
        ax.tick_params(axis='x', rotation=45)  

        cbar = fig.colorbar(im, ax=ax, pad=0.1)  
        if flux_units:
            cbar.set_label(f"Flux [{flux_units}]")
        else:
            cbar.set_label("Flux")

        # --- Secondary axes in physical coordinates ---
        def idx_to_xcm(j): return (j + 0.5) * dx
        def xcm_to_idx(x): return x / dx - 0.5
        def idx_to_ycm(i): return (i + 0.5) * dy
        def ycm_to_idx(y): return y / dy - 0.5

        secax_x = ax.secondary_xaxis('top', functions=(idx_to_xcm, xcm_to_idx))
        secax_y = ax.secondary_yaxis('right', functions=(idx_to_ycm, ycm_to_idx))

        secax_x.set_xlabel("x (cm)", labelpad=5)
        secax_y.set_ylabel("y (cm)", labelpad=5)

        # Save
        timestamp = int(time.time())
        fig.savefig(
            f"output/images/solution_heatmap_timestamp_{timestamp}.svg",
            format='svg',
            bbox_inches='tight'
        )
        np.savetxt(
            f"output/data/solution_data_timestamp_{timestamp}.txt",
            solution_matrix
        )

        plt.show()


    def vector_to_matrix(self, vector, n, m):
        """
        Converts a 1D solution vector into a 2D matrix (row-major).

        Parameters:
            vector (ndarray): The 1D solution vector.
            n (int): Number of rows in the resulting matrix.
            m (int): Number of columns in the resulting matrix.

        Returns:
            ndarray: The reshaped 2D matrix of shape (n, m).
        """
        vector = np.asarray(vector)
        if vector.size != n * m:
            raise ValueError(
                f"Vector size ({vector.size}) does not match n*m = {n*m}."
            )
        solution_matrix = np.zeros((n, m))
        for i in range(n):
            start = i * m
            end = start + m
            solution_matrix[i, :] = vector[start:end]
        return solution_matrix