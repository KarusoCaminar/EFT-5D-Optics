import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""
Module: multi_material_validator.py
Purpose: Scientific Hardening of the 5D-Optics Theory (Version 4.0)
Method: 
    1. Calculate effective UV-Mass (m_eff) from Sellmeier Dispersion Data.
    2. Calculate theoretical 5D-Radius R_5D = h_bar * c / m_eff.
    3. Compare R_5D with physical Lattice Constant 'a'.
    4. Check for 'Geometric Locking' (Integer/Rational ratios).

Hypothesis: If the theory holds, R_5D / a should be close to a simple rational number (Resonance).
"""

# Physical Constants
H_BAR_C = 197.3269804  # eV * nm

# Material Database
# Sources: Malitson, Peter, Edwards, etc. (Standard Refractive Index Data)
# Sellmeier format: n^2 - 1 = Sum( B_i * lambda^2 / (lambda^2 - C_i) )
# We form effective single-pole mass from the dominant UV term (B1/C1 implies mean energy).
# Or better: We fit a single-pole Sellmeier n^2 - 1 = B / (1 - (lambda_0/lambda)^2) to the data in transparency range.
# Lambda_0 corresponds to Energy E = h*c / lambda_0.

materials = {
    "Sapphire (Al2O3)": {
        "lattice_a": 0.4758, # nm (trigonal a-axis)
        # Sellmeier (Malitson): UV pole around 0.072 microns ~ 17 eV? 
        # But we use the effective mass from V3.0 fit: 229 eV (Collective mode)
        # Let's re-evaluate strictly from coefficients if possible, but for now use V3.0 fit value to reproduce baseline.
        "m_eff_fit": 229.0, 
        "color": "blue"
    },
    "Diamond (C)": {
        "lattice_a": 0.3567, # nm (cubic)
        # Peter 1923: n approx 2.41. 
        # UV cut-off ~ 225nm (5.5 eV).
        # Let's perform a rough Effective Mass calc: 
        # Average n ~ 2.4 -> Chi ~ 4.76.
        # Energy E_eff for diamond is usually high (plasmon approx 30eV?).
        # Let's set a placeholder calculated from n=2.41 and dispersion...
        # A clearer approach: effective single oscillator E_0.
        # For Diamond, E_0 is roughly 17 eV (Wemple-DiDomenico parameter).
        # Wait, if we use the V3.0 logic: m_eff determined dispersion curvature.
        # Let's aim to Run the calculation logic inside the script if possible.
        # For this script v1, we assume we need to FIND m_eff that fits n(lambda).
        "sellmeier_coeffs": [4.3356, 0.3306**2, 0.3306], # Dummy structure, need real coeffs
        # Real coeffs (Edwards 1981 via RefractiveIndex.info):
        # n^2 - 1 = 4.3356 * lambda^2 / (lambda^2 - 0.1060^2) + ...
        # The UV pole is at 106 nm.
        "uv_pole_lambda": 0.1060, # microns
        "color": "cyan"
    },
    "Silicon (Si)": {
        "lattice_a": 0.5431, # nm
        # Herzberger 1957.
        # UV pole approx at 300nm? Si is opaque in visible. IR material.
        # Pole is effectively the bandgap/interband center ~ 3.4 eV? 
        # Or proper oscillator at 0.28 um?
        "uv_pole_lambda": 0.29, # rough estimate for single pole dominant term
        "color": "grey"
    },
    "Quartz (SiO2)": {
        "lattice_a": 0.4913, # nm
        # Malitson 1965.
        # B1=0.696, C1=0.06840^2 (68 nm).
        "uv_pole_lambda": 0.092, # Weighted UV avg
        "color": "purple"
    },
    "Zinc Sulfide (ZnS)": {
        "lattice_a": 0.5409, # nm
        # Debenham 1984
        "uv_pole_lambda": 0.200, # Approx
        "color": "green"
    }
}

def calculate_energy(wavelength_microns):
    """Converts wavelength (microns) to Energy (eV). E = 1239.8 / lambda_nm"""
    if wavelength_microns is None: return None
    lambda_nm = wavelength_microns * 1000
    return 1239.84193 / lambda_nm

def run_validation():
    print("--- 5D-Optics Multi-Material Validator (V4.0) ---")
    print(f"{'Material':<20} | {'a [nm]':<8} | {'UV-Pole [eV]':<12} | {'R_5D [nm]':<10} | {'Ratio (R/a)':<10} | {'Locking?'}")
    print("-" * 90)

    results = []

    for name, data in materials.items():
        a = data['lattice_a']
        
        # 2. HYPOTHESIS B: Bulk Plasmon Energy (Electron Density)
        # Instead of arbitrary UV pole scaling, we use the fundamental plasma frequency.
        # This represents the "stiffness" of the electron gas against the 5D metric.
        
        # Approximate Bulk Plasmon Energies (Experimental values from EELS)
        plasmon_energies = {
            "Sapphire (Al2O3)": 22.5, # approx 22-24 eV
            "Diamond (C)": 33.0,      # approx 33-34 eV
            "Silicon (Si)": 16.7,     # 16.7 eV (Standard reference)
            "Quartz (SiO2)": 22.0,    # approx 21-23 eV
            "Zinc Sulfide (ZnS)": 15.5 # approx 15-16 eV
        }
        
        e_plasmon = plasmon_energies.get(name, 20.0) # Default 20
        
        # We assume the 5D Mass is directly the Plasmon Energy (or a simple multiple).
        # Let's test m_phi = E_plasmon * 10 (Just to see raw ratio order of magnitude)
        # Wait, let's look at Sapphire V3.0: Mass=229. Plasmon=22.5. Ratio ~ 10.1
        # Let's try Scaling Factor = 10.17 (derived from Sapphire 229/22.5) for ALL.
        
        scaling_factor = 229.0 / 22.5 # ~ 10.177
        m_eff = e_plasmon * scaling_factor

        # 2. Calculate 5D Radius
        # R = h_bar * c / m
        r_5d = H_BAR_C / m_eff

        # 3. Ratio
        ratio = r_5d / a
        
        # 4. Locking Check (Is it close to int or x.5?)
        is_locked = "NO"
        candidates = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
        match = None
        for c in candidates:
            if abs(ratio - c) < 0.1: # Tighter tolerance 10%
                is_locked = f"YES (~{c})"
                match = c
                break
        
        print(f"{name:<20} | {a:<8.4f} | {m_eff:<12.1f} | {r_5d:<10.4f} | {ratio:<10.3f} | {is_locked}")
        results.append((name, ratio))

    print("-" * 90)
    print(f"NOTE: Mass m_eff = E_plasmon * {229.0/22.5:.3f} (Universal Plasmon Coupling).")

    # Plot
    names = [r[0] for r in results]
    ratios = [r[1] for r in results]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(names, ratios, color='darkblue')
    for h in [0.5, 1.0, 1.5, 2.0, 2.5]:
        plt.axhline(y=h, color='r', linestyle='--', alpha=0.3)
    
    plt.ylabel("Geometric Ratio (R_5D / a)")
    plt.title("Plasmon-Based Locking: R_5D(E_p) / a")
    plt.grid(axis='y', alpha=0.3)
    
    # Add values
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('images/plots/multi_material_validation_v4_plasmon.png')
    print("Plot saved to images/plots/multi_material_validation_v4_plasmon.png")

if __name__ == "__main__":
    run_validation()
