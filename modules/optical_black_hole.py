import numpy as np
import matplotlib.pyplot as plt
import os

"""
Module: optical_black_hole.py
Zweck: Simuliert einen Ereignishorizont in einer Glasfaser (Analog Gravity).

Theorie: Ein intensiver Laserpuls ändert n(x,t) via Kerr-Effekt.
         Wenn sich der Puls mit v bewegt und c/n < v wird, entsteht ein Horizont.
         Licht kann den Puls nicht überholen - es wird "gefangen".
         Dies ist die optische Analogie zu einem Schwarzen Loch.
"""

def simulate_event_horizon():
    print("Simulating Optical Event Horizon (Analog Gravity)...")
    
    # Gitter-Parameter (1D Simulation)
    Nx = 1000
    Nt = 1500
    x = np.linspace(0, 100, Nx)
    dx = x[1] - x[0]
    dt = 0.05 # Zeitschritt
    
    # Felder
    E = np.zeros(Nx)      # Elektrisches Feld (Das "Opfer"-Licht)
    E_prev = np.zeros(Nx)
    
    # Der "Monster"-Puls (Das Schwarze Loch)
    # Er bewegt sich mit Geschwindigkeit v_pulse
    v_pulse = 0.9 
    n0 = 1.0      # Basis-Brechungsindex
    dn = 0.5      # Kerr-Effekt Stärke (Extreme Änderung durch 5D-Kopplung)
    
    # Speicher für das Wasserfall-Diagramm (Raum-Zeit-Plot)
    history = np.zeros((Nt, Nx))
    
    # Simulation Loop (FDTD - Finite Difference Time Domain)
    for t_step in range(Nt):
        t = t_step * dt
        
        # 1. Berechne den aktuellen Brechungsindex n(x,t)
        # Der Puls bewegt sich von links nach rechts
        pulse_pos = 10 + v_pulse * t
        
        # Gauß-Profil des Pulses
        pulse_shape = np.exp(-(x - pulse_pos)**2 / 20.0)
        
        # n steigt dort, wo der Puls ist (Raumzeit-Kompression)
        current_n = n0 + dn * pulse_shape
        
        # Lokale Lichtgeschwindigkeit c(x) = 1 / n(x)
        c_local = 1.0 / current_n
        
        # 2. Wellengleichung lösen: d2E/dt2 = c^2 * d2E/dx2
        # (Vereinfachte FDTD update rule)
        if t_step > 1:
            # Courant-Zahl squared
            C2 = (c_local * dt / dx)**2
            
            # Wave Update (Laplacian)
            E_next = 2*E - E_prev + C2 * (np.roll(E, -1) - 2*E + np.roll(E, 1))
            
            # Quelle: Ein schwacher Sinus-Laser, der versucht, den Puls zu überholen
            # Wir speisen ihn kontinuierlich links ein
            E_next[5] = 0.5 * np.sin(0.5 * t)
            
            # Update history
            E_prev = E.copy()
            E = E_next.copy()
            
            # Absorbierende Ränder (einfach)
            E[0] = E[1]
            E[-1] = E[-2]
            
        history[t_step, :] = E
        
    # Visualisierung: Das Raum-Zeit-Diagramm
    plt.figure(figsize=(10, 8))
    
    # Plot Wavefield
    # Wir plotten die Intensität |E|
    plt.imshow(np.abs(history), aspect='auto', extent=[0, 100, Nt*dt, 0], cmap='inferno')
    
    # Plot die Bahn des "Ereignishorizonts" (Zentrum des Pulses)
    t_axis = np.linspace(0, Nt*dt, Nt)
    horizon_path = 10 + v_pulse * t_axis
    plt.plot(horizon_path, t_axis, 'w--', linewidth=2, label='Ereignishorizont (Puls)')
    
    plt.title("Optical Black Hole Simulation\nLicht (Gelb) wird am Horizont (Weiß) gestaut", fontsize=14)
    plt.xlabel("Ort x (Glasfaser)", fontsize=12)
    plt.ylabel("Zeit t", fontsize=12)
    plt.colorbar(label="Licht-Intensität")
    plt.legend(loc='upper right')
    
    # Annotation
    plt.text(20, 10, "Gefangenes Licht\n(Hawking Pile-up)", color='cyan', fontsize=12, fontweight='bold')
    
    os.makedirs("images", exist_ok=True)
    out_path = os.path.join("images", "optical_black_hole.png")
    plt.savefig(out_path, dpi=150)
    print(f"Saved simulation to {out_path}")
    plt.close()

if __name__ == "__main__":
    simulate_event_horizon()
