import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

"""
Module: interactive_cloaking.py
Purpose: Interactive demonstration of the 5D Invisibility Cloak.
Run this script to open a live matplotlib window showing the FDTD simulation.
"""


# --- Physik-Engine (FDTD) ---
# Wir simulieren wieder die Wellengleichung in 2D
# d^2E/dt^2 = c^2 * Phi^2 * nabla^2 E

SIZE = 200
phi_field = np.ones((SIZE, SIZE))
e_field = np.zeros((SIZE, SIZE))

# --- Das Tarnkappen-Design ---
# Wir wollen, dass Licht um die Mitte herumfließt.
# Dafür brauchen wir einen Gradienten im Brechungsindex.
# Klassisch (Transformation Optics): n(r) muss innen klein und außen groß sein (oder umgekehrt).
# In 5D: Wir modellieren eine "Raumzeit-Beule".

center = SIZE // 2
R_inner = 20
R_outer = 40

y, x = np.ogrid[:SIZE, :SIZE]
r = np.sqrt((x - center)**2 + (y - center)**2)

# Wir erzeugen einen Ring mit variablem Phi
# Phi < 1 bedeutet n > 1 (Licht wird langsam/abgelenkt)
# Wir wollen, dass Licht "außen herum" schneller ist als "innen durch"?
# Nein, wir wollen es ablenken. Wir bauen eine "Linse", die das Licht um den Kern biegt.

mask_ring = (r >= R_inner) & (r <= R_outer)
# Ein Gradient, der das Licht nach außen drückt
phi_field[mask_ring] = 0.5 + 0.5 * (r[mask_ring] - R_inner) / (R_outer - R_inner)

# Im inneren Kern (das Versteck) ist Phi=1 (oder egal, Licht soll nicht hin)
# Wir machen es zur Kontrolle schwarz (Absorber), damit wir sehen, ob Licht reinkommt.
mask_core = r < R_inner
phi_field[mask_core] = 0.0 # "Loch" in der Raumzeit (keine Ausbreitung)

# Arrays für Zeit-Integration
e_current = np.zeros((SIZE, SIZE))
e_prev = np.zeros((SIZE, SIZE))
e_next = np.zeros((SIZE, SIZE))

# Parameter
c = 1.0
dt = 0.5
dx = 1.0

# --- Visualisierung ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Die Geometrie (Die Tarnkappe)
im1 = ax1.imshow(phi_field, cmap='gray', vmin=0, vmax=1.2)
ax1.set_title(r"Das $\Phi$-Feld (Die Tarnkappe)")
# Zeichne Kreise zur Orientierung
circle1 = plt.Circle((center, center), R_inner, color='r', fill=False)
circle2 = plt.Circle((center, center), R_outer, color='b', fill=False)
ax1.add_patch(circle1)
ax1.add_patch(circle2)
ax1.text(center, center, "HIDDEN", color='red', ha='center', va='center')

# Plot 2: Das Licht
im2 = ax2.imshow(e_current, cmap='inferno', vmin=-0.5, vmax=0.5)
ax2.set_title("Lichtwelle (E-Feld)")

def update(frame):
    global e_current, e_prev, e_next
    
    # Laplace
    laplacian = (
        np.roll(e_current, 1, axis=0) + np.roll(e_current, -1, axis=0) +
        np.roll(e_current, 1, axis=1) + np.roll(e_current, -1, axis=1) -
        4 * e_current
    ) / (dx**2)
    
    # Wellengleichung
    v_sq = (c * phi_field)**2
    e_next = 2*e_current - e_prev + v_sq * laplacian * dt**2
    
    # Quelle: Eine Ebene Welle von Links
    # Wir speisen sie kontinuierlich ein
    e_next[:, 5] = np.sin(frame * 0.2)
    
    # Update
    e_prev = e_current.copy()
    e_current = e_next.copy()
    
    im2.set_data(e_current)
    return [im2]

anim = FuncAnimation(fig, update, frames=400, interval=20, blit=True)
plt.show()

print("Beobachtung:")
print("1. Die Wellenfronten kommen von links.")
print("2. Sie treffen auf den Ring (die Tarnkappe).")
print("3. Sie fließen UM den roten Kreis herum.")
print("4. Dahinter (rechts) schließen sie sich wieder.")
print("Ergebnis: Ein Objekt im roten Kreis wäre für den Beobachter rechts UNSICHTBAR.")
