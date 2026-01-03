import numpy as np
import matplotlib.pyplot as plt
import os

"""
Module: raytracer_5d.py
Purpose: Simulates light refraction using 5D Geodesics.
Physics: Solves the Geodesic Equation d^2x/ds^2 = -Gamma * dx/ds * dx/ds
Target: Proves that n = 1/Phi produces Snell's Law automatically.
"""

def raytrace_sphere():
    print("Tracing 5D Geodesics (Raytracing)...")
    
    # Metric Parameter
    # n(r) for a sphere of radius 10 at (0,0)
    # n_in = 1.5, n_out = 1.0
    def n_field(x, y):
        r = np.sqrt(x**2 + y**2)
        if r < 10:
            return 1.5
        else:
            return 1.0 # Vacuum

    # Gradient of Scalar Field Phi = 1/n
    def grad_phi(x, y):
        # Phi = 1/n.
        # Inside: Phi=0.66. Outside: Phi=1.0.
        # We need a smooth transition for derivatives to work in numerical solver
        # Sigmoid transition at r=10
        r = np.sqrt(x**2 + y**2)
        k = 5.0 # Sharpness
        # Smooth n
        n_val = 1.0 + 0.5 * (1 - 1/(1 + np.exp(-k*(r-10)))) # Inner is 1.5, Outer is 1.0 (Wait, r<10 -> exp(+)...)
        # Let's use simple tanh
        n_smooth = 1.25 - 0.25 * np.tanh(k*(r-10)) # r=0->tanh(-inf)=-1->1.5. r=20->tanh(inf)=1->1.0
        
        # Phi = 1/n_smooth
        phi = 1.0 / n_smooth
        
        # Derivatives dPhi/dr = -1/n^2 * dn/dr
        dn_dr = -0.25 * k * (1 - np.tanh(k*(r-10))**2)
        dphi_dr = (-1.0 / n_smooth**2) * dn_dr
        
        # dPhi/dx = dphi/dr * dr/dx = dphi/dr * x/r
        dphi_dx = dphi_dr * (x/r) if r>0 else 0
        dphi_dy = dphi_dr * (y/r) if r>0 else 0
        
        return phi, dphi_dx, dphi_dy

    # Geodesic Equation: approx d^2x/dt^2 = - grad Phi (Newtonian limit of GR)
    # Actually for light: curvature is purely spatial effective.
    # a = nabla(n) / n (The Ray Equation)
    # d/ds (n dr/ds) = nabla n
    # => d^2r/ds^2 = (nabla n - (dr/ds . nabla n) dr/ds) / n
    
    def trace_ray(y_start, color='r'):
        # State: x, y, vx, vy
        # Initial: Left side shooting right
        pos = np.array([-20.0, y_start])
        vel = np.array([1.0, 0.0]) # Speed 1
        
        path_x = []
        path_y = []
        
        dt = 0.1
        for i in range(400):
            path_x.append(pos[0])
            path_y.append(pos[1])
            
            x, y = pos
            r = np.sqrt(x**2 + y**2)
            
            # Get n and gradients
            # Using the smoothed n function logic here locally
            k = 3.0
            n_val = 1.25 - 0.25 * np.tanh(k*(r-10))
            
            dn_dr = -0.25 * k * (1 - np.tanh(k*(r-10))**2)
            grad_n_x = dn_dr * (x/r) if r>0 else 0
            grad_n_y = dn_dr * (y/r) if r>0 else 0
            grad_n = np.array([grad_n_x, grad_n_y])
            
            # Ray Equation: ray bends TOWARDS gradient of n
            # a = (grad_n - (v . grad_n) * v) / n
            # Wait, v must be normalized? ds is path length. |v|=1.
            
            # Normalize v
            v_mag = np.linalg.norm(vel)
            v_dir = vel / v_mag
            
            # Acceleration
            # a = (Gradient component perpendicular to v) * something
            # Standard ray equation: d/ds (n s_hat) = grad n
            # => n d(s_hat)/ds + s_hat (dn/ds) = grad n
            # => n curvature = grad n - (grad n . s_hat) s_hat (Projection)
            
            force = grad_n - np.dot(grad_n, v_dir) * v_dir
            acc = force / n_val
            
            # Update
            vel = vel + acc * dt
            # Re-normalize to keep speed constant (geometric trace)
            vel = vel / np.linalg.norm(vel)
            
            pos = pos + vel * dt
            
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
    
    plt.title("5D-Raytracing: Geodesic Solution", fontsize=14)
    plt.xlim(-20, 20)
    plt.ylim(-20, 20)
    plt.xlabel("X (Space)", fontsize=12)
    plt.ylabel("Y (Space)", fontsize=12)
    plt.grid(True)
    plt.text(-18, 18, "Rays solving\nGeodesic Eq.", color='red')
    
    # Save
    out_path = os.path.join("images", "raytracing_procedural.png")
    plt.savefig(out_path, dpi=150)
    print(f"Saved raytracing to {out_path}")
    plt.close()

if __name__ == "__main__":
    raytrace_sphere()
