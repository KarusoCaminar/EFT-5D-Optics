import numpy as np
import matplotlib.pyplot as plt

def calculate_spatial_physics():
    print("--- Spatial Physics: Beam Averaging Analysis ---")
    
    # Constants
    c = 3e8
    h_bar = 1.054e-34
    
    # 5D Field Parameters (Diamond)
    m_Phi = 1.777e16 # rad/s
    omega_res = m_Phi
    
    # 1. Correlation Length (lambda_c)
    # The size of a "quantum ripple" in the refractive index.
    # From Compton wavelength of the mode mass: lambda = c / f or h_bar / (m*c)
    # Using dispersion relation omega = c*k -> k = omega/c -> lambda = 2pi/k = 2pi*c/omega
    lambda_c = 2 * np.pi * c / omega_res
    
    print(f"5D Resonance Frequency: {omega_res/(2*np.pi):.2e} Hz")
    print(f"Correlation Length (Ripple Size) lambda_c: {lambda_c:.2e} m ({lambda_c*1e9:.1f} nm)")
    
    # 2. Laser Beam Parameters
    # Typical waist radius w0
    beam_waists = np.logspace(-6, -3, 50) # 1 um to 1 mm
    
    # 3. Averaging Factor
    # If the beam area (pi*w0^2) is larger than the correlation area (lambda_c^2),
    # the signal variance scales as 1/N, where N = Area_beam / Area_corr.
    # V_meas = V_point * (A_corr / A_beam)
    # Amplitude signal (sqrt(V)) scales as sqrt(A_corr / A_beam) = lambda_c / w0 approx.
    # Let's compute the reduction factor eta_amplitude.
    
    eta_amplitude = []
    
    for w0 in beam_waists:
        if w0 < lambda_c:
            eta = 1.0 # Point-like sampling
        else:
            # Area ratio N = (w0 / lambda_c)^2
            # Amplitude reduction = 1/w0 * lambda_c (roughly linear dim scaling for Gaussian integrals)
            # Rigorous: 1 / sqrt(1 + (w0/lambda_c)^2) ? 
            # Simple geometric averaging: w0 >> lambda -> factor is lambda_c / w0
            eta = lambda_c / (np.sqrt(np.pi) * w0) 
            
        eta_amplitude.append(eta)
        
    eta_amplitude = np.array(eta_amplitude)
    
    # Plot
    plt.figure(figsize=(10, 6))
    plt.loglog(beam_waists * 1e6, eta_amplitude, linewidth=3, color='crimson')
    plt.xlabel('Laser Beam Waist radius $w_0$ ($\mu m$)')
    plt.ylabel('Signal Amplitude Reduction Factor $\eta_{avg}$')
    plt.title(f'Spatial Averaging (Ripple Size $\lambda_c \\approx {lambda_c*1e9:.1f}$ nm)')
    plt.grid(True, which="both", alpha=0.3)
    
    # Reference points
    plt.axvline(100, color='gray', linestyle='--', label='Standard Fiber Collimator (100 um)')
    plt.axvline(lambda_c*1e6, color='black', linestyle=':', label='Correlation Length')
    
    plt.legend()
    plt.savefig('spatial_averaging.png')
    
    # Conclusion
    # Check 100 um beam
    idx_100um = np.argmin(np.abs(beam_waists - 100e-6))
    factor_100um = eta_amplitude[idx_100um]
    
    print(f"\nAt standard beam size (w0 = 100 um):")
    print(f"Reduction Factor: {factor_100um:.2e}")
    print(f"Loss in dB: {20*np.log10(factor_100um):.1f} dB")
    
    if factor_100um < 1e-4:
        print("\nCRITICAL WARNING: The signal is suppressed by > 80 dB due to spatial averaging.")
        print("Recommendation: You need a nano-focal spot or near-field setup.")
    else:
        print("\nStatus: Averaging is manageable.")

if __name__ == "__main__":
    calculate_spatial_physics()
