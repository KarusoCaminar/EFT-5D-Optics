import subprocess
import os
import sys
import time
import shutil
import argparse

def print_header():
    print("="*60)
    print("      QUANTUM REFRACTOMETER SIMULATION SUITE")
    print("           Status Dashboard v2.1")
    print("="*60)
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

def organize_artifact(filename):
    """Moves artifact to appropriate images subdirectory."""
    if not os.path.exists(filename):
        return False
    
    # Determine destination folder
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.gif', '.mp4', '.avi']:
        subdir = "animations"
    elif ext in ['.png', '.jpg', '.jpeg', '.svg']:
        subdir = "plots"
    else:
        subdir = "" # Root of images/
        
    dest_dir = os.path.join("images", subdir)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    dest_path = os.path.join(dest_dir, filename)
    
    try:
        if os.path.exists(dest_path):
            os.remove(dest_path)
        shutil.move(filename, dest_path)
        print(f"   -> ORGANIZED: Moved to {dest_path}")
        return True
    except Exception as e:
        print(f"   -> ERROR moving artifact: {e}")
        print("   -> Tip: Ensure the dashboard is not holding the file open.") # Tip added for robustness
        return False

def run_module(script_name, description, artifact_check=None, extra_args=[]):
    print(f"\n[EXEC] Running {description}...")
    
    script_path = os.path.join("modules", script_name)
    # print(f"       File: {script_path}")
    
    start_time = time.time()
    try:
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.join(os.getcwd(), "modules")
        
        cmd = ["python", script_path] + extra_args
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"   -> SUCCESS ({duration:.2f}s)")
            
            # Artifact Management
            if artifact_check:
                if organize_artifact(artifact_check):
                    pass # Success message handled in function
                elif os.path.exists(os.path.join("images", "plots", artifact_check)):
                     print(f"   -> VERIFIED: Artifact found in 'images/plots/'.")
                elif os.path.exists(os.path.join("images", "animations", artifact_check)):
                     print(f"   -> VERIFIED: Artifact found in 'images/animations/'.")
                else:
                     print(f"   -> WARNING: Expected artifact '{artifact_check}' missing!")
            return True
        else:
            print(f"   -> FAILED (Return Code: {result.returncode})")
            print("      Error Output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"   -> ERROR: Could not execute script. {e}")
        return False

def launch_interactive_control_center():
    """Launches interactive modules in separate windows without blocking."""
    print("\n" + "="*60)
    print("   LAUNCHING INTERACTIVE CONTROL CENTER")
    print("="*60)
    print("Opening visualization windows...")
    
    scripts = [
        ("interactive_prism.py", "Prism Simulation"),
        ("interactive_cloaking.py", "Cloaking Simulation"),
        ("tesseract_projection.py", "4D Tesseract Viewer"),
        ("kaluza_klein_visualizer.py", "KK Cylinder Viewer"),
        ("field_explorer.py", "5D Field Explorer")
    ]
    
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(os.getcwd(), "modules")
    
    processes = []
    
    for script_name, label in scripts:
        print(f"   -> Starting {label}...")
        script_path = os.path.join("modules", script_name)
        # Use Popen to run in parallel/background
        try:
            p = subprocess.Popen(["python", script_path], env=env, cwd=os.getcwd())
            processes.append(p)
        except Exception as e:
            print(f"      ERROR: Failed to launch {script_name}: {e}")
            
    print("\n[INFO] All interactive modules launched.")
    print("       Close the windows to terminate them.")
    print("="*60)

def run_batch_simulation():
    results = {}
    
    # 1. Material Analysis
    results['Materials'] = run_module("material_parameters.py", "Material Candidate Analysis")
    
    # 2. Simulation Modules
    results['Quantum Sim'] = run_module("quantum_refractometer.py", "Langevin Quantum Simulation", "quantum_refractometer_temperature.png")
    results['Tensor Sim'] = run_module("tensor_simulation.py", "Anisotropic Tensor Simulation", "tensor_simulation_results.png")
    results['Spatial'] = run_module("spatial_physics.py", "Spatial Beam Averaging Check", "spatial_averaging.png")
    results['Cavity'] = run_module("cavity_response.py", "Cavity Bandwidth Analysis", "cavity_response.png")
    results['Dispersion'] = run_module("dispersion_validator.py", "Spectral Dispersion Validation", "dispersion_validation.png")
    
    # 3. Visualization Modules (Batch Mode)
    results['Vis Tesseract'] = run_module("tesseract_projection.py", "4D Tesseract", "tesseract_projection.gif", ["--batch"])
    
    # Secondary artifact cleanup (Ensure MP4 is moved if generated)
    if os.path.exists("tesseract_projection.mp4"):
        organize_artifact("tesseract_projection.mp4")

    results['Vis KK'] = run_module("kaluza_klein_visualizer.py", "KK Cylinder", "kaluza_klein_visualization.png", ["--batch"])
    results['Vis Quant'] = run_module("quantum_ring_visualizer.py", "Quantum Ring", "quantum_ring_visualization.png", ["--batch"])
    results['Vis Matrix'] = run_module("metric_tensor_visualizer.py", "Metric Tensor", "metric_tensor_visualization.png", ["--batch"])
    
    # 4. Advanced & New Features
    results['Engineering'] = run_module("engineering_application.py", "Engineering Limits")
    results['KK Spectrum'] = run_module("kaluza_klein_tower.py", "KK Mass Spectrum", "kk_tower_spectrum.png", ["--batch"])
    results['Field Explorer'] = run_module("field_explorer.py", "5D-Field Explorer", "field_explorer.gif", ["--batch"])
    results['Lattice Schem'] = run_module("lattice_schematic.py", "Lattice Schematic", "lattice_schematic.png")
    results['Lattice Corr'] = run_module("lattice_correlation.py", "Lattice Correlation", "lattice_correlation.png")
    results['Momentum'] = run_module("momentum_transfer.py", "Momentum Transfer", "momentum_transfer.png")
    results['Sensitivity'] = run_module("sensitivity_calculator.py", "Sensitivity SNR", "sensitivity_snr.png")
    results['Validation'] = run_module("educational_visualizer.py", "Real Data Validation", "real_data_validation.png")

    # 5. Metamaterials (New)
    results['Gen Cloaking'] = run_module("generate_cloaking_image.py", "Cloaking Simulation (Asset Gen)", "cloaking_simulation.gif")
    results['Gen Prism'] = run_module("generate_prism_image.py", "Prism Simulation (Asset Gen)", "prism_simulation.gif")
    
    # 6. Educational Proof (Text)
    results['Edu Proof'] = run_module("educational_proof.py", "Generating Math Protocol")
    # Move the text file manually if successful
    if results['Edu Proof'] and os.path.exists("Math_for_Humans.txt"):
        shutil.move("Math_for_Humans.txt", os.path.join("docs", "Math_for_Humans.txt"))
        print("   -> ORGANIZED: Moved Math_for_Humans.txt to docs/")

    # 6. Report Generation
    print("\n[EXEC] Running Report Generator...")
    cmd = ["python", "generate_report.py"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print("   -> SUCCESS: QRS_Final_Report.html generated.")
    else:
        print("   -> FAILED: Report generation error.")
        print(res.stderr)

    print("\n" + "="*60)
    print("FINAL PROJECT STATUS REPORT")
    print("="*60)
    print("All batch modules executed.")
    print("Check 'QRS_Final_Report.html' for results.")

def main():
    print_header()
    
    parser = argparse.ArgumentParser(description="QRS Simulation Dashboard")
    parser.add_argument("--batch", action="store_true", help="Run full batch simulation for report")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive control center")
    
    args = parser.parse_args()
    
    if args.batch:
        run_batch_simulation()
    elif args.interactive:
        launch_interactive_control_center()
    else:
        # Menu Mode
        print("Select Mode:")
        print("  [1] Run Full Scientific Report (Batch Mode)")
        print("  [2] Launch Interactive Control Center")
        print("  [3] Exit")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            run_batch_simulation()
        elif choice == "2":
            launch_interactive_control_center()
        else:
            print("Exiting.")

if __name__ == "__main__":
    main()
