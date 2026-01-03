import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

# --- 1. Physics Model: Tensor Coupling ---
# Theory: The scalar field Phi couples to the trace of the Energy-Momentum tensor.
# In a crystal, the refractive index is a tensor n_ij.
# The coupling constant gamma_eff is derived from the susceptibility chi.
# For a uniaxial crystal (Sapphire):
# gamma_o (Ordinary ray) corresponds to n_o
# gamma_e (Extraordinary ray) corresponds to n_e

class BirefringentMaterial:
    def __init__(self, name, n_o_params, n_e_params):
        """
        params: (B1, C1) tuple for the UV resonance
        We calculate gamma_eff separately for O and E axes.
        """
        self.name = name
        
        # Physics Constants
        c = 3e8
        
        # Ordinary Axis (x, y)
        Bo, Co = n_o_params
        lam_o = np.sqrt(Co) * 1e-6
        omega_o = 2 * np.pi * c / lam_o
        self.gamma_o = np.sqrt(Bo) * omega_o
        self.m_Phi_o = omega_o
        
        # Extraordinary Axis (z)
        Be, Ce = n_e_params
        lam_e = np.sqrt(Ce) * 1e-6
        omega_e = 2 * np.pi * c / lam_e
        self.gamma_e = np.sqrt(Be) * omega_e
        self.m_Phi_e = omega_e
        
        # We assume the scalar field mass m_Phi is unique to the material Vacuum manifold
        # But effectively, the coupling probes slightly different "modes" or the effective mass differs.
        # Strict 5D Theory: Mass is m_KaluzaKlein (geometry). It should be isotropic (scalar).
        # We will assume m_Phi is the average, but coupling gamma differs.
        self.m_Phi_mean = (omega_o + omega_e) / 2

# Sapphire Data (approx UV pole)
# Ordinary: B=1.43, C=0.072^2
# Extraordinary: B=1.50, C=0.074^2 (Sapphire is negative unixial n_e < n_o? Check data)
# Actually, let's use the material_parameters.py logic
sapphire = BirefringentMaterial("Sapphire", 
                               n_o_params=(1.431, 0.0726**2), 
                               n_e_params=(1.327, 0.0740**2)) # Hypothetical E-ray data close to O

# --- 2. Simulation Logic ---
def run_tensor_simulation():
    print(f"Initializing Anisotropic Simulation for {sapphire.name}...")
    
    # Scale Factors
    SCALE = 1e30
    fs = 1e17
    T_sim = 5e-14
    N = int(T_sim * fs)
    t = np.linspace(0, T_sim, N)
    
    print(f"Coupling Ratio (E/O): {sapphire.gamma_e / sapphire.gamma_o:.3f}")
    
    # Dynamics (Langevin for Scalar Field Phi)
    # The field itself is isotropic (scalar).
    # d^2phi/dt^2 + ... = noise
    
    gamma_damping = 1e12
    m_phi = sapphire.m_Phi_mean
    
    # Scaled noise
    xi_scaled = np.random.normal(0, 1.0 * SCALE, N)
    
    phi_scaled = np.zeros(N)
    v = 0
    x = 0
    dt = 1/fs
    
    for i in range(1, N):
        acc = xi_scaled[i] - gamma_damping * v - m_phi**2 * x
        v += acc * dt
        x += v * dt
        phi_scaled[i] = x
        
    phi_fluct = phi_scaled / SCALE
    
    # --- 3. Polarization Projection ---
    # The noise in the refractive index delta_n depends on the projection.
    # delta_n_x = gamma_x * phi
    # delta_n_z = gamma_z * phi
    
    delta_n_o = - sapphire.gamma_o * phi_fluct
    delta_n_e = - sapphire.gamma_e * phi_fluct
    
    # --- 4. Analysis ---
    f, Pxx_o = welch(delta_n_o, fs, nperseg=min(1024, N))
    f, Pxx_e = welch(delta_n_e, fs, nperseg=min(1024, N))
    
    # Calculate Ratio Curve
    ratio_curve = Pxx_e / Pxx_o
    
    # --- 5. Visualization ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
    
    # Plot 1: Absolute Noise Power
    ax1.loglog(f, Pxx_o, label='Ordinary Ray (Polarization $\perp$ c)', color='blue')
    ax1.loglog(f, Pxx_e, label='Extraordinary Ray (Polarization $\parallel$ c)', color='orange', linestyle='--')
    ax1.set_title(f'Anisotropic Refractive Noise Spectrum ({sapphire.name})')
    ax1.set_ylabel('PSD ($\delta n^2 / Hz$)')
    ax1.set_xlabel('Frequency (Hz)')
    ax1.legend()
    ax1.grid(True, which="both", alpha=0.3)
    
    # Plot 2: Differential Signal (The "Smoking Gun")
    # If the theory is true, rotating the polarization changes the noise level.
    avg_ratio = np.mean(ratio_curve)
    ax2.plot(f, ratio_curve, color='purple', label=f'Anisotropy Ratio (E/O) ~ {avg_ratio:.2f}')
    ax2.set_title('Polarization Sensitivity ("Smoking Gun" Signal)')
    ax2.set_ylabel('Ratio $PSD_E / PSD_O$')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylim(0.5, 1.5)
    ax2.axhline(1.0, color='black', linestyle=':')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('tensor_simulation_results.png')
    print("Results saved to tensor_simulation_results.png")
    
    print("\n--- Tensor Result ---")
    print(f"Experimental Prediction: Rotating polarization changes noise power by {(1-avg_ratio)*100:.1f}%.")

if __name__ == "__main__":
    run_tensor_simulation()
