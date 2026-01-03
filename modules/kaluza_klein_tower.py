import numpy as np
import matplotlib.pyplot as plt
import sys

# --- 1. Physik-Engine ---
# Basis-Werte aus unserer Theorie (Dispersion Validator Result)
m1_eV = 229.40 # Grundmasse aus Saphir-Fit (n=1)
c = 3e8        # Lichtgeschwindigkeit

def calculate_kk_tower(max_n=5):
    modes = []
    for n in range(1, max_n + 1):
        mass_eV = n * m1_eV
        modes.append((n, mass_eV))
    return modes

def relativistic_velocity(energy_total_eV, rest_mass_eV):
    # E_total = gamma * m * c^2
    # v = c * sqrt(1 - (mc^2 / E)^2)
    if energy_total_eV < rest_mass_eV:
        return 0.0 # Existiert nicht (Tunneln oder virtuell)
    
    term = (rest_mass_eV / energy_total_eV)**2
    beta = np.sqrt(1 - term)
    return beta # in Einheiten von c

def run_kk_tower_analysis():
    print("--- Kaluza-Klein Spectrum Analysis ---")
    
    # --- 2. Berechnung ---
    tower = calculate_kk_tower(6)
    
    # Wir schauen uns an, wie schnell ein Teilchen der Mode n=1 ist, 
    # wenn wir ihm verschiedene Energien geben.
    energies_scan = np.linspace(229, 1000, 500) # eV
    velocities_n1 = [relativistic_velocity(e, m1_eV) for e in energies_scan]
    velocities_n2 = [relativistic_velocity(e, m1_eV * 2) for e in energies_scan]
    
    # --- 3. Visualisierung ---
    plt.figure(figsize=(12, 6))
    
    # Plot 1: Der Turm (Spektrum)
    plt.subplot(1, 2, 1)
    ns = [x[0] for x in tower]
    ms = [x[1] for x in tower]
    bars = plt.bar(ns, ms, color='darkblue', alpha=0.7)
    plt.title("Der Kaluza-Klein Turm (Saphir)\nVorhersage für Absorptions-Linien", fontsize=12)
    plt.xlabel("Mode $n$ (Quantenzahl)")
    plt.ylabel("Effektive Masse / Energie (eV)")
    plt.grid(True, axis='y', alpha=0.3)
    
    print("\n[VORHERSAGE] Predicted Kaluza-Klein Resonances:")
    for n, m in zip(ns, ms):
        plt.text(n, m + 15, f"{m:.0f} eV", ha='center', fontweight='bold', fontsize=9)
        print(f"Mode n={n}: {m:.1f} eV")
    
    # Plot 2: Einstein & Geschwindigkeit
    plt.subplot(1, 2, 2)
    plt.plot(energies_scan, velocities_n1, 'r-', linewidth=2, label=f'Mode n=1 ({m1_eV:.0f} eV)')
    plt.plot(energies_scan, velocities_n2, 'b--', linewidth=2, label=f'Mode n=2 ({m1_eV*2:.0f} eV)')
    plt.axhline(1.0, color='k', linestyle=':', label='Lichtgeschwindigkeit c')
    plt.title("Relativistische Geschwindigkeit in 3D\n(Masse = 5D Rotation)", fontsize=12)
    plt.xlabel("Gesamtenergie des Teilchens (eV)")
    plt.ylabel("Geschwindigkeit ($v/c$)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('kk_tower_spectrum.png')
    print("\nVisual saved to 'kk_tower_spectrum.png'")
    
    # --- 4. Interpretation ---
    print("\n--- Analyse der 5D-Dynamik ---")
    # hbar * c approx 197.3 eV nm
    radius_nm = 197.3 / m1_eV 
    print(f"Radius der 5. Dimension (R): {radius_nm:.2f} nm (aus h_bar*c / m1)")
    print("Interpretation:")
    print(f"1. Ein Photon mit 300 eV (mehr als {m1_eV:.0f} eV) kann den n=1 Modus anregen.")
    v_300 = relativistic_velocity(300, m1_eV)
    print(f"   Es würde sich dann nur noch mit {v_300*100:.1f}% Lichtgeschwindigkeit bewegen.")
    print(f"2. Ein Photon mit 1000 eV (Röntgen) kann sogar den n=2 Modus anregen.")
    print("3. Diese 'Verlangsamung' durch Anregung der 5. Dimension IST die Brechung.")
    
    if "--batch" not in sys.argv:
        plt.show()

if __name__ == "__main__":
    run_kk_tower_analysis()
