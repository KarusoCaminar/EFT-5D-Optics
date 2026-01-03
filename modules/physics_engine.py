import numpy as np

"""
Module: physics_engine.py
Status: Core Engine (V4.2 - Universal)
Purpose: Centralizes all physical laws and constants for the 5D-Optics framework.
         Implements the 'Hardened' Theory V4.0 logic with improved numerical stability.
"""

class PhysicsEngine:
    def __init__(self):
        # Universal Constants
        self.H_BAR_C = 197.3269804 # eV nm
        
        # Theory Parameters (V4.0)
        # Power Law: Chi ~ Phi^k
        self.COUPLING_EXPONENT = -5.0
        
        # Universal Calibration (V4.2 - Silicon Gauge Fixing)
        # Sets the energy scale such that Silicon (n=3.42) has Resonance N=0.5
        # Previous legacy value was ~73 (based on Saphir).
        self.SCALING_FACTOR_K = 63.5
        
        # Internal State
        self.objects = []
        
    def add_object(self, obj):
        """Adds a geometric object (Sphere, Slab, etc.) to the world."""
        self.objects.append(obj)
        
    def n_field(self, pos):
        """
        Calculates the scalar field 'n' (Refractive Index) at a given 3D position [x, y, z].
        n is emergent from the 5D scalar field Phi: n = 1/Phi.
        Default implementation uses added objects.
        """
        x, y = pos[0], pos[1]
        
        # Base vacuum value
        n_val = 1.0
        
        # Simple composition: Take the MAX n of all objects (simplification for overlap)
        for obj in self.objects:
            if obj['type'] == 'sphere':
                r = np.sqrt((x - obj['x'])**2 + (y - obj['y'])**2)
                if r < obj['radius']:
                    n_val = max(n_val, obj['n'])
                # Transitions can be handled by custom sources
                
        return n_val

    def set_n_field_source(self, source_func):
        """
        Sets a custom source for the refractive index field.
        Replaces 'monkey patching' with a proper interface, allowing complex simulations
        to override the default object list.
        """
        # We bind the method to the instance
        self.n_field = source_func

    def get_phi(self, pos):
        """Returns the 5D Scalar Field Phi at pos."""
        return 1.0 / self.n_field(pos)
        
    def get_gradients(self, pos, delta=1e-3):
        """
        Numerical gradient of n.
        Needed for the Geodesic Equation.
        'delta' should be small relative to feature size.
        """
        x, y = pos[0], pos[1]
        n0 = self.n_field(pos)
        
        # We use a central difference for higher accuracy? 
        # Or just finer forward/backward. 
        # Standard forward diff with small delta:
        nx = self.n_field([x + delta, y])
        ny = self.n_field([x, y + delta])
        
        dn_dx = (nx - n0) / delta
        dn_dy = (ny - n0) / delta
        
        return np.array([dn_dx, dn_dy])

    def symplectic_step(self, pos, vel, dt):
        """
        Symplectic Integrator wrapper.
        Currently defaults to RK4 for stability with velocity-dependent forces.
        """
        return self.rk4_step(pos, vel, dt)

    def rk4_step(self, pos, vel, dt):
        """Runge-Kutta 4 Integrator for Ray Equation (Geodesic)."""
        
        # Adaptive delta heuristic:
        # If dt is very small, we might be in a high precision zone, so we use finer gradients.
        grad_delta = 1e-4 if dt < 0.05 else 1e-3

        def accel(p, v):
            gn = self.get_gradients(p, delta=grad_delta)
            n_loc = self.n_field(p)
            v_dir = v / np.linalg.norm(v)
            # Geodesic Equation for Optics:
            # d/ds(n v) = grad n  =>  n a + (v.grad n)v = grad n
            # a = (grad n - (v.grad n)v) / n
            vdg = np.dot(v_dir, gn)
            a = (gn - vdg * v_dir) / n_loc
            return a

        # k1
        k1_v = accel(pos, vel) * dt
        k1_p = vel * dt
        
        # k2
        k2_v = accel(pos + 0.5*k1_p, vel + 0.5*k1_v) * dt
        k2_p = (vel + 0.5*k1_v) * dt
        
        # k3
        k3_v = accel(pos + 0.5*k2_p, vel + 0.5*k2_v) * dt
        k3_p = (vel + 0.5*k2_v) * dt
        
        # k4
        k4_v = accel(pos + k3_p, vel + k3_v) * dt
        k4_p = (vel + k3_v) * dt
        
        vel_new = vel + (k1_v + 2*k2_v + 2*k3_v + k4_v) / 6.0
        pos_new = pos + (k1_p + 2*k2_p + 2*k3_p + k4_p) / 6.0
        
        # Enforce |v| = 1 conservation (optional but good for stability)
        vel_new = vel_new / np.linalg.norm(vel_new)
        
        return pos_new, vel_new
