import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

# Robust Import for PhysicsEngine (Add Root to Path)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.physics_engine import PhysicsEngine

"""
Module: material_scanner.py
Zweck: Scannt reale Materialdatenbanken nach 5D-Resonanzen.
Theorie: Ein Material ist stabil/besonders, wenn R_5D / a_Gitter approx Integer (Ganzzahl).
         R_5D = h_bar * c / m_eff. m_eff wird aus dem Brechungsindex n abgeleitet.
"""

# Konstanten
# H_BAR_C = 197.3269804 # eV * nm (Now available in Engine, but keeping local copy or using Engine's?)
# Let's use Engine's to be 100% consistent.
ENGINE = PhysicsEngine()

def calculate_5d_resonance(name, n_index, lattice_a_nm):
    """
    Berechnet die 5D-Metriken für ein gegebenes Material.
    """
    # 1. Berechne effektive Masse aus Brechungsindex (Heuristik)
    # Uses Universal Calibration K
    m_eff_ev = ENGINE.SCALING_FACTOR_K * (n_index**2)
    
    # 2. Berechne 5D-Radius R (Compton-Wellenlänge der Masse)
    # R = hbar*c / m
    if m_eff_ev == 0: return 0, 0, 0
    R_5d_nm = ENGINE.H_BAR_C / m_eff_ev
    
    # 3. Berechne Resonanz-Faktor N
    # N = R / a (oder a / R, je nach Definition. Wir nutzen R/a wie im Bericht)
    resonance_ratio = R_5d_nm / lattice_a_nm
    
    return m_eff_ev, R_5d_nm, resonance_ratio

def run_material_scan():
    print("--- 5D-Optics Universal Material Scanner ---")
    print(f"Calibration: K={ENGINE.SCALING_FACTOR_K} (Silicon Gauge)")
    print("Scanning database for geometric resonances...")
    
    # Echte Materialdaten (Beispiele aus Datenbanken wie Materials Project / RefractiveIndex.info)
    # Format: [Name, Brechungsindex n (bei 589nm), Gitterkonstante a (nm)]
    database = [
        ["Vacuum", 1.00, 100.0], # Dummy
        ["Sapphire (Al2O3)", 1.77, 0.476],
        ["Diamond (C)", 2.42, 0.357],
        ["Silicon (Si)", 3.42, 0.543],
        ["Quartz (SiO2)", 1.54, 0.491],
        ["Salt (NaCl)", 1.54, 0.564],
        ["Gallium Arsenide", 3.30, 0.565],
        ["Germanium (Ge)", 4.00, 0.566],
        ["Ice (H2O)", 1.31, 0.452] 
    ]
    
    results = []
    
    print(f"{'Material':<20} | {'n':<6} | {'a (nm)':<8} | {'R_5D (nm)':<10} | {'Ratio (N)':<10} | {'Qualität'}")
    print("-" * 90)
    
    for mat in database:
        name, n, a = mat
        if name == "Vacuum": continue
        
        m, R, N = calculate_5d_resonance(name, n, a)
        
        # Bewertung der Resonanz (Wie nah ist N an einer ganzen Zahl?)
        # Wir suchen N = 1.0, 2.0, 3.0, 4.0 ...
        deviation = abs(N - round(N))
        quality = "---"
        if deviation < 0.15: quality = "HIT! *"
        if deviation < 0.05: quality = "PERFECT **"
        
        print(f"{name:<20} | {n:<6.2f} | {a:<8.3f} | {R:<10.4f} | {N:<10.3f} | {quality}")
        results.append({'name': name, 'N': N})

    # Visualisierung
    names = [r['name'] for r in results]
    Ns = [r['N'] for r in results]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(names, Ns, color='skyblue', edgecolor='black')
    
    # Markiere ganzzahlige Linien (Resonanz-Ziele)
    for i in range(1, 6):
        plt.axhline(i, color='red', linestyle='--', alpha=0.3)
        plt.text(-0.5, i, f"Harmonic N={i}", color='red', fontsize=8)
        
    plt.title("Suche nach 5D-Resonanzen in realen Materialien", fontsize=14)
    plt.ylabel("Geometrisches Verhältnis R_5D / a_Lattice")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    
    # Highlight Hits
    for bar, N in zip(bars, Ns):
        if abs(N - round(N)) < 0.15:
            bar.set_color('gold')
            bar.set_edgecolor('orange')
    
    # Ensure dir exists
    os.makedirs("images/plots", exist_ok=True)
    out_path = "images/plots/material_resonance_scan.png"
    plt.tight_layout()
    plt.savefig(out_path)
    print(f"\nScan complete. Image saved to '{out_path}'.")
    print("Goldene Balken zeigen Materialien, die geometrisch 'einrasten' (stabile 5D-Kopplung).")

if __name__ == "__main__":
    run_material_scan()
