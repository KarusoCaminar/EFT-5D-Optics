import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

"""
Module: quantum_tob_optimizer.py
Zweck: Wendet 'Topology Optimization' (TOB) auf die 5D-Raumzeit an.
Ziel: Designe eine Gitterstruktur, die den Elektronen-Widerstand minimiert.
      (Suche nach dem perfekten Supraleiter-Gitter).
"""

# 1. Die Zielfunktion (Was wollen wir optimieren?)
# Wir wollen minimale effektive Masse m ~ 1/R_5D
# R_5D hängt von der Gitterkonstante 'a' und der Geometrie 'shape' ab.

def effective_mass_cost(design_params):
    """
    design_params: [a_lattice, geometry_factor]
    a_lattice: Gitterabstand (nm)
    geometry_factor: Wie 'verdreht' ist der Raum? (Moiré-Winkel, Krümmung)
    """
    a = design_params[0]
    twist = design_params[1]
    
    # Unsere Theorie-Formel (Hypothetisch erweitert für TOB)
    # R_5D = a * (1 + sin(twist))  <-- Geometrischer Boost durch Verdrehung
    # Masse m ~ 1 / R_5D
    
    # Straf-Terme (Constraints):
    # a darf nicht zu klein sein (Atomkollaps)
    # a darf nicht zu groß sein (Gitter instabil)
    if a < 0.2 or a > 2.0: return 1e6 
    
    R_5d = a * (1.0 + 2.0 * np.sin(twist)**2) # Moiré-Effekt erhöht effektiven Radius
    
    mass = 1.0 / R_5d # Ziel: Minimiere Masse
    return mass

# 2. Der Optimierer (Die KI)
def run_tob_optimization():
    print("--- Quantum Topology Optimization (TOB) ---")
    print("Suche nach der optimalen Raumzeit-Architektur...")
    
    # Startwert: Saphir-ähnlich (a=0.47), aber mit leichtem Twist (1.0 rad),
    # damit der Optimizer nicht im Sattelpunkt (0°) stecken bleibt.
    initial_guess = [0.47, 1.0]
    
    # Optimierung
    result = minimize(effective_mass_cost, initial_guess, method='Nelder-Mead')
    
    best_a = result.x[0]
    best_twist = result.x[1]
    
    # Twist in Grad
    best_twist_deg = np.degrees(best_twist)
    
    min_mass = result.fun
    
    print(f"\nOPTIMALES DESIGN GEFUNDEN:")
    print(f"Gitterkonstante a: {best_a:.4f} nm")
    print(f"Twist-Winkel:      {best_twist:.4f} rad ({best_twist_deg:.1f}°)")
    print(f"Effektive Masse:   {min_mass:.4f} (Relativ)")
    print("-" * 40)
    
    # Visualisierung des "Landschaft"
    a_range = np.linspace(0.2, 2.2, 100)
    twist_range = np.linspace(0, np.pi, 100)
    A, T = np.meshgrid(a_range, twist_range)
    # Massen-Landschaft
    Mass = 1.0 / (A * (1.0 + 2.0 * np.sin(T)**2))
    
    plt.figure(figsize=(10, 7))
    # Levels logaritmisch oder fein abgestuft für besseren Kontrast
    levels = np.linspace(Mass.min(), Mass.max(), 40)
    cp = plt.contourf(A, np.degrees(T), Mass, levels=levels, cmap='inferno_r') # Inferno Reverse: Hell = Wenig Masse
    cbar = plt.colorbar(cp)
    cbar.set_label('Effektive Masse (Geometrischer Widerstand)', fontsize=12)
    
    # Optimum markieren
    plt.plot(best_a, np.degrees(best_twist), 'cyan', marker='*', markersize=20, markeredgecolor='white', label='TOB Optimum (90° Twist)')
    
    plt.annotate(f"Min Mass: {min_mass:.2f}\nAngle: {np.degrees(best_twist):.0f}°", 
                 xy=(best_a, np.degrees(best_twist)), 
                 xytext=(best_a - 0.8, np.degrees(best_twist) - 30),
                 color='white', fontweight='bold', fontsize=11,
                 arrowprops=dict(facecolor='white', shrink=0.05))

    plt.title("Quantum TOB: Topologie-Optimierung der Raumzeit", fontsize=16, pad=20)
    plt.xlabel("Gitterkonstante a [nm]", fontsize=12)
    plt.ylabel("Geometrischer Twist [Grad]", fontsize=12)
    plt.grid(True, alpha=0.3, color='white')
    plt.legend(loc='upper right', frameon=True, facecolor='black', labelcolor='white')
    
    # Style Anpassungen
    plt.tight_layout()
    plt.savefig("quantum_tob_result.png", dpi=300)
    print("Visualisierung gespeichert: quantum_tob_result.png")

if __name__ == "__main__":
    run_tob_optimization()
