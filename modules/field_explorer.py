import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import sys

def run_field_explorer():
    print("--- 5D Field Explorer: Visualizing Refraction as Geometry ---")
    
    # --- Physik ---
    SIZE = 150 # Grid Size
    phi_field = np.ones((SIZE, SIZE)) # Vakuum phi=1
    e_field = np.zeros((SIZE, SIZE))  # Lichtpuls

    # Wir platzieren "Materie" in der Mitte (einen Kristall)
    # Materie bedeutet: Das Phi-Feld ist hier "steifer" (höhere Dichte)
    center_y, center_x = SIZE // 2, SIZE // 2
    radius = 30
    y, x = np.ogrid[:SIZE, :SIZE]
    
    # Materie mit weicher Kante für schönere Simulation
    dist_sq = (x - center_x)**2 + (y - center_y)**2
    mask = dist_sq <= radius**2
    phi_field[mask] = 0.5 # Kleineres Phi -> Höherer Brechungsindex (n=2)
    
    # Simulation Parameters
    dt = 0.5
    dx = 1.0
    c = 1.0

    # Arrays für Zeit-Integration (FDTD)
    e_current = np.zeros((SIZE, SIZE))
    e_prev = np.zeros((SIZE, SIZE))
    e_next = np.zeros((SIZE, SIZE))

    # --- Visualisierung ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    im1 = ax1.imshow(phi_field, cmap='gray', vmin=0.0, vmax=1.2)
    ax1.set_title("Die 5D-Geometrie ($\Phi$-Feld)")
    ax1.set_xlabel("Dunkler Kreis = Kompaktere 5. Dimension")
    
    # Text overlay on Phi Field
    ax1.text(center_x, center_y, "MATERIE\n(n=2)", color='white', ha='center', va='center', fontweight='bold')
    ax1.text(10, 10, "VAKUUM (n=1)", color='black', ha='left', va='top')

    im2 = ax2.imshow(e_current, cmap='inferno', vmin=-0.5, vmax=0.5)
    ax2.set_title("Das Lichtfeld ($E$-Feld)")
    ax2.set_xlabel("Licht wird durch die Krümmung gebrochen")

    def update(frame):
        nonlocal e_current, e_prev, e_next
        
        # 1. Laplace-Operator (Raumkrümmung)
        laplacian = (
            np.roll(e_current, 1, axis=0) + np.roll(e_current, -1, axis=0) +
            np.roll(e_current, 1, axis=1) + np.roll(e_current, -1, axis=1) -
            4 * e_current
        ) / (dx**2)
        
        # 2. Wellengleichung mit 5D-Kopplung
        # Die lokale Lichtgeschwindigkeit ist c * phi
        # FDTD Update Rule: u(t+dt) = 2u(t) - u(t-dt) + v^2 * dt^2 * laplacian
        v_local_sq = (c * phi_field)**2
        
        # Damping boundary to prevent reflections from edges
        # Simple damping at borders
        damping = np.ones_like(e_current)
        edge = 10
        damping[:edge, :] *= 0.8
        damping[-edge:, :] *= 0.8
        damping[:, :edge] *= 0.8
        damping[:, -edge:] *= 0.8
        
        e_next = (2*e_current - e_prev + v_local_sq * laplacian * (dt**2)) * damping
        
        # Quelle (Laserpuls von links, schräg einfallend)
        # Wir simulieren eine ebene Welle, die von links oben kommt
        if frame < 60:
            sources_y = np.arange(20, 80)
            sources_x = 10
            phase = sources_y * 0.2 # Winkel
            e_next[sources_y, sources_x] += 0.5 * np.sin(frame * 0.5 + phase)
        
        # Update
        e_prev = e_current.copy()
        e_current = e_next.copy()
        
        im2.set_data(e_current)
        return [im2]
    
    frames = 500
    anim = FuncAnimation(fig, update, frames=frames, interval=30, blit=True)
    
    # Save Logic
    if "--batch" in sys.argv:
        import os
        
        # Ensure images/ directory exists
        output_dir = "images"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        gif_path = os.path.join(output_dir, 'field_explorer.gif')
        png_path = os.path.join(output_dir, 'field_explorer_snapshot.png')
        
        print(f"Saving animation to '{gif_path}'...")
        anim.save(gif_path, writer=PillowWriter(fps=30))
        print("Animation saved.")
        
        # Also save a snapshot for static report
        plt.savefig(png_path)
    else:
        plt.show()

if __name__ == "__main__":
    run_field_explorer()
