class Material:
    def __init__(self, name, sigma__tr, sigma_a, mu_0, sigma_f, s, bounds, bound_type):
        """Initialize a Material instance.
        Parameters:
            name (str): Name of the material.
            sigma__tr (float): Transport cross-section.
            sigma_a (float): Absorption cross-section.
            mu_0 (float): Average cosine of the scattering angle.
            sigma_f (float): Fission cross-section.
            s (float): Source term.
            bounds (tuple - float): Spatial bounds of the material. in 2D (x_0, x_1, y_0, y_1).
            bound_type (tuple - boolean): Type of boundary condition. in 2D (true for reflective, false for vacuum) (x_0, x_1, y_0, y_1).
        """
        self.name = name
        self.sigma__tr = sigma__tr
        self.sigma_a = sigma_a 
        self.mu_0 = mu_0
        self.sigma_f = sigma_f
        self.s = s
        self.bounds = bounds
        self.bound_type = bound_type

    # getters
    def get_name(self):
        return self.name
    
    def get_sigma__tr(self):
        return self.sigma__tr
    
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
    
    # setters
    def set_name(self, name):
        self.name = name
    
    def set_sigma__tr(self, sigma__tr):
        self.sigma__tr = sigma__tr

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

    # other methods

    def extrapolated_boundary_parameter(self):
        """Calculate the extrapolated boundary distance based on the transport cross-section.
        Returns:
            float: Extrapolated boundary distance.
        """
        return 0.7104 / self.sigma__tr
    
    def diffusion_coefficient(self):
        """Calculate the diffusion coefficient based on the transport cross-section.
        Returns:
            float: Diffusion coefficient.
        """
        return 1 / (3 * self.sigma__tr)
    
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

        self.set_bounds((x_0, x_1, y_0, y_1))

        return (x_0, x_1, y_0, y_1)