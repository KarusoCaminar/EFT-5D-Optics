import numpy as np
import matplotlib.pyplot as plt

def run_engineering_application():
    print("--- Real-World Engineering Application: 5D Physics Limits ---")
    
    # Constants
    c = 3e8
    epsilon0 = 8.854e-12
    n_sapphire = 1.76
    lambda_laser = 1064e-9 # 1064 nm
    
    # --- Case 1: The Einstein Telescope (Gravitational Waves) ---
    print("\n[Case Study 1] The Einstein Telescope (ET)")
    print("Scenario: Uses cryo-cooled Sapphire Mirrors. Does 5D noise blind the detector?")
    
    # ET Parameters
    L_arm = 10000 # 10 km arm length
    Target_Strain = 1e-25 # Sensitivity goal (extremely small!)
    
    # 5D Noise Calculation
    # From our quantum_refractometer.py, we know the PSD of delta_n at 100 Hz.
    # Let's assume a "Leakage Factor". The 5D noise is at 15 THz (Resonance).
    # But tails of the distribution leak into low frequencies (100 Hz).
    # Since it's a high-Q resonance, the tail is suppressed by (f_low / f_res)^4 for density
    
    f_res = 2.83e15 # 15 THz
    f_gw = 100.0    # 100 Hz (Gravitational Wave freq)
    
    suppression = (f_gw / f_res)**2 # Lorentz oscillator tail amplitude scaling ~ 1/w^2
    
    # Base fluctuation amplitude at resonance (from simulation approx)
    delta_n_peak = 1e-12 # Peak fluctuation
    
    # Effective noise at 100 Hz
    delta_n_100Hz = delta_n_peak * suppression
    
    # Apparent length change due to index noise
    # Signal is delta L / L.
    # If the mirror coating (thickness d ~ 5 um) fluctuates:
    d_coating = 5e-6 
    delta_L_apparent = delta_n_100Hz * d_coating
    
    apparent_strain = delta_L_apparent / L_arm
    
    print(f"5D Resonance Freq:   {f_res:.2e} Hz")
    print(f"Observer Freq (GW):  {f_gw:.1f} Hz")
    print(f"Suppression Factor:  {suppression:.2e}")
    print(f"Noise (delta n):     {delta_n_100Hz:.2e}")
    print(f"Apparent Strain h:   {apparent_strain:.2e}")
    
    if apparent_strain > Target_Strain:
        print("RESULT: CRITICAL. 5D noise masks the gravitational wave.")
    else:
        print("RESULT: PASS. The 5D resonance is too high-frequency to disturb GW detection.")
        print(f"Safety Margin: {Target_Strain / apparent_strain:.1e}x")

    # --- Case 2: High-Power Industrial Laser ---
    print("\n[Case Study 2] High-Power Laser Machining")
    print("Scenario: 10kW Laser focused through a lens. Does Space-Time Elasticity shift the focus?")
    
    # Laser Parameters
    Power = 10000 # 10 kW
    Waist = 50e-6 # 50 micron spot size
    Intensity = Power / (np.pi * Waist**2)
    
    # E-Field Calculation
    # I = 0.5 * c * n * eps0 * E^2
    E_field = np.sqrt(2 * Intensity / (c * n_sapphire * epsilon0))
    
    # 5D Metric Elasticity (Kerr Effect)
    # n2 for Sapphire approx 3e-20 m^2/W
    n2 = 3e-20 
    delta_n_5D = n2 * Intensity
    
    print(f"Laser Intensity:     {Intensity/1e9:.2f} GW/m^2")
    print(f"Electric Field:      {E_field/1e6:.2f} MV/m")
    print(f"5D Index Shift:      {delta_n_5D:.2e}")
    
    # Compare to Thermal Lensing
    # dn/dT approx 1e-5 / K. Delta T easily 10 K.
    delta_n_thermal = 1e-5 * 10
    
    print(f"Thermal Shift:       {delta_n_thermal:.2e}")
    ratio = delta_n_5D / delta_n_thermal
    
    if ratio > 1.0:
        print("RESULT: 5D DOMINATED. Spacetime elasticity is stronger than heat.")
    else:
        print(f"RESULT: THERMAL DOMINATED. Heat is {1/ratio:.1f}x stronger than 5D effects.")
        print("Insight: To measure 5D, you must use PULSED lasers (femtosecond) to avoid heat accumulation.")

    # --- VISUALIZATION ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Plot 1: Frequency Domains (ET Detector)
    freqs = np.logspace(0, 16, 100)
    suppression_curve = (freqs / f_res)**2
    suppression_curve[suppression_curve > 1] = 1
    
    ax1.loglog(freqs, suppression_curve, 'b-', lw=2, label='5D Noise Suppression')
    ax1.axvline(100, color='r', ls='--', label='GW Detection (100 Hz)')
    ax1.axvline(f_res, color='g', ls='--', label=f'5D Resonance ({f_res:.0e} Hz)')
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Relative Noise Amplitude")
    ax1.set_title("Einstein Telescope: Why 5D Noise is Harmless")
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(1, 1e17)
    
    # Plot 2: Laser Intensity vs. Index Shift
    intensities = np.linspace(0, 200, 100)  # GW/m^2
    delta_n_5d = n2 * intensities * 1e9  # Convert GW to W
    delta_n_therm = np.ones_like(intensities) * delta_n_thermal
    
    ax2.semilogy(intensities, delta_n_5d, 'b-', lw=2, label='5D (Kerr) Effect')
    ax2.semilogy(intensities, delta_n_therm, 'r--', lw=2, label='Thermal Effect (10K rise)')
    ax2.set_xlabel("Laser Intensity (GW/m²)")
    ax2.set_ylabel("Index Shift Δn")
    ax2.set_title("High-Power Laser: 5D vs. Thermal Effects")
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    import os
    os.makedirs("images", exist_ok=True)
    plt.savefig("images/engineering_applications.png", dpi=150)
    print(f"\nVisualization saved to images/engineering_applications.png")
    plt.close()

if __name__ == "__main__":
    run_engineering_application()
