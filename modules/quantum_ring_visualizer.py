import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys

# --- Physik ---
# Wir simulieren eine Welle auf einem geschlossenen Ring (5. Dimension)
# Bedingung für Existenz: Die Welle muss sich in den Schwanz beißen (konstruktive Interferenz)

def generate_ring_wave(radius, mode_number, resolution=500):
    # Winkel von 0 bis 2*pi (einmal um den Kreis)
    theta = np.linspace(0, 2*np.pi, resolution)
    
    # Der Kreis im Raum (Geometrie der 5. Dimension)
    x_circle = radius * np.cos(theta)
    y_circle = radius * np.sin(theta)
    
    # Die Welle "auf" dem Kreis (Amplitude addiert zum Radius)
    # mode_number (n) bestimmt, wie viele Wellenberge auf den Ring passen
    amplitude = 0.2 * radius * np.sin(mode_number * theta)
    
    # Modifizierte Koordinaten (wackelnder Ring)
    x_wave = (radius + amplitude) * np.cos(theta)
    y_wave = (radius + amplitude) * np.sin(theta)
    
    return x_circle, y_circle, x_wave, y_wave

def run_visualization():
    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.subplots_adjust(bottom=0.25)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.title("Warum ist Energie quantisiert?\nNur ganze Zahlen $n$ bilden stabile Wellen.", fontsize=14)

    # Initiale Werte
    R0 = 1.0
    n0 = 1.0

    # Geometrie zeichnen
    xc, yc, xw, yw = generate_ring_wave(R0, n0)
    line_base, = ax.plot(xc, yc, 'k--', alpha=0.3, label='5. Dimension (Kompakt)')
    line_wave, = ax.plot(xw, yw, 'r-', linewidth=2, label='Feld $\Phi$ (Wellenfunktion)')
    start_point, = ax.plot(xw[0], yw[0], 'bo', markersize=8, label='Start/Ende-Punkt')

    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.legend(loc='upper right')

    # Text für Status
    status_text = ax.text(0, 0, "STABIL (Resonanz)", ha='center', va='center', fontsize=12, color='green', fontweight='bold')

    # Slider Logic (only for interactive mode)
    ax_n = plt.axes([0.2, 0.1, 0.6, 0.03])
    slider_n = Slider(ax_n, 'Modus n (Impuls)', 0.0, 10.0, valinit=n0)

    def update(val):
        n = slider_n.val
        update_plot(n)

    def update_plot(n):
        # Neuberechnung
        _, _, xw_new, yw_new = generate_ring_wave(R0, n)
        line_wave.set_data(xw_new, yw_new)
        
        # Visueller Check: Ist n nahe an einer ganzen Zahl?
        if abs(n - round(n)) < 0.05:
            line_wave.set_color('green')
            status_text.set_text("STABIL (Quantisiert)\nEnergie erhalten")
            status_text.set_color('green')
            line_wave.set_linestyle('-')
        else:
            line_wave.set_color('red')
            status_text.set_text("INSTABIL (Zerfall)\nSelbst-Auslöschung")
            status_text.set_color('red')
            line_wave.set_linestyle(':')

    slider_n.on_changed(update)

    # Check for batch mode
    if "--batch" in sys.argv:
        # Generate a stable state for the snapshot
        update_plot(3.0) 
        plt.savefig('quantum_ring_visualization.png')
        print("Snapshot saved to 'quantum_ring_visualization.png'")
    else:
        plt.show()

if __name__ == "__main__":
    run_visualization()
