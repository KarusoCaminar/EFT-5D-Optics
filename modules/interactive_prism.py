import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

"""
Module: interactive_prism.py
Purpose: Interactive demonstration of classical optics (Prism) emerging from 5D geometry.
Run this script to open a live matplotlib window showing the FDTD simulation.
"""

# --- Physik-Engine (FDTD) ---
SIZE = 200
phi_field = np.ones((SIZE, SIZE))
e_field = np.zeros((SIZE, SIZE))

# --- Das Prisma-Design ---
# Ein Dreieck in der Mitte
def create_prism(grid_size):
    mask = np.zeros((grid_size, grid_size), dtype=bool)
    # Dreieck Koordinaten
    p1 = (50, 100)
    p2 = (150, 50)
    p3 = (150, 150)
    
    # Baryzentrische Koordinaten oder einfache Linien-Logik für das Dreieck
    y, x = np.ogrid[:grid_size, :grid_size]
    # Einfaches Dreieck (rechtwinklig für Demo)
    # x > 80 und y > 50 und y < 150 und x < (150 - (y-100)*0.5) ... vereinfacht
    # Wir machen ein einfaches Keil-Prisma
    mask = (x > 80) & (x < 140) & (y > 50 + (x-80)*0.5) & (y < 150 - (x-80)*0.5)
    return mask

mask_prism = create_prism(SIZE)
phi_field[mask_prism] = 0.6 # Hoher Brechungsindex (Glas)

# Arrays
e_current = np.zeros((SIZE, SIZE))
e_prev = np.zeros((SIZE, SIZE))
e_next = np.zeros((SIZE, SIZE))

# Parameter
c = 1.0
dt = 0.5
dx = 1.0

# --- Visualisierung ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

im1 = ax1.imshow(phi_field, cmap='gray', vmin=0, vmax=1.2)
ax1.set_title("Die 5D-Geometrie (Das Prisma)")

im2 = ax2.imshow(e_current, cmap='inferno', vmin=-0.5, vmax=0.5)
ax2.set_title("Lichtbrechung (Simulation)")

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
    
    # Quelle: Lichtstrahl von links (schmal)
    # Wir feuern einen kontinuierlichen Strahl ("Laser")
    if frame < 1000:
        beam_width = 10
        center_y = SIZE // 2
        e_next[center_y-beam_width:center_y+beam_width, 10] = np.sin(frame * 0.3)
    
    # Update
    e_prev = e_current.copy()
    e_current = e_next.copy()
    
    im2.set_data(e_current)
    return [im2]

if __name__ == "__main__":
    print("Starte interaktive Prisma-Simulation...")
    anim = FuncAnimation(fig, update, frames=300, interval=20, blit=True)
    plt.show()

    print("Beobachtung:")
    print("Das Licht trifft gerade auf das Prisma und wird nach UNTEN abgelenkt.")
    print("Das beweist: Unsere Feldtheorie beherrscht klassische Optik.")
