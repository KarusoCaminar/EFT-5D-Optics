import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

"""
Module: 5d_wave_simulation.py
Purpose: Visualize Light not as vectors, but as Metric Distortion (Kaluza-Klein).
Theory: The E-field is a non-diagonal metric term G_05 (or A_mu). 
        An EM wave is a propagating "shear" or "twist" of the 5D geometry.
"""

def simulate_geometric_light():
    print("Simulating 5D Geometric Light Wave...")

    # Space-Time Grid
    x = np.linspace(0, 4*np.pi, 100)
    
    # 1. Classical Physics: The E-field Vector
    # E(x,t) = E0 * sin(k*x - w*t)
    wavelength = 2*np.pi
    k = 2*np.pi / wavelength
    omega = 1.0 # arbitrary speed
    
    # Setup Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    plt.subplots_adjust(hspace=0.4)
    
    # Static Holders for animation
    line_classic, = ax1.plot([], [], 'b-', lw=2, label='E-Field Vector (Classic)')
    ax1.set_title("Standard Physics: Light as a Vector Field (E)", fontsize=12)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_xlim(0, 4*np.pi)
    ax1.grid(True)
    ax1.legend(loc='upper right')
    
    # 2. 5D Physics: The Metric Shear
    # In KK theory, A_mu corresponds to the "tilt" of the 5th dimension fiber.
    # We visualize the 5th dimension as small "needles" or fibers attached to space.
    # The wave twists these fibers.
    
    # Create a grid of "Fibers" (Points in x)
    fiber_x = np.linspace(0, 4*np.pi, 25) 
    # Initialize quiver with dummy data to establish shapes
    Y_origin = np.zeros_like(fiber_x)
    U_init = np.zeros_like(fiber_x)
    V_init = np.ones_like(fiber_x)
    
    quiver = ax2.quiver(fiber_x, Y_origin, U_init, V_init, scale=20, color='r', label='5D-Fiber Tilt (Metric)')
    
    ax2.set_title("5D-Theory: Light as Geometric Torsion (Frame Dragging)", fontsize=12)
    ax2.set_ylim(-1, 1)
    ax2.set_xlim(0, 4*np.pi)
    ax2.set_yticks([])
    ax2.text(0.5, -0.2, "The 'E-Field' is physically the tilt angle of the 5th Dimension", 
             transform=ax2.transAxes, ha='center', fontsize=10, color='gray')

    def init():
        line_classic.set_data([], [])
        # Reset quiver to vertical
        quiver.set_UVC(np.zeros_like(fiber_x), np.ones_like(fiber_x))
        return line_classic, quiver

    def update(frame):
        t = frame * 0.1
        
        # Classical
        y_classic = np.sin(k*x - omega*t)
        line_classic.set_data(x, y_classic)
        
        # 5D Geometric
        E_local = np.sin(k*fiber_x - omega*t)
        
        # Vector components
        U = E_local * 0.5 
        V = np.ones_like(U)
        
        quiver.set_UVC(U, V)
        return line_classic, quiver

    ani = FuncAnimation(fig, update, frames=100, init_func=init, blit=False)
    
    # Save one frame as static image for the user
    # (Since we can't display video easily here, we save a representative frame)
    init()
    update(15) # Freeze at t=1.5
    
    os.makedirs("images", exist_ok=True)
    out_path = os.path.join("images", "light_as_geometry.png")
    plt.savefig(out_path, dpi=150)
    print(f"Saved visualization to {out_path}")
    plt.close()

if __name__ == "__main__":
    simulate_geometric_light()
