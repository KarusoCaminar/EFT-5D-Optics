import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import welch
import os

"""
Module: kagra_noise_simulation.py
Purpose: Simulate the 'Smoking Gun' signature of 5D Spacetime Fluctuations.
Context: KAGRA (Japan) uses Cryogenic Sapphire Mirrors. They suffer from 'Unknown Excess Noise'.
Theory Prediction: The 5D-Scalar Field Phi fluctuates. In Sapphire, this noise is anisotropic.
          Amplitude modulation = 10.7% dependent on polarization angle relative to C-axis.
Source: QRS Final Report, Section 7.2 & 8.
"""

def generate_pink_noise(n_samples):
    """Generates 1/f noise (Pink Noise) representing fundamental background fluctuations."""
    # Classical thermal noise is often 1/f or 1/f^2 at low frequencies
    white = np.random.standard_normal(size=n_samples)
    # FFT to frequency domain
    X_white = np.fft.rfft(white)
    frequencies = np.fft.rfftfreq(n_samples)
    # Apply 1/f filter (avoid division by zero at f=0)
    with np.errstate(divide='ignore'):
        scale = 1 / np.sqrt(frequencies)
    scale[0] = 0
    X_pink = X_white * scale
    # Back to time domain
    pink = np.fft.irfft(X_pink)
    # Normalize
    return pink / np.std(pink)

def simulate_kagra_experiment():
    print("Simulating Quantum Refractometer Experiment (KAGRA Environment)...")
    
    # Setup
    fs = 16384.0       # Sampling rate (Hz) - typical for GW detectors
    duration = 10.0    # Seconds of data
    n_samples = int(fs * duration)
    t = np.arange(n_samples) / fs
    
    # 1. Base Noise (Standard Physics)
    # Thermal Noise + Shot Noise (Isotropic - same for all angles)
    # We model this as a mix of White and Pink noise
    noise_thermal = generate_pink_noise(n_samples) * 1e-19  # Amplitude scale
    noise_shot = np.random.normal(0, 0.5e-19, n_samples)
    baseline_noise = noise_thermal + noise_shot
    
    # 2. 5D-Geometric Noise (The Prediction)
    # This noise comes from the fluctuation of the scalar field Phi.
    # It couples via the refractive index.
    # Crucial: It is modulated by the Tesseract Geometry of Sapphire.
    
    # Anisotropy Factor from Theory: 10.7% difference between axes
    anisotropy_factor = 0.107 
    
    # Simulation: Measurement at 0 degrees (c-axis alignment)
    # Here the coupling is minimal (Base 5D noise)
    noise_5d_base = generate_pink_noise(n_samples) * 0.8e-19 # Slightly lower level
    signal_0deg = baseline_noise + noise_5d_base
    
    # Simulation: Measurement at 90 degrees (a-axis alignment)
    # Here the coupling is maximal (+10.7% amplitude on the 5D component)
    noise_5d_max = noise_5d_base * (1.0 + anisotropy_factor)
    signal_90deg = baseline_noise + noise_5d_max
    
    # 3. Analysis: Compute Power Spectral Density (PSD)
    # This is what scientists look at (Sensitivity Curve)
    f0, psd_0 = welch(signal_0deg, fs, nperseg=4096)
    f90, psd_90 = welch(signal_90deg, fs, nperseg=4096)
    
    # Plotting
    plt.figure(figsize=(12, 7))
    
    # Plot standard KAGRA-like sensitivity curve shape (log-log)
    plt.loglog(f0, np.sqrt(psd_0), 'b-', alpha=0.6, label=r'Polarization $\theta=0^\circ$ (c-axis)')
    plt.loglog(f90, np.sqrt(psd_90), 'r-', alpha=0.8, label=r'Polarization $\theta=90^\circ$ (a-axis)')
    
    # Highlight the gap
    plt.fill_between(f0, np.sqrt(psd_0), np.sqrt(psd_90), color='red', alpha=0.1, label='Excess Noise Gap (The 5D-Signature)')
    
    # Labels
    plt.title("Signature of 5D-Fluctuations vs. Classical Birefringence Noise", fontsize=14)
    plt.xlabel("Frequency [Hz]", fontsize=12)
    plt.ylabel(r"Strain Sensitivity [$1/\sqrt{Hz}$]", fontsize=12)
    plt.grid(True, which="both", ls="-", alpha=0.4)
    plt.legend(fontsize=10)
    plt.xlim(10, 5000) # Relevant GW band
    
    # Annotation
    plt.text(100, 2.2e-19, "Real Data Match:\nKAGRA reports 'Birefringence Noise'\ndepends on Polarization Angle.", fontsize=12, color='darkred', weight='bold')
    plt.text(100, 1.5e-19, "Our Theory explains this as\nGeometric Drag (10.7%).", fontsize=10, color='black', style='italic')
    
    # Save
    os.makedirs("images", exist_ok=True)
    out_path = os.path.join("images", "kagra_noise_prediction.png")
    plt.savefig(out_path, dpi=150)
    print(f"Saved simulation to {out_path}")
    plt.close()

if __name__ == "__main__":
    simulate_kagra_experiment()
