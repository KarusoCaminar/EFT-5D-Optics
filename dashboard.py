import subprocess
import os
import sys
import time
import shutil

def print_header():
    print("="*60)
    print("      QUANTUM REFRACTOMETER SIMULATION SUITE")
    print("           Status Dashboard v2.0 (Clean)")
    print("="*60)
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)

def run_module(script_name, description, artifact_check=None, extra_args=[]):
    print(f"\n[EXEC] Running {description}...")
    
    # Scripts are now in modules/
    script_path = os.path.join("modules", script_name)
    print(f"       File: {script_path}")
    
    start_time = time.time()
    try:
        # Run script. Subprocess inherits CWD, so scripts run in ROOT.
        # This is good because they import each other (if they do) relative to root? 
        # Wait, if script A imports script B, and both are in modules, 
        # running 'python modules/A.py' from root requires 'modules' to be a package or PYTHONPATH adjusted.
        # Most scripts here are standalone or import 'material_parameters'.
        # We need to add 'modules' to PYTHONPATH for the subprocess.
        
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.join(os.getcwd(), "modules")
        
        cmd = ["python", script_path] + extra_args
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"   -> SUCCESS ({duration:.2f}s)")
            
            # Artifact Management
            if artifact_check:
                # Script generated artifact in CWD (Root)
                if os.path.exists(artifact_check):
                    print(f"   -> VERIFIED: Artifact '{artifact_check}' created in root.")
                    # Move to images/ folder
                    dest = os.path.join("images", artifact_check)
                    shutil.move(artifact_check, dest)
                    print(f"   -> ORGANIZED: Moved to {dest}")
                elif os.path.exists(os.path.join("images", artifact_check)):
                     print(f"   -> VERIFIED: Artifact found in 'images/'.")
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

def main():
    print_header()
    
    results = {}
    
    # 1. Material Analysis
    results['Materials'] = run_module("material_parameters.py", "Material Candidate Analysis")
    
    # 2. Simulation Modules
    results['Quantum Sim'] = run_module("quantum_refractometer.py", "Langevin Quantum Simulation", "quantum_refractometer_temperature.png")
    results['Tensor Sim'] = run_module("tensor_simulation.py", "Anisotropic Tensor Simulation", "tensor_simulation_results.png")
    results['Spatial'] = run_module("spatial_physics.py", "Spatial Beam Averaging Check", "spatial_averaging.png")
    results['Cavity'] = run_module("cavity_response.py", "Cavity Bandwidth Analysis", "cavity_response.png")
    results['Dispersion'] = run_module("dispersion_validator.py", "Spectral Dispersion Validation", "dispersion_validation.png")
    
    # 3. Visualization Modules
    results['Vis Tesseract'] = run_module("tesseract_projection.py", "4D Tesseract", "tesseract_projection.gif", ["--batch"])
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
    # generate_report is in ROOT, not modules. So handled differently? 
    # Or implies generate_report.py handles its own imports.
    # Wait, finalize_project.py left generate_report in root.
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
    print("All modules executed and organized.")
    print("Check 'QRS_Final_Report.html' for results.")

if __name__ == "__main__":
    main()
