import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter, FFMpegWriter
import os

"""
Module: generate_fiber_image.py
Purpose: Generates visual assets (GIF/MP4) for Total Internal Reflection (Fiber Optics).
This demonstrates that the 5D theory naturally handles reflection when angles are steep.
"""

# Configure FFmpeg Path explicitly
ffmpeg_path = r"C:\Users\Moritz\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"
plt.rcParams['animation.ffmpeg_path'] = ffmpeg_path

# --- Physik-Engine (FDTD) ---
SIZE = 200
phi_field = np.ones((SIZE, SIZE))
e_field = np.zeros((SIZE, SIZE))

# --- Fiber Design ---
# High index core (n=2, phi=0.5) surrounded by vacuum (n=1, phi=1)
center_y = SIZE // 2
fiber_width = 40
phi_field[center_y-fiber_width//2:center_y+fiber_width//2, :] = 0.5 # Core

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
ax1.set_title("Die 5D-Geometrie (Glasfaser)")
ax1.text(10, center_y, "CORE (n=2)", color='white', ha='left', va='center')
ax1.text(10, 20, "CLADDING (n=1)", color='black', ha='left', va='center')

im2 = ax2.imshow(e_current, cmap='inferno', vmin=-0.5, vmax=0.5)
ax2.set_title("Totalreflexion (Lichtleiter)")

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
    
    # Quelle: Lichtstrahl schräg von links unten
    # Wir starten IM Kern, aber schräg, damit er gegen die Wand prallt
    if frame < 2000: # Continuous beam
        # Launch point: Bottom of core, angled up
        start_y = center_y + 10
        start_x = 10
        # Simple point source oscillating
        # To make a beam, we need a phased array or just a point that moves?
        # Let's just do a point source at the edge of the core
        e_next[center_y+10, 50] += 0.5 * np.sin(frame * 0.3)

    # Update
    e_prev = e_current.copy()
    e_current = e_next.copy()
    
    im2.set_data(e_current)
    return [im2]

# Create Animation
print("Generating fiber animation...")
# 500 Frames to show bouncing
anim = FuncAnimation(fig, update, frames=450, interval=20, blit=True)

# Ensure images dir exists
os.makedirs("images", exist_ok=True)

# Save as MP4
mp4_path = os.path.join("images", "fiber_simulation.mp4")
try:
    anim.save(mp4_path, writer=FFMpegWriter(fps=30), dpi=100)
    print(f"Saved MP4: {mp4_path}")
except Exception as e:
    print(f"FFmpeg not found or error saving MP4: {e}. Skipping MP4.")
    
# Standard PNG fallback
plt.savefig('images/fiber_simulation.png')

# Save GIF
gif_path = os.path.join("images", "fiber_simulation.gif")
print(f"Saving GIF to {gif_path}...")
anim.save(gif_path, writer=PillowWriter(fps=30))
print("GIF saved.")

plt.close(fig)
print("Done.")
