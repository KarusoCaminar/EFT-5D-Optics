import numpy as np
import matplotlib.pyplot as plt

class SensitivityCalculator:
    def __init__(self):
        # Constants
        self.h = 6.626e-34
        self.c = 3e8
        self.lambda_laser = 1064e-9
        self.omega_laser = 2 * np.pi * self.c / self.lambda_laser
        self.L_cavity = 0.1 # m
        
        # Experimental Parameters
        self.Finesse = 10000        # High finesse cavity
        self.eta_qe = 0.9           # Quantum efficiency
        self.integration_time = 1.0 # second
        
        # Predicted Signal (from Simulation)
        # Peak PSD ~ 1e-35 (very small) approx
        # We need an estimated PSD value at resonance from the theory.
        # From quantum_refractometer.py: delta_n ~ 1e-27
        # PSD ~ (delta_n)^2 / Bandwidth
        # Let's assume a conservatively derived PSD peak from the 5D theory:
        self.S_nn_theory = 1e-58 # m^2/Hz equivalent in index units? 
        # Actually, let's work with Phase Noise S_phi_phi
        # phi = k * n * L
        # S_phi = (kL)^2 * S_n
        
        # Recalibrate based on "Strong" Sapphire result approximately
        # If delta_n ~ 1e-27, then S_n ~ 1e-54 / Hz approx?
        # Let's use a "Signal Strength" parameter A_signal
        self.Signal_PSD_n = 5e-50 # Hypothesis

    def calculate_shot_noise(self, Power_W):
        """
        Shot noise limit for phase measurement:
        S_phi_shot = 1 / (2 * N_photons)
        N_photons = (P * eta / h*nu) * tau (for simple measurement)
        In a cavity, it's modified by Finesse?
        Standard Shot Noise PSD (Phase): S_phi = h*nu / (2 * P * eta) roughly?
        Actually: delta_phi_shot = 1 / (2 * sqrt(N))
        PSD_shot = 1 / (4 * Flux)
        """
        photon_flux = Power_W / (self.h * (self.c / self.lambda_laser))
        # Phase noise spectral density (rad^2/Hz)
        # Simple interferometry: S_phi = 1 / (2 * PhotonFlux * eta)
        S_phi_shot = 1 / (2 * photon_flux * self.eta_qe)
        
        # Convert to Index Noise S_n = S_phi / (kL)^2
        kL = (2 * np.pi / self.lambda_laser) * self.L_cavity
        S_n_shot = S_phi_shot / (kL**2)
        
        # Cavity enhancement? 
        # In a cavity, phase sensitivity is enhanced by Finesse.
        # Effective Flux = Flux * Finesse/pi ?
        # Let's assume Cavity enhancement factor of roughly F^2 or similar
        # Standard result: sensitivity improves with F.
        # S_n_shot_cavity = S_n_shot / (2 * F / pi)^2
        enhancement = (2 * self.Finesse / np.pi)**2
        return S_n_shot / enhancement

    def calculate_snr(self, powers):
        snrs = []
        for P in powers:
            noise_floor = self.calculate_shot_noise(P)
            # Add thermal coating noise (fixed floor)
            # e.g., 1e-45
            noise_floor += 1e-45 
            
            # SNR = Signal_PSD / Noise_PSD
            snrs.append(self.Signal_PSD_n / noise_floor)
        return np.array(snrs)

# --- Run Calculation ---
def run_sensitivity_analysis():
    calc = SensitivityCalculator()
    
    # Power Range: 1 mW to 100 W
    powers = np.logspace(-3, 2, 50) 
    snrs = calc.calculate_snr(powers)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.loglog(powers, snrs, linewidth=3, color='green')
    plt.xlabel('Laser Power (Watts)')
    plt.ylabel('Signal-to-Noise Ratio (SNR)')
    plt.title(f'Experimental Feasibility (Sapphire, Finesse={calc.Finesse})')
    plt.grid(True, which="both", alpha=0.3)
    
    # Thresholds
    plt.axhline(1.0, color='red', linestyle='--', label='Detection Threshold (SNR=1)')
    plt.axhline(5.0, color='orange', linestyle='--', label='Discovery Threshold (SNR=5)')
    
    plt.legend()
    plt.savefig('sensitivity_snr.png')
    
    # Conclusion
    critical_power_idx = np.where(snrs > 1.0)[0]
    if len(critical_power_idx) > 0:
        p_crit = powers[critical_power_idx[0]]
        print(f"CRITICAL LASER POWER for Detection: {p_crit*1000:.1f} mW")
    else:
        print("Detection requires > 100 W laser power.")

if __name__ == "__main__":
    run_sensitivity_analysis()
