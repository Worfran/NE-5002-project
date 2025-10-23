class Material:
    
    def __init__(self, name, sigma_s, sigma_a, mu_0, sigma_f, s, bounds, bound_type):
        """Initialize a Material instance.
        Parameters:
            name (str): Name of the material.
            sigma__s (float): Transport cross-section.
            sigma_a (float): Absorption cross-section.
            mu_0 (float): Average cosine of the scattering angle.
            sigma_f (float): Fission cross-section.
            s (float): Source term.
            bounds (tuple - float): Spatial bounds of the material. in 2D (x_0, x_1, y_0, y_1).
            bound_type (tuple - boolean): Type of boundary condition. in 2D (true for reflective, false for vacuum) (x_0, x_1, y_0, y_1).
        """
        self.name = name
        self.sigma_s = sigma_s
        self.sigma_a = sigma_a
        self.mu_0 = mu_0
        self.sigma_f = sigma_f
        self.s = s
        self.bounds = bounds
        self.bound_type = bound_type
        self.sigma_tr = None

    # getters
    def get_name(self):
        return self.name
    
    def get_sigma_s(self):
        return self.sigma_s
    
    def get_sigma_a(self):
        return self.sigma_a
    
    def get_mu_0(self):
        return self.mu_0
    
    def get_sigma_f(self):
        return self.sigma_f
    
    def get_s(self):
        return self.s
    
    def get_bounds(self):
        return self.bounds
    
    def get_bound_type(self):
        return self.bound_type
    
    def get_sigma_tr(self):
        """Calculate the transport cross-section.
        Returns:
            float: Transport cross-section.
        """
        return self.sigma__tr
    
    # setters
    def set_name(self, name):
        self.name = name
    
    def set_sigma_s(self, sigma__s):
        self.sigma__s = sigma__s

    def set_sigma_a(self, sigma_a):
        self.sigma_a = sigma_a

    def set_mu_0(self, mu_0):
        self.mu_0 = mu_0

    def set_sigma_f(self, sigma_f):
        self.sigma_f = sigma_f

    def set_s(self, s):
        self.s = s

    def set_bounds(self, bounds):
        self.bounds = bounds

    def set_bound_type(self, bound_type):
        self.bound_type = bound_type

    def set_sigma_tr(self, sigma_tr):
        self.sigma_tr = sigma_tr

    # other methods

    def compute_sigma_tr(self):
        """Compute the transport cross-section based on absorption cross-section and average cosine of the scattering angle.
        Returns:
            float: Transport cross-section.
        """
        if self.sigma_s is None or self.sigma_a is None or self.mu_0 is None:
            raise ValueError("sigma_s, sigma_a, and mu_0 must be set to compute sigma_tr.")
        self.sigma_tr = self.sigma_a + (1 - self.mu_0) * self.sigma_s
        return self.sigma_tr

    def extrapolated_boundary_parameter(self):
        """Calculate the extrapolated boundary distance based on the transport cross-section.
        Returns:
            float: Extrapolated boundary distance.
        """
        return 0.7104 / self.sigma__s
    
    def diffusion_coefficient(self):
        """Calculate the diffusion coefficient based on the transport cross-section.
        Returns:
            float: Diffusion coefficient.
        """
        return 1 / (3 * self.sigma__s)
    
    def solution_bounds(self):
        """Get the solution bounds adjusted for extrapolated boundary conditions.
        Returns:
            tuple - float: Adjusted solution bounds in 2D (x_0, x_1, y_0, y_1).
        """
        d = self.extrapolated_boundary_parameter()
        x_0, x_1, y_0, y_1 = self.bounds

        tx_0, tx_1, ty_0, ty_1 = self.bound_type

        if not tx_0:
            x_0 -= d
        if not tx_1:
            x_1 += d
        if not ty_0:
            y_0 -= d
        if not ty_1:
            y_1 += d

        return (x_0, x_1, y_0, y_1)