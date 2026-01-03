import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter, FFMpegWriter
from itertools import combinations
import os

# Configure FFmpeg Path explicitly
ffmpeg_path = r"C:\Users\Moritz\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"
plt.rcParams['animation.ffmpeg_path'] = ffmpeg_path

# --- 1. Tesserakt Geometrie (4D) ---
def create_tesseract():
    # Ein Tesserakt hat 16 Ecken (+/-1, +/-1, +/-1, +/-1)
    points = []
    for x in [-1, 1]:
        for y in [-1, 1]:
            for z in [-1, 1]:
                for w in [-1, 1]:
                    points.append([x, y, z, w])
    return np.array(points)

# Verbindungen (Kanten) zwischen den Ecken
def get_edges(points):
    edges = []
    # Zwei Punkte sind verbunden, wenn sie sich nur in 1 Koordinate unterscheiden
    for i, p1 in enumerate(points):
        for j, p2 in enumerate(points):
            if i < j:
                diff = np.sum(np.abs(p1 - p2))
                if np.isclose(diff, 2): # Abstand 2 bedeutet, nur 1 Koordinate ist anders
                    edges.append((i, j))
    return edges

# --- 2. 4D Rotations-Matrizen ---
def rotate_xw(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, 0, 0, -s],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [s, 0, 0, c]
    ])

def rotate_zw(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, c, -s],
        [0, 0, s, c]
    ])

# --- 3. Projektion 4D -> 3D ---
# Stereographische oder einfache perspektivische Projektion
def project_4d_to_3d(points_4d, d=2):
    points_3d = []
    for p in points_4d:
        w = p[3]
        scale = 1 / (d - w) if d != w else 1
        points_3d.append(p[:3] * scale) # x, y, z skaliert
    return np.array(points_3d)

# --- 4. Projektion 3D -> 2D (für den Bildschirm) ---
def project_3d_to_2d(points_3d):
    return points_3d[:, :2] # Einfach x, y nehmen (orthographisch)

# --- 5. Animation ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.axis('off') # Kein Rahmen, nur reine Geometrie
plt.title("Schatten der 5. Dimension: Tesserakt -> Hexagon", fontsize=14)

tesseract_points = create_tesseract()
edges = get_edges(tesseract_points)

# Linien-Objekte für den Plot
lines = [ax.plot([], [], 'k-', alpha=0.6, linewidth=1.5)[0] for _ in edges]
points_plot, = ax.plot([], [], 'ro', markersize=4)

def update(frame):
    angle = frame * 0.02
    
    # 1. Rotation im 4D Raum (Das ist die "Physik" der 5. Dimension)
    # Wir rotieren in zwei Ebenen gleichzeitig für komplexe Schatten
    rotated_points = tesseract_points @ rotate_xw(angle).T @ rotate_zw(angle * 0.5).T
    
    # 2. Projektion auf 3D (Der Übergang in unsere Welt)
    projected_3d = project_4d_to_3d(rotated_points, d=3)
    
    # 3. Drehung des 3D-Objekts (Kamera-Perspektive)
    # Wir schauen "Kante-voran" (Edge-First) um Hexagone zu sehen
    # Das simulieren wir durch Projektion auf 2D
    projected_2d = project_3d_to_2d(projected_3d)
    
    # Zeichnen
    points_plot.set_data(projected_2d[:, 0], projected_2d[:, 1])
    
    for line, edge in zip(lines, edges):
        p1 = projected_2d[edge[0]]
        p2 = projected_2d[edge[1]]
        line.set_data([p1[0], p2[0]], [p1[1], p2[1]])
        
        # Farbe je nach "Tiefe" (w-Koordinate) ändern
        # Das visualisiert die 4. Dimension durch Farbe
        depth = rotated_points[edge[0], 3]
        color_val = (depth + 1.5) / 3 # Normalisieren 0..1
        color_val = np.clip(color_val, 0, 1)
        line.set_color(plt.cm.viridis(color_val))

    return lines + [points_plot]

def init():
    """Initialize animation state - ensures animation starts from frame 0."""
    points_plot.set_data([], [])
    for line in lines:
        line.set_data([], [])
    return lines + [points_plot]

print("Generiere Animation... (Das kann paar Sekunden dauern)")
anim = FuncAnimation(fig, update, frames=200, interval=20, blit=True, init_func=init)

# Save as GIF for documentation
try:
    anim.save('tesseract_projection.gif', writer='pillow', fps=30)
    print("Animation saved to 'tesseract_projection.gif'")
except Exception as e:
    print(f"Could not save GIF: {e}")

# Save as MP4
try:
    anim.save('tesseract_projection.mp4', writer=FFMpegWriter(fps=30), dpi=100)
    print("Animation saved to 'tesseract_projection.mp4'")
except Exception as e:
    print(f"Could not save MP4: {e}")

print("Beobachte: In bestimmten Winkeln formt der Schatten ein perfektes HEXAGON.")
print("Das ist der Moment, in dem die 5D-Geometrie als Graphen-Gitter sichtbar wird.")

import sys

if __name__ == "__main__":
    if "--batch" not in sys.argv:
        plt.show()
    else:
        print("Batch mode: Skipping window display.")
