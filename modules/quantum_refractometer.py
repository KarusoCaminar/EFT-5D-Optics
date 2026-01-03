import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch

# --- 1. Class for Physical Parameters ---
class PhysicalParameters:
    def __init__(self, temp_k=300):
        # Constants
        self.c = 3e8
        self.hbar = 1.054e-34
        self.kB = 1.38e-23
        self.T = temp_k 
        
        # Real Material Parameters (Sapphire - Ordinary Ray)
        # Derived from material_parameters.py
        self.m_Phi = 2.592e16        # rad/s (~4.1e15 Hz)
        self.gamma_eff = 3.101e16    # Coupling strength
        self.Gamma = 1e12            # Damping (linewidth), kept constant for now
        
        # Simulation Settings
        # Increased Sampling Rate for UV resonance (m_Phi ~ 2.6e16 rad/s => f ~ 4e15 Hz)
        # We need fs >> f_res. 
        self.fs = 1e17               # 100 PHz sampling!
        self.T_sim = 5e-14           # Very short duration (50 femtoseconds)
        
        # Noise Scaling
        # Base Quantum Noise Amplitude (Zero Point Energy equivalent)
        # We assume the "force" normalization matches the ZPE energy.
        self.noise_amp_quantum = 1e-1  # Arbitrary scaling for 'theory' visibility in this model
        
        # Numerical Stability Scaling
        self.SCALE = 1e30            

# --- 2. Simulation Logic ---
def run_simulation():
    print("Initializing Quantum Refractometer Simulation (Temperature Mode)...")
    
    # Temperatures to test
    temperatures = [300, 77, 4, 0]
    colors = {300: 'red', 77: 'orange', 4: 'blue', 0: 'black'}
    labels = {300: '300K (Room)', 77: '77K (LN2)', 4: '4K (LHe)', 0: '0K (Quantum Only)'}
    
    plt.figure(figsize=(10, 8))
    
    for T in temperatures:
        print(f"Simulating T = {T} K...")
        params = PhysicalParameters(temp_k=T)
        
        # Time vector
        N = int(params.T_sim * params.fs)
        # Safety check for memory
        if N > 1e7: 
            print("Warning: N too large, clipping.")
            N = int(1e7)
            
        t = np.linspace(0, params.T_sim, N)
        
        # --- Noise Generation (Thermal + Quantum) ---
        # Fluctuation Dissipation Theorem-ish scaling:
        # Variance ~ coth(hbar*w / 2kT)
        # If T=0, factor=1. If T is large, factor grows.
        
        # Calculate Coth factor for the resonant frequency
        if T == 0:
            therm_factor = 1.0
        else:
            # Argument x = hbar * omega / (2 * kB * T)
            arg = (params.hbar * params.m_Phi) / (2 * params.kB * T)
            # Clip arg to avoid overflow
            if arg > 100: 
                therm_factor = 1.0 # Quantum limit
            elif arg < 1e-4:
                therm_factor = 1.0 / arg # Classical limit 2kT/hw
            else:
                therm_factor = 1.0 / np.tanh(arg) # coth(x)
        
        print(f"  -> Thermal Amplification Factor (Coth): {therm_factor:.2f}")
        
        # Generate Noise
        current_noise_amp = params.noise_amp_quantum * np.sqrt(therm_factor)
        xi_scaled = np.random.normal(0, current_noise_amp * params.SCALE, N)
        
        # --- System Response (Langevin) ---
        phi_scaled = np.zeros(N)
        v_scaled = 0 
        x_scaled = 0 
        dt = 1 / params.fs
        
        for i in range(1, N):
            acc_scaled = xi_scaled[i] - params.Gamma * v_scaled - params.m_Phi**2 * x_scaled
            v_scaled += acc_scaled * dt
            x_scaled += v_scaled * dt
            phi_scaled[i] = x_scaled
            
        # Unscale
        phi_fluct = phi_scaled / params.SCALE
        delta_n = - (params.gamma_eff * phi_fluct)
        
        # --- Spectral Analysis ---
        f, Pxx = welch(delta_n, params.fs, nperseg=min(1024, N))
        
        # Plotting
        plt.loglog(f, Pxx, label=f'{labels[T]} (Factor {therm_factor:.1f})', color=colors[T], linewidth=2 if T==0 else 1)

    # Finalize Plot
    plt.title('Quantum vs Thermal Noise Strategy (Sapphire Crystal)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel(r'PSD ($\delta n^2$/Hz)')
    
    # Mark Resonance
    # resonance is at m_Phi rad/s -> m_Phi / 2pi Hz
    res_freq = 2.592e16 / (2 * np.pi) 
    plt.axvline(x=res_freq, color='green', linestyle=':', label=f'Sapphire Resonance ({res_freq:.1e} Hz)')
    
    plt.legend()
    plt.grid(True, which="both", alpha=0.3)
    
    output_filename = 'quantum_refractometer_temperature.png'
    plt.savefig(output_filename)
    print(f"Simulation Complete. Results saved to {output_filename}")

if __name__ == "__main__":
    run_simulation()
