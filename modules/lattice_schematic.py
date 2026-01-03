import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def run_lattice_schematic():
    print("--- Generating Crystal Lattice Schematic ---")
    
    # Sapphire Lattice Constants (approx for schematic)
    a = 0.475 # nm
    
    # 5D Radius derived from theory
    R_5d = 0.86 # nm (Calculated from m=229eV)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 1. Draw Crystal Lattice (2D Slice of Hexagonal/Trigonal)
    # We draw a grid of atoms
    rows = 5
    cols = 8
    
    # Atom positions
    atom_x = []
    atom_y = []
    
    for i in range(rows):
        for j in range(cols):
            # Shift every other row for hexagonal packing look
            x_shift = 0.5 * a if i % 2 else 0
            x = j * a + x_shift
            y = i * (a * np.sqrt(3)/2) # Hex height
            atom_x.append(x)
            atom_y.append(y)
            
            # Draw Atom
            circle = plt.Circle((x, y), 0.08, color='#7f8c8d', alpha=0.5)
            ax.add_patch(circle)
            
    # Plot atoms
    ax.scatter(atom_x, atom_y, color='#2c3e50', s=50, label='Sapphire Atoms (Al/O)')
    
    # 2. Draw the 5D Wave / Radius
    # We want to show that R_5D fits into this lattice.
    # Center of the "mode"
    center_x = 3 * a
    center_y = 2 * (a * np.sqrt(3)/2)
    
    # Draw the 5D Radius Circle
    # R_5D is the radius of the compact dimension.
    # In the crystal, the "mode" (standing wave) has a wavelength related to R (or diameter).
    # If R ~ 2a, that means the circumference 2*pi*R or the diameter fits.
    # Let's draw a circle of radius R_5D to compare scale.
    
    circle_5d = plt.Circle((center_x, center_y), R_5d, color='red', fill=False, 
                           linestyle='--', linewidth=2, label='5D Radius ($R_{5D}$)')
    ax.add_patch(circle_5d)
    
    # Annotation for Lattice Constant 'a'
    # Draw line between two atoms
    p1 = (atom_x[0], atom_y[0])
    p2 = (atom_x[1], atom_y[0]) # Next atom in x
    ax.annotate("", xy=p2, xytext=p1, arrowprops=dict(arrowstyle="<->", color='green', lw=2))
    ax.text((p1[0]+p2[0])/2, p1[1]-0.2, f"a = {a} nm", color='green', ha='center')
    
    # Annotation for 5D Radius
    # Draw radius line from center to edge of circle
    p_center = (center_x, center_y)
    p_edge = (center_x + R_5d * np.cos(np.pi/4), center_y + R_5d * np.sin(np.pi/4))
    ax.annotate("", xy=p_edge, xytext=p_center, arrowprops=dict(arrowstyle="->", color='red', lw=2))
    ax.text((p_center[0]+p_edge[0])/2 - 0.2, (p_center[1]+p_edge[1])/2 + 0.1, 
            f"$R_{{5D}} \\approx {R_5d}$ nm\n$\\approx 1.8 \\times a$", color='red', fontweight='bold')

    ax.set_aspect('equal')
    ax.set_title("Geometric Validation: The 5D Mode fits the Crystal Lattice")
    ax.set_xlabel("x (nm)")
    ax.set_ylabel("y (nm)")
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-0.5, 2.5)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.2)
    
    plt.savefig('lattice_schematic.png', dpi=150)
    print("Schematic saved to 'lattice_schematic.png'")

if __name__ == "__main__":
    run_lattice_schematic()
