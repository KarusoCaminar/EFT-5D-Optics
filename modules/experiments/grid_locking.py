import numpy as np
import matplotlib.pyplot as plt
import os
from modules.physics_engine import PhysicsEngine

"""
Module: grid_locking.py
Purpose: Visualizes the "Geometric Locking" (Resonance) between the 5D-Field and atomic matter.
Physics: Compares the 5D-wavelength (lambda = 2*R_5D) with the Crystal Lattice Constant (a).
"""

def simulate_locking():
    print("Simulating Grid Locking (Geometric Resonance)...")
    
    engine = PhysicsEngine()
    
    # Parameters for Sapphire
    a_lattice = 0.475  # nm
    n_sapphire = 1.77
    
    # Calculate R_5D dynamically
    m_eff = engine.SCALING_FACTOR_K * (n_sapphire**2)
    R_5D = engine.H_BAR_C / m_eff
    
    ratio = R_5D / a_lattice
    print(f"Sapphire Ratio Check: {ratio:.3f}")
    
    length = 5.0 # nm
    x = np.linspace(0, length, 1000)
    
    # 1. The Atomic Lattice (Potential Wells)
    potential = np.zeros_like(x)
    atom_positions = np.arange(0, length, a_lattice)
    
    for pos in atom_positions:
        potential += -1.0 * np.exp(-(x - pos)**2 / 0.01)
        
    # 2. The 5D Standing Wave
    # With Ratio ~ 2.08, the wave should be approx twice the lattice spacing.
    # Wavelength Lambda ~ R_5D * 2? Or just R_5D?
    # If the Ratio is ~2, that means R_5D is 2*a.
    # If we assume the simplest mode fits R_5D, then Lambda = R_5D.
    lambda_field = R_5D 
    
    wave = 0.8 * np.cos(2 * np.pi * x / lambda_field)
    
    # Visualization
    plt.figure(figsize=(12, 6))
    
    plt.fill_between(x, potential, 0, color='gray', alpha=0.5, label='Crystal Lattice (Al/O Atoms)')
    plt.plot(x, wave, 'r-', linewidth=2, label=r'5D Metric Wave ($\Phi$)')
    
    # Mark Resonance Points?
    # If perfectly locked (Ratio 2.0), every 2nd atom hits a peak.
    if abs(ratio - 2.0) < 0.2:
        plt.scatter(atom_positions[::2], np.zeros_like(atom_positions[::2]), color='red', zorder=5, label='Locking Nodes (N=2)')
    
    plt.title(f'Geometric Locking: 5D-Field vs. Lattice (Ratio = {ratio:.2f})', fontsize=14)
    plt.xlabel('Distance [nm]', fontsize=12)
    plt.ylabel('Field Amplitude / Potential', fontsize=12)
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 4)
    plt.ylim(-1.5, 1.5)
    
    plt.text(0.2, 1.2, f"$R_{{5D}}$ = {R_5D:.3f} nm", fontsize=12, color='blue')
    plt.text(2.0, -1.3, "Universal Calibration K=63.5 applied.", fontsize=10, style='italic')
    
    os.makedirs("images/plots", exist_ok=True)
    out_path = os.path.join("images", "plots", "experiment_locking.png") # Updated path to plots
    plt.savefig(out_path, dpi=150)
    print(f"Saved simulation to {out_path}")
    plt.close()

if __name__ == "__main__":
    simulate_locking()
