import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import sys

# --- Physik-Engine ---
def calculate_trajectory(R, winding_number, t_max=10):
    """
    Berechnet die Bahn eines Photons in 5D (Helix).
    R: Radius der 5. Dimension (Kompaktifizierung)
    winding_number: Wie oft wickelt sich das Teilchen pro Längeneinheit? (Masse)
    """
    # Zeit/Längsachse (unsere 4D-Welt)
    x4 = np.linspace(0, t_max, 500)
    
    # Die 5D-Bewegung (Winkelkoordinate theta)
    # p5 = n / R (Quantisierter Impuls)
    # Ein hohes 'winding_number' (n) bedeutet hohe Frequenz im Kreis
    theta = (winding_number / R) * x4
    
    # Koordinaten im 3D-Raum (projiziert als Zylinder)
    # Wir stellen die 5. Dimension als Kreis (y, z) dar, x4 ist die Längsrichtung
    y5 = R * np.cos(theta)
    z5 = R * np.sin(theta)
    
    # Effektive Geschwindigkeit in 4D (v_group)
    # In 5D ist v = c = 1.
    # v_4d = 1 / sqrt(1 + (dy/dx)^2) ... geometrische Verlangsamung
    # Steigung der Spirale m = winding_number
    # v_eff = 1 / sqrt(1 + m^2)
    slope = winding_number # Vereinfacht
    v_eff = 1.0 / np.sqrt(1 + slope**2)
    
    return x4, y5, z5, v_eff

# --- Visualisierung ---
def run_visualization():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(bottom=0.25)

    # Startwerte
    init_R = 1.0
    init_n = 2.0 # Modus n=2

    # Plot-Funktion
    def update_plot(val=None):
        R = slider_R.val
        n = slider_n.val
        
        ax.clear()
        
        # 1. Zylinder (Die 5. Dimension)
        Xc = np.linspace(0, 10, 50)
        Th = np.linspace(0, 2*np.pi, 50)
        Xc, Th = np.meshgrid(Xc, Th)
        Yc = R * np.cos(Th)
        Zc = R * np.sin(Th)
        ax.plot_surface(Xc, Yc, Zc, alpha=0.1, color='gray')
        
        # 2. Die Teilchenbahn (Spirale)
        x, y, z, v_eff = calculate_trajectory(R, n, t_max=10)
        
        # Farbe je nach "Effektiver Masse" (Verlangsamung)
        # Rot = Langsam (Massiv/Hohes n), Blau = Schnell (Masselos/n=0)
        color = plt.cm.jet(1 - v_eff) 
        
        ax.plot(x, y, z, linewidth=3, color='red' if n > 0 else 'blue', label='Teilchen-Wellenfunktion')
        
        # Projektion (Schatten) auf den Boden -> Das sehen wir in 4D
        ax.plot(x, y*0 + 2.5, z*0 - 2.5, 'k--', alpha=0.5, label='4D-Projektion (Beobachtung)')

        # Labels
        ax.set_title(f"Kaluza-Klein Kompaktifizierung\nEffektive Lichtgeschwindigkeit $v_{{eff}} = {v_eff:.2f} c$")
        ax.set_xlabel("4D Raumrichtung (x)")
        ax.set_ylabel("5. Dimension (y)")
        ax.set_zlabel("5. Dimension (z)")
        ax.set_ylim(-3, 3)
        ax.set_zlim(-3, 3)
        ax.legend()

    # Slider Controls
    ax_R = plt.axes([0.25, 0.1, 0.65, 0.03])
    ax_n = plt.axes([0.25, 0.05, 0.65, 0.03])

    slider_R = Slider(ax_R, 'Radius R (5D)', 0.5, 3.0, valinit=init_R)
    slider_n = Slider(ax_n, 'Modus n (Impuls)', 0, 10.0, valinit=init_n, valstep=1)

    slider_R.on_changed(update_plot)
    slider_n.on_changed(update_plot)

    # Initialer Aufruf
    update_plot()
    
    # Save a snapshot for documentation
    try:
        plt.savefig('kaluza_klein_visualization.png')
        print("Snapshot saved to 'kaluza_klein_visualization.png'")
    except Exception as e:
        print(f"Failed to save snapshot: {e}")

    # Interactive Handling
    if "--batch" in sys.argv:
        print("Batch mode: Skipping interactive window.")
    else:
        plt.show()

    # --- Erklärung für den User ---
    print("\n--- WAS DU SIEHST ---")
    print("1. Der graue Zylinder ist die 5. Dimension (aufgerollt entlang unserer x-Achse).")
    print("2. Die rote/blaue Linie ist das Lichtteilchen.")
    print("3. Wenn n=0 (gerade Linie): Das Teilchen bewegt sich nicht in der 5. Dimension. Es ist masselos (v=c).")
    print("4. Wenn n>0 (Spirale): Das Teilchen muss 'Umwege' um den Zylinder machen.")
    print("   -> In unserer Welt (der schwarze Schatten) sieht es so aus, als wäre es langsamer.")
    print("   -> Diese 'Verlangsamung' interpretieren wir physikalisch als MASSE.")
    print("5. Der Radius R bestimmt, wie eng die Kurven sind. Kleines R = Hochenergetische Spirale = Große Masse.")

if __name__ == "__main__":
    run_visualization()
