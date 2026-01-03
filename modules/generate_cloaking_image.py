import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
import os

"""
Module: generate_cloaking_image.py
Purpose: Generates visual assets (GIF/MP4) for the 5D Cloaking Simulation.
This script runs the FDTD simulation non-interactively and saves the output
to the 'images/' directory for inclusion in the final report.
"""


# Configure FFmpeg Path explicitly
ffmpeg_path = r"C:\Users\Moritz\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"
plt.rcParams['animation.ffmpeg_path'] = ffmpeg_path

# --- Physik-Engine (FDTD) ---
SIZE = 200
phi_field = np.ones((SIZE, SIZE))
e_field = np.zeros((SIZE, SIZE))

center = SIZE // 2
R_inner = 20
R_outer = 40

y, x = np.ogrid[:SIZE, :SIZE]
r = np.sqrt((x - center)**2 + (y - center)**2)

# Tarnkappen-Design (Gradient)
mask_ring = (r >= R_inner) & (r <= R_outer)
phi_field[mask_ring] = 0.5 + 0.5 * (r[mask_ring] - R_inner) / (R_outer - R_inner)

mask_core = r < R_inner
phi_field[mask_core] = 0.0 # Absorber

# Arrays for simulation
e_current = np.zeros((SIZE, SIZE))
e_prev = np.zeros((SIZE, SIZE))
e_next = np.zeros((SIZE, SIZE))

# Parameter
c = 1.0
dt = 0.5
dx = 1.0

# Setup Plot
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Geometry
im1 = ax1.imshow(phi_field, cmap='gray', vmin=0, vmax=1.2)
ax1.set_title(r"Das $\Phi$-Feld (Die Tarnkappe)")
circle1 = plt.Circle((center, center), R_inner, color='r', fill=False)
circle2 = plt.Circle((center, center), R_outer, color='b', fill=False)
ax1.add_patch(circle1)
ax1.add_patch(circle2)
ax1.text(center, center, "HIDDEN", color='red', ha='center', va='center')

# Plot 2: Field
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
    
    # Quelle
    e_next[:, 5] = np.sin(frame * 0.2)
    
    # Update
    e_prev = e_current.copy()
    e_current = e_next.copy()
    
    im2.set_data(e_current)
    return [im2]

# Create Animation
print("Generating animation (this may take a minute)...")
anim = FuncAnimation(fig, update, frames=450, interval=30, blit=True)

# Ensure images dir exists
os.makedirs("images", exist_ok=True)

# Save GIF
gif_path = os.path.join("images", "cloaking_simulation.gif")
print(f"Saving GIF to {gif_path}...")
anim.save(gif_path, writer=PillowWriter(fps=30))
print("GIF saved.")

# Save MP4 (Try/Except in case ffmpeg is not available)
mp4_path = os.path.join("images", "cloaking_simulation.mp4") # Save as MP4
try:
    anim.save(mp4_path, writer='ffmpeg', fps=30, dpi=100)
    print(f"Saved MP4: {mp4_path}")
except Exception as e: # Catch specific exception for ffmpeg writer
    print("FFmpeg not found. Skipping MP4 using default writer.")
    try:
        # Fallback to FFMpegWriter if 'ffmpeg' string writer fails
        anim.save(mp4_path, writer=FFMpegWriter(fps=30))
        print("MP4 saved using FFMpegWriter.")
    except Exception as e_fallback:
        print(f"Could not save MP4 (ffmpeg might be missing or other error): {e_fallback}")

plt.savefig('images/cloaking_simulation_result.png')

plt.close(fig)
print("Done.")
