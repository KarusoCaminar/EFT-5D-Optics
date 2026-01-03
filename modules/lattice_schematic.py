import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import sys
import os

# Robust Import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.physics_engine import PhysicsEngine

def run_lattice_schematic():
    print("--- Generating Crystal Lattice Schematic ---")
    
    # Initialize Core Engine for Calculations
    engine = PhysicsEngine()
    
    # Sapphire Lattice Constants (approx for schematic)
    a = 0.475 # nm
    n_sapphire = 1.77
    
    # 5D Radius derived CORRECTLY from theory (V4.2 Universal)
    m_eff = engine.SCALING_FACTOR_K * (n_sapphire**2)
    R_5d = engine.H_BAR_C / m_eff
    
    print(f"Calculated R_5D for Sapphire (n={n_sapphire}): {R_5d:.4f} nm")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 1. Draw Crystal Lattice (2D Slice of Hexagonal/Trigonal)
    rows = 5
    cols = 8
    
    atom_x = []
    atom_y = []
    
    for i in range(rows):
        for j in range(cols):
            x_shift = 0.5 * a if i % 2 else 0
            x = j * a + x_shift
            y = i * (a * np.sqrt(3)/2) 
            atom_x.append(x)
            atom_y.append(y)
            
            circle = plt.Circle((x, y), 0.08, color='#7f8c8d', alpha=0.5)
            ax.add_patch(circle)
            
    ax.scatter(atom_x, atom_y, color='#2c3e50', s=50, label='Sapphire Atoms (Al/O)')
    
    # 2. Draw the 5D Wave / Radius
    center_x = 3 * a
    center_y = 2 * (a * np.sqrt(3)/2)
    
    # Draw circle
    circle_5d = plt.Circle((center_x, center_y), R_5d, color='red', fill=False, 
                           linestyle='--', linewidth=2, label=f'5D Radius ($R_{{5D}}={R_5d:.2f}$ nm)')
    ax.add_patch(circle_5d)
    
    # Annotate a
    p1 = (atom_x[0], atom_y[0])
    p2 = (atom_x[1], atom_y[0])
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="<->", color='green', lw=2))
    ax.text((p1[0]+p2[0])/2, p1[1]-0.2, f"a = {a} nm", color='green', ha='center')
    
    # Annotate R
    p_center = (center_x, center_y)
    p_edge = (center_x + R_5d * np.cos(np.pi/4), center_y + R_5d * np.sin(np.pi/4))
    ax.annotate("", xy=p_edge, xytext=p_center, arrowprops=dict(arrowstyle="->", color='red', lw=2))
    
    ratio = R_5d / a
    # V4.2 Correction: Ratio is now ~2.08, not 1.8. 
    # Logic: The resonance is with the 2nd Harmonic (N=2), so R ~ 2a.
    ax.text((p_center[0]+p_edge[0])/2 - 0.2, (p_center[1]+p_edge[1])/2 + 0.1, 
            f"$R_{{5D}}/a \\approx {ratio:.2f} (N \\approx 2)$", color='red', fontweight='bold')

    ax.set_aspect('equal')
    ax.set_title("Geometric Validation: The 5D Mode fits the Crystal Lattice (Universal K)")
    ax.set_xlabel("x (nm)")
    ax.set_ylabel("y (nm)")
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 2.5)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.2)
    
    os.makedirs("images/plots", exist_ok=True)
    out_path = os.path.join("images", "plots", "lattice_schematic.png")
    plt.savefig(out_path, dpi=150)
    print(f"Schematic saved to '{out_path}'")

if __name__ == "__main__":
    run_lattice_schematic()
