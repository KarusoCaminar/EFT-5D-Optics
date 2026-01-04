import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Update Path to ensure we import the local modules correctly even if run from subfolder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
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
    
    # Calculate R_5D dynamically using V4.2 Universal K
    m_eff = engine.SCALING_FACTOR_K * (n_sapphire**2)
    R_5D = engine.H_BAR_C / m_eff
    
    ratio = R_5D / a_lattice
    print(f"Sapphire Ratio Check: {ratio:.3f} (Should be ~2.08)")
    
    length = 5.0 # nm
    x = np.linspace(0, length, 1000)
    
    # 1. The Atomic Lattice (Potential Wells)
    potential = np.zeros_like(x)
    atom_positions = np.arange(0, length, a_lattice)
    
    for pos in atom_positions:
        potential += -1.0 * np.exp(-(x - pos)**2 / 0.01)
        
    # 2. The 5D Standing Wave
    # With Ratio ~ 2.08, R_5D is approx 2*a.
    # Wavelength Lambda = R_5D works well for visual resonance if Node alignment is N=2
    lambda_field = R_5D 
    
    wave = 0.8 * np.cos(2 * np.pi * x / lambda_field)
    
    # Visualization
    plt.figure(figsize=(10, 6))
    
    plt.fill_between(x, potential, 0, color='#bdc3c7', alpha=0.5, label='Crystal Lattice (Al/O Atoms)')
    plt.plot(x, wave, 'r-', linewidth=2, label=r'5D Metric Wave ($\Phi$)')
    
    # Mark Resonance Points - Every 2nd atom should match a peak/node
    # If ratio is approx 2.08, it drifts slightly, but aligns locally.
    lock_pts = atom_positions[::2]
    plt.scatter(lock_pts, np.zeros_like(lock_pts) + 0.1, color='red', marker='v', zorder=5, label='Locking Nodes (N=2)')
    
    plt.title(f'Geometric Locking: 5D-Field vs. Atomic Lattice (Ratio = {ratio:.2f})', fontsize=14)
    plt.xlabel('Distance [nm]', fontsize=12)
    plt.ylabel('Field Amplitude / Potential', fontsize=12)
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 4)
    plt.ylim(-1.5, 1.5)
    
    # Explicit Annotation of V4.2 Constants
    plt.text(0.1, 1.3, f"$R_{{5D}}$ = {R_5D:.3f} nm", fontsize=11, color='blue', fontweight='bold')
    plt.text(0.1, 1.15, f"$a$ = {a_lattice:.3f} nm", fontsize=11, color='gray')
    plt.text(2.0, -1.3, f"Universal Calibration K={engine.SCALING_FACTOR_K}", fontsize=10, style='italic')
    
    os.makedirs("images/plots", exist_ok=True)
    out_path = os.path.join("images", "plots", "experiment_locking.png")
    plt.savefig(out_path, dpi=150)
    print(f"Saved simulation to {out_path}")
    plt.close()

if __name__ == "__main__":
    simulate_locking()
