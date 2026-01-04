import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

"""
Module: raytracer_5d_engine.py
Zweck: Physikalisch korrekter Raytracer basierend auf 5D-Geodäten.
Features:
- Simuliert Lichtbahnen in gekrümmten Metriken (Metamaterialien/Gravitation).
- Erzeugt 'Fischaugen'-Effekte und Linsenverzerrungen prozedural.
- Kann als Basis für Spiele oder CGI genutzt werden.
"""

# 1. Die "Welt" (Metrik-Definition)
def metric_lens(x, y):
    """
    Definiert die optische Dichte (Krümmung Phi) im Raum.
    Beispiel: Eine 'Luneburg-Linse' oder ein Gravitationsfeld.
    """
    r2 = x**2 + y**2
    # Ein dichter Kern in der Mitte (hoher Brechungsindex n = 1/Phi)
    # Phi geht von 1.0 (Vakuum) runter auf 0.5 (Kern)
    Phi = 1.0 - 0.5 * np.exp(-r2 / 4.0)
    
    # Gradienten (für die Kraftberechnung)
    dPhi_dr = -0.5 * np.exp(-r2 / 4.0) * (-2*np.sqrt(r2) / 4.0)
    # Kettenregel für x, y (vereinfacht für radialsymmetrisches Feld)
    dPhi_dx = -0.5 * np.exp(-r2 / 4.0) * (-2*x / 4.0)
    dPhi_dy = -0.5 * np.exp(-r2 / 4.0) * (-2*y / 4.0)
    
    return Phi, dPhi_dx, dPhi_dy

# 2. Die Physik (Geodätengleichung)
def ray_equation(t, state):
    x, y, vx, vy = state
    
    # Hole Metrik-Daten an aktueller Position
    Phi, dPhi_dx, dPhi_dy = metric_lens(x, y)
    
    # 5D-Kraftgesetz: F = - (1/Phi) * grad(Phi) * v^2
    # Das Licht wird in Bereiche mit kleinerem Phi (höherem n) gezogen.
    speed_sq = vx**2 + vy**2
    ax = (1.0 / Phi) * dPhi_dx * speed_sq
    ay = (1.0 / Phi) * dPhi_dy * speed_sq
    
    return [vx, vy, ax, ay]

# 3. Die Kamera (Rendering)
def render_scene(resolution=20):
    print("Rendering 5D Scene (Raytracing)...")
    
    # Wir schießen Strahlen von links (x=-10) nach rechts durch die Linse
    y_start_points = np.linspace(-5, 5, resolution)
    
    plt.figure(figsize=(10, 8))
    
    # Hintergrund (Das "Gitter" der Raumzeit)
    X, Y = np.meshgrid(np.linspace(-10, 10, 50), np.linspace(-6, 6, 50))
    Phi_val = 1.0 - 0.5 * np.exp(-(X**2 + Y**2) / 4.0)
    plt.contourf(X, Y, Phi_val, levels=30, cmap='bone')
    plt.colorbar(label="Raumzeit-Skalierung $\Phi$")
    
    # Raytracing Loop
    for y_start in y_start_points:
        # Startzustand: x=-10, y=y_start, vx=1 (nach rechts), vy=0
        initial_state = [-10, y_start, 1.0, 0.0]
        
        # Löse die Bewegungsgleichung
        sol = solve_ivp(ray_equation, [0, 25], initial_state, rtol=1e-5, max_step=0.1)
        
        # Zeichne den Strahl
        # Farbe basierend auf y_start (Regenbogen-Effekt)
        color = plt.cm.jet((y_start + 5) / 10)
        plt.plot(sol.y[0], sol.y[1], color=color, alpha=0.8, linewidth=1.5)

    plt.title("5D Raytracing: Lichtkrümmung durch Metrik-Gradienten", fontsize=14)
    plt.xlabel("Raum X")
    plt.ylabel("Raum Y")
    plt.xlim(-10, 10)
    plt.ylim(-6, 6)
    
    # Speichern
    plt.savefig("5d_raytracing_render.png", dpi=150)
    print("Render saved to 5d_raytracing_render.png")

if __name__ == "__main__":
    render_scene(resolution=30)
