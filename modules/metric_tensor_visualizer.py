import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sys

# --- Physik der 5D-Matrix ---
# G_AB ist der 5x5 metrische Tensor.
# Indizes: 0=Zeit, 1,2,3=Raum, 4=5. Dimension (xi)

def create_metric_matrix(E_field_strength, scalar_field_phi):
    # Basis: Minkowski-Metrik (-1, 1, 1, 1) + 5. Dim
    G = np.zeros((5, 5))
    
    # 4D Block (Vereinfacht ohne Raumkrümmung)
    np.fill_diagonal(G, [ -1, 1, 1, 1, 0 ])
    
    # Die 5. Dimension G_55 (Brechungsindex^2 approx)
    G[4, 4] = scalar_field_phi**2
    
    # Die Interaktion: Elektromagnetismus (Kaluza-Klein)
    # E-Feld sitzt in G_04 (und G_40) -> Mischung aus Zeit und 5. Dim
    # B-Feld säße in G_14, G_24...
    G[0, 4] = E_field_strength
    G[4, 0] = E_field_strength
    
    return G

def run_metric_visualization():
    print("--- 5D Matrix Simulator: The Elasticity of Spacetime ---")
    
    # Parameter
    E_max = 2.0
    frames = 100
    
    # Arrays für Kerr-Effekt Plot
    E_values = np.linspace(0, E_max, frames)
    Phi_values = []
    
    # Material-Parameter "Elastizität"
    # Wie stark schrumpft die 5. Dimension unter Stress?
    # Modell: Hookesches Gesetz für Raumzeit. Stress ~ E^2
    # Phi = Phi_0 + gamma * E^2
    Phi_0 = 1.0
    gamma = 0.1 
    
    fig = plt.figure(figsize=(12, 6))
    
    # Subplot 1: Die Matrix (Heatmap)
    ax_mat = fig.add_subplot(1, 2, 1)
    
    # Subplot 2: Der "Feder-Effekt" (Kerr Kurve)
    ax_kerr = fig.add_subplot(1, 2, 2)
    line_kerr, = ax_kerr.plot([], [], 'r-', linewidth=2, label='5D-Deformation (Kerr-Effekt)')
    
    def update(frame):
        # 1. Physik berechnen
        E = E_values[frame]
        
        # Die Reaktion der 5. Dimension (Das "Atmen")
        # Stress auf G_04 führt zu Strain in G_55
        delta_Phi = gamma * E**2 
        Phi = Phi_0 + delta_Phi
        
        # Werte speichern
        Phi_values.append(Phi)
        
        # 2. Matrix updaten
        G = create_metric_matrix(E, Phi)
        
        # Plot Matrix
        ax_mat.clear()
        cax = ax_mat.imshow(G, cmap='coolwarm', vmin=-2, vmax=2)
        
        # Labels Matrix
        labels = ['t', 'x', 'y', 'z', '$\\xi$']
        ax_mat.set_xticks(range(5))
        ax_mat.set_yticks(range(5))
        ax_mat.set_xticklabels(labels)
        ax_mat.set_yticklabels(labels)
        ax_mat.set_title(f"Der Metrische Tensor $G_{{AB}}$\nStress (E-Feld) = {E:.2f}")
        
        # Annotationen
        ax_mat.text(4, 0, "EM-Feld", ha='center', va='center', color='white', fontweight='bold')
        ax_mat.text(4, 4, f"$\Phi$={Phi:.2f}", ha='center', va='center', color='black', fontweight='bold')

        # Plot Kerr
        ax_kerr.clear()
        ax_kerr.plot(E_values[:len(Phi_values)], Phi_values, 'r-', linewidth=2)
        ax_kerr.set_xlim(0, E_max)
        ax_kerr.set_ylim(0.9, 1.5)
        ax_kerr.set_xlabel("Stress (Elektrisches Feld $E$)")
        ax_kerr.set_ylabel("Größe der 5. Dimension ($\Phi$ / Brechungsindex)")
        ax_kerr.set_title("Elastizität: Die '5D-Feder'")
        ax_kerr.grid(True)
        
        # Erklärung
        # Positionierung: Blue Text (left) -> Arrow (center) -> Red Text (right)
        ax_kerr.text(0.0, 1.4, "Stärkeres Feld E...", color='blue', ha='left', va='center')
        
        # Pfeil: Zentriert zwischen den Texten (0.65 bis 1.05)
        ax_kerr.annotate("", xy=(1.05, 1.4), xytext=(0.65, 1.4),
                     arrowprops=dict(arrowstyle="->", lw=1.5, color='black'))
                     
        ax_kerr.text(1.1, 1.4, "...dehnt die 5. Dimension", color='red', ha='left', va='center')
        
    anim = FuncAnimation(fig, update, frames=frames, interval=50, repeat=False)
    
    if "--batch" in sys.argv:
        # Save last frame
        # BUGFIX: We must run the loop to populate the history [Phi_values]
        for i in range(frames):
            update(i)
            
        plt.savefig('metric_tensor_visualization.png')
        print("Snapshot saved to 'metric_tensor_visualization.png'")
    else:
        plt.show()

if __name__ == "__main__":
    run_metric_visualization()
