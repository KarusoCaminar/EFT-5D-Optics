import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Robust Import for PhysicsEngine
# If running as script, 'modules' might not be in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.physics_engine import PhysicsEngine

# --- 1. Physik-Engine Integration ---
# Calculate Spectrum from Universal Theory (V4.2)
ENGINE = PhysicsEngine()

# We analyze Sapphire as the reference case
# n = 1.77
n_sapphire = 1.77
# Calculate Ground Mass m1 via Scaling Factor K
m1_eV = ENGINE.SCALING_FACTOR_K * (n_sapphire**2) 
# Result should be approx 63.5 * 1.77^2 = 198.9 eV (Updated from old 229 eV)

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
    print("--- Kaluza-Klein Spectrum Analysis (Universal V4.2) ---")
    print(f"Base Mass m1 (Sapphire n={n_sapphire}): {m1_eV:.2f} eV")
    
    # --- 2. Berechnung ---
    tower = calculate_kk_tower(6)
    
    # Wir schauen uns an, wie schnell ein Teilchen der Mode n=1 ist, 
    # wenn wir ihm verschiedene Energien geben.
    energies_scan = np.linspace(int(m1_eV), 1000, 500) # eV
    velocities_n1 = [relativistic_velocity(e, m1_eV) for e in energies_scan]
    velocities_n2 = [relativistic_velocity(e, m1_eV * 2) for e in energies_scan]
    
    # --- 3. Visualisierung ---
    plt.figure(figsize=(12, 6))
    
    # Plotting the Tower
    plt.subplot(1, 2, 1) # Keep subplot for consistency with the second plot
    
    ns = [x[0] for x in tower]
    ms = [x[1] for x in tower]
    
    # Plot levels
    for n_idx, energy in enumerate(ms):
        mode_label = n_idx + 1
        label_text = f"Mode {mode_label}"
        color = 'blue'
        
        if mode_label == 1:
            label_text = f"EFT Cutoff $\Lambda$ ({energy:.1f} eV)"
            color = 'red'
        elif mode_label == 2:
            label_text = f"2nd Harmonic ({energy:.1f} eV)"
        
        plt.hlines(energy, 0, 1, colors=color, linestyles='solid', linewidth=2)
        plt.text(1.02, energy, label_text, verticalalignment='center', fontsize=10, color=color)

    plt.title(f"V4.3 Prediction: 5D-EFT Energy Scales (Sapphire)\n$\Lambda \approx {m1_eV:.1f}$ eV (Validity Limit)", fontsize=12)
    plt.ylabel("Energy (eV)")
    plt.xlabel("Topological Mode Index")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xticks([]) # Hide x-axis ticks
    plt.xlim(0, 1.3)
    
    # Annotation for experimentalists
    plt.text(0.1, ms[0] - (ms[1]-ms[0])*0.3, 
             "NOTE: 229 eV is not a resonance,\nbut the model's UV-Cutoff scale.", 
             bbox=dict(facecolor='yellow', alpha=0.2))
    
    print("\n[VORHERSAGE] Predicted Kaluza-Klein Resonances:")
    for n, m in zip(ns, ms):
        # The text for the bar plot is removed as it's replaced by hlines text
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
    os.makedirs("images/plots", exist_ok=True)
    out_path = os.path.join("images", "plots", "kk_tower_spectrum.png")
    plt.savefig(out_path)
    print(f"\nVisual saved to '{out_path}'")
    
    # --- 4. Interpretation ---
    print("\n--- Analyse der 5D-Dynamik ---")
    radius_nm = ENGINE.H_BAR_C / m1_eV 
    print(f"Radius der 5. Dimension (R): {radius_nm:.4f} nm")
    print("Interpretation:")
    print(f"1. Ein Photon mit > {m1_eV:.0f} eV kann den n=1 Modus anregen.")
    print(f"2. Dieser neue Radius passt besser zum Gitter (N ~ 2.0).")
    
    if "--batch" not in sys.argv:
        plt.show()

if __name__ == "__main__":
    run_kk_tower_analysis()
