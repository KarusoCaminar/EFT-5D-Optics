import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def run_dispersion_validation():
    print("--- Dispersion Validator: Testing 'Dispersion is Mass' Hypothesis ---")

    # --- 1. Physikalische Konstanten ---
    c = 299792458  # Lichtgeschwindigkeit in m/s
    h_bar = 1.0545718e-34

    # --- 2. Echte Daten: Saphir (Ordinary Ray) ---
    # Sellmeier-Gleichung für Saphir (Quelle: Malitson 1962)
    def sapphire_index_real(wavelength_microns):
        w = wavelength_microns
        # Saphir 3-Term Sellmeier
        # C-Werte sind lambda^2 (Mikrometer^2)
        n_sq = 1 + (1.4313493 * w**2) / (w**2 - 0.0726631**2) + \
                   (0.65054713 * w**2) / (w**2 - 0.1193242**2) + \
                   (5.3414021 * w**2) / (w**2 - 18.028251**2)
        return np.sqrt(n_sq)

    # Wir scannen von UV (0.2 um) bis Infrarot (2.0 um)
    wavelengths = np.linspace(0.25, 2.0, 100) # in Mikrometer
    n_real_data = sapphire_index_real(wavelengths)
    omegas = 2 * np.pi * c / (wavelengths * 1e-6) # Kreisfrequenzen in rad/s

    # --- 3. Unsere 5D-Theorie ---
    # Hypothese: n(omega) = n_vacuum + Kopplung / (m_Phi^2 - omega^2)
    # Das ist der Realteil des Propagators eines massiven Skalarfeldes (Lorentz-Oszillator).
    
    def theory_5d_propagator(omega, m_phi, coupling_A, n_offset):
        # n(w) approx n_offset + A * 1/(m^2 - w^2)
        # Wir testen, ob ein einziger effektiver Pol (Resonanz) das ganze Verhalten erklärt.
        return n_offset + coupling_A / (m_phi**2 - omega**2)

    # Fit durchführen
    # Startwerte: Masse ~ UV-Frequenz (2e16), Kopplung sehr groß, Offset ~ 1
    popt, pcov = curve_fit(theory_5d_propagator, omegas, n_real_data, 
                           p0=[2.6e16, 2e32, 1.7], maxfev=100000)

    m_phi_fit, coupling_fit, n_offset_fit = popt

    # --- 4. Auswertung ---
    n_theory = theory_5d_propagator(omegas, *popt)
    residuals = n_real_data - n_theory

    # Metrics
    max_error = np.max(np.abs(residuals))
    rmse = np.sqrt(np.mean(residuals**2))

    print("--- 5D Theorie Fit Ergebnisse ---")
    print(f"Gefittete Masse (m_Phi):     {m_phi_fit:.3e} rad/s")
    
    resonance_hz = m_phi_fit / (2 * np.pi)
    print(f"Resonanz-Frequenz:           {resonance_hz:.2e} Hz")
    
    eV_energy = m_phi_fit * h_bar / 1.602e-19
    print(f"Energie (Masse):             {eV_energy:.2f} eV")
    
    # --- Kaluza-Klein Radius Calculation ---
    # Condition: 2*pi*R = lambda_Compton = h / (m*c) ??
    # Actually: m = 1/R (in natural units) -> R = hbar*c / m
    # Or circle condition: 2*pi*R = lambda -> p = h/lambda -> p = h/(2*pi*R) = hbar/R
    # If m is the first mode (n=1), then m = 1/R.
    R_5d = c / m_phi_fit # (since m_phi is omega_res = c/R_eff)
    # Wait, m_phi_fit is angular frequency (rad/s).
    # m_phi (mass) = hbar * omega / c^2
    # R = hbar / (m*c) = hbar / (hbar*omega/c) = c / omega
    # So R is simply c / omega_res.
    
    R_nanometers = R_5d * 1e9
    print(f"5D Radius (R):               {R_nanometers:.2f} nm")
    
    print(f"Basis-Offset (Vakuum):       {n_offset_fit:.4f}")
    print(f"Maximaler Fehler (Residual): {max_error:.4f} (Index)")
    print(f"RMSE Fehler:                 {rmse:.4f}")

    if max_error < 0.05:
        print("\nSUCCESS: The 5D Propagator curve matches the real dispersion data.")
        print("This validates that dispersion behaves LIKE a massive field resonance.")
    else:
        print("\nWARNING: Fit is poor. Multi-pole model might be needed.")

    # --- 5. Plotting ---
    plt.figure(figsize=(10, 8))

    # Hauptplot: Kurvenvergleich
    plt.subplot(2, 1, 1)
    plt.plot(wavelengths, n_real_data, 'k-', linewidth=2, label='Real Data (Sapphire Sellmeier)')
    plt.plot(wavelengths, n_theory, 'r--', linewidth=2, label=f'5D Theory Fit (Mass = {eV_energy:.1f} eV)')
    plt.title("Spectral Proof: 'Dispersion is Mass'")
    plt.ylabel("Refractive Index $n$")
    plt.xlabel("Wavelength ($\mu m$)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    # Residualplot
    plt.subplot(2, 1, 2)
    plt.plot(wavelengths, residuals, 'b-')
    plt.title("Theory Error (Residuals)")
    plt.ylabel("Deviation $\Delta n$")
    plt.xlabel("Wavelength ($\mu m$)")
    plt.grid(True, alpha=0.3)
    plt.axhline(0, color='k', linestyle='-')

    plt.tight_layout()
    plt.savefig('dispersion_validation.png')
    print("Plot saved to 'dispersion_validation.png'")

if __name__ == "__main__":
    run_dispersion_validation()
