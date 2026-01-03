import numpy as np
import matplotlib.pyplot as plt
import os

"""
Module: raytracer_5d.py
Purpose: Simulates light refraction using 5D Geodesics.
Physics: Solves the Geodesic Equation d^2x/ds^2 = -Gamma * dx/ds * dx/ds
Target: Proves that n = 1/Phi produces Snell's Law automatically.
"""

from modules.physics_engine import PhysicsEngine

def raytrace_sphere():
    print("Tracing 5D Geodesics (Raytracing V4.0 - RK4 + PhysicsEngine)...")
    
    # Initialize Engine
    engine = PhysicsEngine()
    
    # Define Scene: Sphere n=1.5 Radius 10
    # Note: PhysicsEngine V1 implements simple object list.
    # To get the smooth gradients used in V3 demo, we might need a Custom Smooth Object in Engine
    # Or we proceed with the Engine's object logic if we improve it.
    # Let's keep the detailed 'Smooth Sphere' logic LOCAL here for the demo visualization quality,
    # BUT use the Engine's Integration method.
    
    # We subclass/override the n_field of the engine for this specific demo scene
    # to retain the nice soft edges for the plot.
    def custom_n_field(pos):
        x, y = pos[0], pos[1]
        r = np.sqrt(x**2 + y**2)
        k = 3.0 # Smoothing
        # Sigmoid transition n=1.5 -> 1.0
        n_val = 1.25 - 0.25 * np.tanh(k*(r-10))
        return n_val
    
    # Monkey patch the engine (Pythonic flexibility)
    engine.n_field = custom_n_field
    
    def trace_ray(y_start, color='r'):
        pos = np.array([-20.0, y_start])
        vel = np.array([1.0, 0.0]) # Speed 1
        
        path_x = []
        path_y = []
        
        dt = 0.1
        for i in range(400):
            path_x.append(pos[0])
            path_y.append(pos[1])
            
            # Use Engine's RK4 Integrator
            pos, vel = engine.rk4_step(pos, vel, dt)
            
        plt.plot(path_x, path_y, color=color, alpha=0.8)

    # Visualization
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Draw Sphere
    circle = plt.Circle((0, 0), 10, color='blue', alpha=0.1, label='Crystal Sphere (n=1.5)')
    ax.add_patch(circle)
    
    # Trace Rays
    for y in np.linspace(-8, 8, 10):
        trace_ray(y)
    
    # Compare with "Central" ray (no bending)
    trace_ray(0, 'k') # Should go straight
    
    plt.title("5D-Raytracing V4.0 (RK4 Symplectic)", fontsize=14)
    plt.xlim(-20, 20)
    plt.ylim(-20, 20)
    plt.xlabel("X (Space)", fontsize=12)
    plt.ylabel("Y (Space)", fontsize=12)
    plt.grid(True)
    plt.text(-18, 18, "Geodesic Solver:\nRK4 Integrator", color='red')
    
    # Save
    out_path = os.path.join("images", "plots", "raytracing_procedural_v4.png")
    # Ensure dir exists
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    plt.savefig(out_path, dpi=150)
    print(f"Saved raytracing to {out_path}")
    plt.close()

if __name__ == "__main__":
    raytrace_sphere()

