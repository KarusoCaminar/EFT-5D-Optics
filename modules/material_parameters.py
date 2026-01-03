import numpy as np

# Physical Constants
c = 2.99792458e8  # m/s

class Material:
    def __init__(self, name, sellmeier_coeffs, n2_cm2_W=None):
        """
        sellmeier_coeffs: List of (B, C) pairs for the equation:
        n^2 = 1 + sum( B_i * lambda^2 / (lambda^2 - C_i) )
        where C_i has units of um^2.
        
        n2_cm2_W: Nonlinear refractive index in cm^2/W (common unit).
        """
        self.name = name
        self.coeffs = sellmeier_coeffs
        self.n2 = n2_cm2_W # cm^2/W
        
        # Calculated parameters
        self.m_Phi_uv = None
        self.gamma_eff_linear = None
        self.gamma_eff_nonlinear = None
        
        self.analyze_material()
        
    def analyze_material(self):
        # 1. Linear Analysis (Sellmeier)
        # B1, C1 correspond to the UV resonance
        bs, cs = zip(*self.coeffs)
        B1 = bs[0]
        C1 = cs[0] # um^2
        
        lambda_res_m = np.sqrt(C1) * 1e-6 
        omega_res = 2 * np.pi * c / lambda_res_m
        
        self.m_Phi_uv = omega_res
        
        # Linear approximation for coupling: gamma ~ sqrt(B) * m
        # This assumes the entire refractive index comes from the 5D field interaction
        self.gamma_eff_linear = np.sqrt(B1) * omega_res
        
        # 2. Nonlinear Analysis (Kerr Effect)
        # Using the relation: n2 \propto gamma^4 / m^4 (roughly) from the theory
        # In 5D EFT: delta_n = (gamma/m^2) * phi
        # The Kerr nonlinearity relates to the 4-point function. 
        # Heuristic: We use n2 to cross-check gamma.
        
        if self.n2:
            # Conversion to SI (m^2/W)
            n2_si = self.n2 * 1e-4 # cm2 to m2
            
            # Theoretical scaling (Toy Model Relation):
            # n2 ~ (gamma_eff / m_Phi)^4 * (some_factor)
            # Let's define a "Nonlinear Coupling Strength" metric
            # This is purely qualitative for ranking materials based on n2
            
            # We assume stronger n2 -> stronger coupling gamma
            # Scale factor for display
            self.gamma_eff_nonlinear = np.power(n2_si * 1e20, 0.25) * omega_res 
            
    def __repr__(self):
        return f"{self.name}: m={self.m_Phi_uv:.2e}"

# Material Database
# Sellmeier Coefficients (Schott / RefractiveIndex.info)
# n2 values (typical, approx) in 10^-16 cm^2/W

materials = [
    Material("Fused Silica", [
        (0.6961663, 0.0684043**2), 
        (0.4079426, 0.1162414**2), 
        (0.8974794, 9.896161**2)
    ], n2_cm2_W=2.2e-16),
    
    Material("BK7", [
        (1.03961212, 0.00600069867), 
        (0.231792344, 0.0200179144), 
        (1.01046945, 103.560653)
    ], n2_cm2_W=3.4e-16),
    
    Material("Sapphire (Ord)", [
        (1.43134930, 0.0726631**2), 
        (0.65054713, 0.1193242**2), 
        (5.3414021, 18.028251**2)
    ], n2_cm2_W=3.0e-16),
    
    # Diamond (C) - Peter 1923
    # n^2 - 1 = B1 * lam^2 / (lam^2 - C1) ...
    # Simplified single pole for UV (approx)
    # B1 = 4.3356, C1 = 0.106^2 um^2 (106 nm resonance)
    Material("Diamond", [
        (4.3356, 0.106**2),
         # Add dummy terms if needed, or just 1 pole model
         # Many sources use a single UV pole + IR pole
         (0.3306, 175.0**2) 
    ], n2_cm2_W=13.0e-16) 
]

# Analysis Output
print("--- Quantum Refractometer: Material Candidate Analysis ---")
print(f"{'Material':<15} | {'m_Phi (Hz)':<12} | {'Eff. Coupling (Hz)':<18} | {'n2 (cm²/W)':<12} | {'Ranking Score'}")
print("-" * 85)

best_mat = None
max_score = 0

for mat in materials:
    # Frequencies to Hz
    f_res = mat.m_Phi_uv / (2 * np.pi)
    gamma_lin = mat.gamma_eff_linear / (2 * np.pi)
    
    # Heuristic Score: Combination of Linear Strength (B) and Nonlinearity (n2)
    # If the theory holds, high n2 should correlate with observable quantum noise.
    score = mat.gamma_eff_linear * (mat.n2 if mat.n2 else 1e-16) * 1e15
    
    if score > max_score:
        max_score = score
        best_mat = mat
        
    n2_str = f"{mat.n2:.1e}" if mat.n2 else "N/A"
    
    print(f"{mat.name:<15} | {f_res:.2e}   | {gamma_lin:.2e}         | {n2_str:<12} | {score:.2f}")

print("-" * 85)
print(f"WINNER: {best_mat.name}")
print("Reason: Highest combination of resonant coupling and nonlinear susceptibility.")
print(f"Parameter Set for Diamond (if selected): m_Phi={best_mat.m_Phi_uv:.3e}, gamma_eff={best_mat.gamma_eff_linear:.3e}")
