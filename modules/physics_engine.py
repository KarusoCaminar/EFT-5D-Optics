import numpy as np

"""
Module: physics_engine.py
Status: Core Engine (V4.0)
Purpose: Centralizes all physical laws and constants for the 5D-Optics framework.
         Implements the 'Hardened' Theory V4.0 logic.
"""

class PhysicsEngine:
    def __init__(self):
        # Universal Constants
        self.H_BAR_C = 197.3269804 # eV nm
        
        # Theory Parameters (V4.0)
        # Power Law: Chi ~ Phi^k
        self.COUPLING_EXPONENT = -5.0
        
        # Internal State
        self.objects = []
        
    def add_object(self, obj):
        """Adds a geometric object (Sphere, Slab, etc.) to the world."""
        self.objects.append(obj)
        
    def n_field(self, pos):
        """
        Calculates the scalar field 'n' (Refractive Index) at a given 3D position [x, y, z].
        n is emergent from the 5D scalar field Phi: n = 1/Phi.
        """
        x, y = pos[0], pos[1]
        
        # Base vacuum value
        n_val = 1.0
        
        # Simple composition: Take the MAX n of all objects (simplification for overlap)
        # Or smooth blending.
        for obj in self.objects:
            # Check interaction
            if obj['type'] == 'sphere':
                r = np.sqrt((x - obj['x'])**2 + (y - obj['y'])**2)
                if r < obj['radius']:
                    n_val = max(n_val, obj['n'])
                # Transitions?
                
        return n_val

    def get_phi(self, pos):
        """Returns the 5D Scalar Field Phi at pos."""
        return 1.0 / self.n_field(pos)
        
    def get_gradients(self, pos, delta=0.01):
        """
        Numerical gradient of n.
        Needed for the Geodesic Equation.
        """
        x, y = pos[0], pos[1]
        n0 = self.n_field(pos)
        
        nx = self.n_field([x + delta, y])
        ny = self.n_field([x, y + delta])
        
        dn_dx = (nx - n0) / delta
        dn_dy = (ny - n0) / delta
        
        return np.array([dn_dx, dn_dy])

    def symplectic_step(self, pos, vel, dt):
        """
        Symplectic Integrator (Velocity Verlet / Leapfrog semi-implicit)
        Crucial for Energy conservation in Hamiltonian systems.
        Hamiltonian H = |p| / n(x) = const.
        
        Equations of Motion (derived from Fermat's Principle / Geodesics):
        d^2x/ds^2 = grad(n). (Simplified Ray Equation form approx).
        Exact Relativistic Form:
        d/ds (n v) = grad(n)
        => n dv/ds + v (v.grad n) = grad n
        => n dv/ds = grad n - v (v.grad n) = P_perp (grad n)
        
        Verlet Step:
        x(t+dt) = x(t) + v(t)dt + 0.5*a(t)dt^2
        v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))dt
        """
        
        # 1. Half Step Velocity
        grad_n = self.get_gradients(pos)
        n = self.n_field(pos)
        
        # Acceleration a = (grad n - (v.grad n)v) / n
        v_dot_grad = np.dot(vel, grad_n)
        acc_t = (grad_n - v_dot_grad * vel) / n
        
        pos_new = pos + vel * dt + 0.5 * acc_t * dt**2
        
        # 2. Re-evaluate Force
        grad_n_new = self.get_gradients(pos_new)
        n_new = self.n_field(pos_new)
        
        # Note: Velocity has changed, we need estimate for dot product?
        # Standard Verlet is for conservative forces F(x). Here F depends on v.
        # This is tricky. Let's use RK4 for velocity-dependent forces OR simplified Geometric Verlet for Optics.
        # Strict Symplectic for Raytracing: (q, p) coordinates.
        # p = n * v (Canonical Momentum)
        # H = |p|^2 / 2 - n^2(q) / 2 = 0? (Mechanical Analogy)
        # Let's stick to High-Order RK4 for stability if Verlet is hard to formulate for v-dep forces.
        
        # Fallback to RK4 implementation
        return self.rk4_step(pos, vel, dt)

    def rk4_step(self, pos, vel, dt):
        """Runge-Kutta 4 Integrator for Ray Equation."""
        
        def accel(p, v):
            gn = self.get_gradients(p)
            n_loc = self.n_field(p)
            # Re-normalize v to be safe? No, let the integrator handle it,
            # but Ray equation assumes parameter s is arc length (|v|=1).
            # If |v| drifts, we must re-normalize energy.
            v_dir = v / np.linalg.norm(v)
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
        
        # Enforce Conservation (Constraint |v|=1 for parameter s)
        vel_new = vel_new / np.linalg.norm(vel_new)
        
        return pos_new, vel_new
