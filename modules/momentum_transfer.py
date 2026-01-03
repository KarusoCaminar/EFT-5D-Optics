import numpy as np
import matplotlib.pyplot as plt

def run_momentum_transfer():
    print("--- Calculating Abraham-Minkowski Momentum Split ---")
    
    # Parameters for Sapphire
    n_sapphire = 1.76
    P_laser = 100.0 # Watts
    c = 3e8
    
    # 1. Force / Pressure Calculation
    # Force exerted on the crystal due to the momentum difference
    # F = P/c * (n - 1/n) (Abraham term is complicated, let's stick to the user's definition)
    # User: Minkowski (n*p0) - Abraham (p0/n) = Lattice Momentum? 
    # Let's visualize the unit momentum vectors.
    
    # Parameters
    materials = ['Vacuum', 'Quartz', 'Sapphire', 'Diamond']
    indices = [1.0, 1.54, 1.76, 2.42]
    colors = ['gray', 'orange', 'blue', 'cyan']
    
    fig, ax = plt.subplots(figsize=(10, 8)) # Taller figure
    
    y_pos = 0
    
    for i, (mat, n) in enumerate(zip(materials, indices)):
        y = 3 - i # 3, 2, 1, 0
        
        # 1. Vacuum Momentum (p0)
        p0 = 1.0
        
        # 2. Minkowski (Total) = n * p0
        p_minkowski = n * p0
        
        # 3. Abraham (Kinetic) = p0 / n
        p_abraham = p0 / n
        
        # 4. Lattice (Drag)
        p_lattice = p_minkowski - p_abraham
        
        # Base Line
        ax.plot([-0.5, 3.5], [y, y], 'k--', alpha=0.1)
        
        # Minkowski (Total)
        ax.arrow(0, y+0.12, p_minkowski, 0, width=0.04, head_width=0.12, head_length=0.1, color=colors[i], alpha=0.3, label='Minkowski (Gesamtimpuls $n \cdot p_0$)' if i==2 else "")
        if i == 0: ax.text(p_minkowski/2, y+0.2, f"Total $p=p_0$", ha='center', color=colors[i], fontsize=8)
        
        # Abraham (Kinetic)
        ax.arrow(0, y-0.12, p_abraham, 0, width=0.04, head_width=0.12, head_length=0.1, color='red', alpha=0.8, label='Abraham (Kinetisch $p_0/n$)' if i==2 else "")
        
        # Lattice (Geometry Drag)
        if n > 1.0:
            ax.arrow(p_abraham, y-0.12, p_lattice, 0, width=0.04, head_width=0.12, head_length=0.1, color='green', alpha=0.8, label='Lattice (5D-Impulsübertrag)' if i==2 else "")
            # Label centered on the green arrow
            ax.text(p_abraham + p_lattice/2, y-0.25, f"Gitter-Impuls\n{p_lattice:.2f} $p_0$", ha='center', color='green', fontsize=8, fontweight='bold')

        ax.text(-0.8, y, f"{mat}\n(n={n})", va='center', ha='right', fontweight='bold', fontsize=10)

    ax.set_xlim(-1, 4.0)
    ax.set_ylim(-2.0, 4.5) # More space at bottom
    ax.set_yticks([])
    ax.set_title("Lösung des Impuls-Rätsels: Geometrische Impulsübertragung\n$p_{Minkowski} = p_{Abraham} + p_{Lattice}$", fontsize=14)
    
    # Legend at top to avoid clash
    ax.legend(loc='upper right', frameon=True)
    
    # Explanation Text (Yellow Box) - Moved DOWN and LEFT
    explanation = (
        "INTERPRETATION:\n"
        "• Das Photon behält seine Identität (rote Pfeile werden kürzer -> langsamer).\n"
        "• Die Differenz zum Gesamtimpuls (blau) geht nicht verloren,\n"
        "  sondern wird als mechanischer Impuls auf das 5D-Gitter übertragen (grün).\n"
        "• Je dichter das Medium (höheres n), desto größer der 'Geometrie-Drag'."
    )
    ax.text(1.5, -1.2, explanation, ha='center', va='center', fontsize=10,
            bbox=dict(facecolor='#fffcdc', edgecolor='#f1c40f', boxstyle='round,pad=1'))

    plt.tight_layout()
    plt.savefig('momentum_transfer.png', dpi=150)
    print("Graph saved to 'momentum_transfer.png'")

if __name__ == "__main__":
    run_momentum_transfer()
