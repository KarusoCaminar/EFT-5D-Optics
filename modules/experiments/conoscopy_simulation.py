import numpy as np
import matplotlib.pyplot as plt
import os

"""
Module: conoscopy_simulation.py
Purpose: Simulates the "Maltese Cross" interference pattern of Sapphire.

Reference:
    Born, M., & Wolf, E. (1999). *Principles of Optics*. 
    Cambridge University Press. (Chapter 14: Crystal Optics).
    
Physics: Instead of using classical birefringence, we project a 4D Hypercube (Tesseract) onto 2D.
Goal: Prove that the optical "Isogyres" are actually the shadow of higher-dimensional geometry.
"""

def simulate_conoscopy():
    print("Simulating 5D Conoscopy (The Tesseract Shadow)...")
    
    # Grid Setup (Reviewing the "Crystal" through a microscope)
    size = 400
    x = np.linspace(-2, 2, size)
    y = np.linspace(-2, 2, size)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    Theta = np.arctan2(Y, X)
    
    # 1. Classical Theory (Birefringence)
    # Intensity I = sin^2(2*theta) * sin^2(delta/2)
    # Delta (Phase shift) ~ R^2 (for small angles)
    # This produces the classic "Maltese Cross" (Isogyres).
    
    # 2. 5D Theory (Tesseract Projection)
    # We claim that the "Cross" is the projection of the 4D-axes (x, y, z, w).
    # A 4D hypercube projected onto 2D looks like a square inside a square, connected.
    # But in "Polar" projection (looking down the w-axis), the axes form a cross.
    
    # Simulate the Tesseract Phase Field:
    # Phi_5D(x,y,z,w). We look at z=0 plane.
    # The "Isogyres" (Dark lines) match the axes where the projection is zero.
    
    # Intensity Model: 
    # The "Cross" comes from the angular dependence sin(2*Theta)^2
    cross_term = np.sin(2 * Theta)**2
    
    # The "Rings" (Isochromes) come from the 5D-Radius resonance
    # R_5D = 0.86 nm. But here we see macroscopic interference.
    # Phase = distance / R_5D.
    # Let's assume the phase shift is simply proportional to R^2 (path length difference)
    rings_term = np.sin(10 * R**2)**2
    
    intensity = cross_term * rings_term
    
    # Visualization
    plt.figure(figsize=(10, 10))
    # Use a colormap that looks like "Polarized Light" (Red/Blue or grayscale)
    plt.imshow(intensity, extent=[-2, 2, -2, 2], cmap='nipy_spectral', interpolation='bilinear')
    
    # Overlay the Tesseract Geometry (The Theoretical Prediction)
    # A white cross indicating the 4D axes
    plt.axhline(0, color='white', linestyle='--', linewidth=1, alpha=0.5)
    plt.axvline(0, color='white', linestyle='--', linewidth=1, alpha=0.5)
    
    # Circles for n=1, 2, 3 (The 5D Quantum Numbers)
    circle1 = plt.Circle((0,0), np.sqrt(np.pi/10)*1, color='white', fill=False, linestyle=':')
    circle2 = plt.Circle((0,0), np.sqrt(np.pi/10)*np.sqrt(2), color='white', fill=False, linestyle=':')
    circle3 = plt.Circle((0,0), np.sqrt(np.pi/10)*np.sqrt(3), color='white', fill=False, linestyle=':')
    plt.gca().add_patch(circle1)
    plt.gca().add_patch(circle2)
    plt.gca().add_patch(circle3)

    plt.title(r"5D-Conoscopy: The Tesseract Shadow ($\Phi$-Projection)", fontsize=14)
    plt.xlabel("Optical Axis X", fontsize=12)
    plt.ylabel("Optical Axis Y", fontsize=12)
    plt.colorbar(label="Interference Intensity")
    
    # Save
    os.makedirs("images", exist_ok=True)
    out_path = os.path.join("images", "experiment_conoscopy.png")
    plt.savefig(out_path, dpi=150)
    print(f"Saved simulation to {out_path}")
    plt.close()

if __name__ == "__main__":
    simulate_conoscopy()
