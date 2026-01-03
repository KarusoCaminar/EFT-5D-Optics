import numpy as np
import matplotlib.pyplot as plt

def analyze_cavity_response():
    print("--- Cavity Response Analysis ---")
    
    # Constants
    c = 3e8
    
    # Cavity Parameters
    L = 0.1 # m (10 cm)
    Finesse = 10000 
    
    # FSR (Free Spectral Range) = c / 2L
    FSR = c / (2 * L)
    print(f"Cavity Length: {L} m")
    print(f"FSR: {FSR/1e9:.3f} GHz")
    
    # Linewidth (FWHM) = FSR / Finesse
    bandwidth_hz = FSR / Finesse
    print(f"Cavity Linewidth: {bandwidth_hz/1e3:.1f} kHz")
    
    # Signal Frequency (Diamond 5D Mode)
    # m_Phi = 1.777e16 rad/s -> f = 2.83e15 Hz
    f_signal = 2.83e15 
    print(f"Target Signal Frequency: {f_signal:.3e} Hz")
    
    # Check if the signal hits a mode
    # N = f_signal / FSR
    mode_number = f_signal / FSR
    nearest_integer = round(mode_number)
    detuning_hz = np.abs(f_signal - nearest_integer * FSR)
    
    print(f"Mode Order N: {mode_number:.4f}")
    print(f"Detuning from nearest mode: {detuning_hz/1e3:.1f} kHz")
    print(f"Linewidth limit: {bandwidth_hz/2/1e3:.1f} kHz")
    
    is_resonant = detuning_hz < (bandwidth_hz / 2)
    
    # Transfer Function T(f)
    # T = 1 / (1 + (2F/pi)^2 * sin^2(pi * f / FSR))
    # We plot T roughly around the signal frequency
    
    span = bandwidth_hz * 10 
    f_axis = np.linspace(f_signal - span, f_signal + span, 1000)
    
    # Phase argument of the cavity
    # phi = 2*pi*f * 2L / c = 2*pi * f / FSR
    phi = 2 * np.pi * f_axis / FSR
    Transmission = 1 / (1 + (2 * Finesse / np.pi)**2 * np.sin(phi/2)**2)
    
    plt.figure(figsize=(10, 6))
    plt.plot((f_axis - f_signal)/1e3, Transmission, color='blue', label='Cavity Transmission')
    plt.axvline(0, color='red', linestyle='--', label='5D Signal Frequency')
    plt.title(f'Cavity Filtering Effect (Finesse {Finesse})')
    plt.xlabel('Detuning from Signal (kHz)')
    plt.ylabel('Transmission')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('cavity_response.png')
    
    if is_resonant:
        print("\nRESULT: LUCK! The signal accidentally hits a cavity mode.")
    else:
        print(f"\nRESULT: BLOCKED. The signal is off-resonant by {detuning_hz/bandwidth_hz:.1f} linewidths.")
        print("ACTION REQUIRED: You must TUNE the cavity length L piezo-electrically to scan for the signal.")
        print(f"Required Tuning Precision: Delta L < { (c/(2*f_signal**2) * bandwidth_hz) * 1e15 :.2f} femtometers!")

if __name__ == "__main__":
    analyze_cavity_response()
