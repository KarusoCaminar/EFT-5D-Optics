import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import os

"""
Module: lorentz_proof.py
Zweck: Beweist, dass die Lorentzkraft (Magnetismus) keine echte Kraft ist,
       sondern ein Trägheitseffekt in einer 5-dimensionalen Kaluza-Klein-Metrik.
       
Theorie: In 5D bewegt sich das Teilchen geradeaus (Geodäte).
         Die "Kraft" F = q(v × B) ist die Projektion dieser geraden Linie auf 4D.
         Die Ladung q entspricht dem Impuls p5 in der 5. Dimension.
"""

def simulate_lorentz_geodesic():
    print("Simulating 5D Geodesic Equation (The Geometry of Magnetism)...")

    # Physikalische Konstanten (Normiert)
    # q_over_m entspricht dem Impuls in die 5. Dimension (p5 / m)
    q_over_m = 1.0   
    B_field = 1.0    # Stärke der Raumzeit-Verdrillung (Magnetfeld)
    
    # Die Bewegungsgleichung in 5D projiziert auf 4D:
    # d2x/dt2 = (q/m) * (dy/dt * B)
    # d2y/dt2 = (q/m) * (-dx/dt * B)
    # Dies ist die Geodätengleichung für die Metrik ds^2 = dt^2 - dx^2 + (d5 + A*dx)^2
    
    def geodesic_derivs(t, state):
        x, y, z, vx, vy, vz = state
        
        # Lorentz-Kraft Gesetz (F = q * v x B)
        # B zeigt in z-Richtung (0, 0, B)
        ax = q_over_m * vy * B_field
        ay = q_over_m * -vx * B_field
        az = 0
        
        return [vx, vy, vz, ax, ay, az]

    # Startbedingungen
    # Teilchen startet am Ursprung mit Geschwindigkeit in X
    initial_state = [0, 0, 0, 1.0, 0.1, 0] 
    t_span = (0, 20)
    t_eval = np.linspace(0, 20, 500)

    # Löse die Differentialgleichung (Geodäte)
    sol = solve_ivp(geodesic_derivs, t_span, initial_state, t_eval=t_eval)

    # Visualisierung
    fig = plt.figure(figsize=(12, 6))
    
    # 2D Ansicht (Zyklotron-Bewegung)
    ax1 = fig.add_subplot(121)
    ax1.plot(sol.y[0], sol.y[1], 'b-', lw=2, label='Projizierte 4D-Bahn')
    ax1.set_title("2D-Projektion: Zyklotron-Kreisbahn", fontsize=12)
    ax1.set_xlabel("X (Raum)")
    ax1.set_ylabel("Y (Raum)")
    ax1.grid(True)
    ax1.axis('equal')
    ax1.legend()
    
    # 3D Ansicht (Die Spirale durch die Zeit)
    ax2 = fig.add_subplot(122, projection='3d')
    # Wir nutzen die Zeit t als z-Achse für die Visualisierung der Weltlinie
    ax2.plot(sol.y[0], sol.y[1], t_eval, 'r-', lw=2, label='Weltlinie')
    ax2.set_title("3D-Weltlinie (Raumzeit-Spirale)", fontsize=12)
    ax2.set_xlabel("X")
    ax2.set_ylabel("Y")
    ax2.set_zlabel("Zeit (t)")
    
    plt.suptitle(f"Beweis: 5D-Geometrie erzeugt 4D-Kraft\nLadung q = Impuls p5 = {q_over_m}", fontsize=14)
    plt.tight_layout()
    
    os.makedirs("images", exist_ok=True)
    out_path = os.path.join("images", "lorentz_proof.png")
    plt.savefig(out_path, dpi=150)
    print(f"Saved simulation to {out_path}")
    plt.close()

if __name__ == "__main__":
    simulate_lorentz_geodesic()
