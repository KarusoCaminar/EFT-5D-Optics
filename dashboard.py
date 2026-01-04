import subprocess
import os
import sys
import time
import shutil
import argparse

def print_header():
    print("="*60)
    print("      QUANTUM REFRACTOMETER SIMULATION SUITE")
    print("           Status Dashboard v4.2 (Atlas)")
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
        # If file exists in destination, remove it first
        if os.path.exists(dest_path):
            os.remove(dest_path)
            
        # Move the new file
        shutil.move(filename, dest_path)
        print(f"   -> ORGANIZED: Moved to {dest_path}")
        return True
    except Exception as e:
        # If move fails, it might be because the file is already in place (if module saved directly)
        if os.path.abspath(filename) == os.path.abspath(dest_path):
             return True
        print(f"   -> ERROR moving artifact: {e}")
        return False

def run_module(script_name, description, artifact_check=None, extra_args=[]):
    print(f"\n[EXEC] Running {description}...")
    
    script_path = os.path.join("modules", script_name)
    
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
                # 1. Try to organize it (if it was saved to root)
                if organize_artifact(artifact_check):
                    pass 
                # 2. Check if it exists in the destination (if module saved clearly)
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

def run_batch_simulation():
    print("Starting Batch Generation for Scientific Atlas V4.2...")
    
    # 1. GEOMETRY
    run_module("tesseract_projection.py", "1. Tesseract Animation", "tesseract_projection.gif", ["--batch"])
    run_module("kaluza_klein_visualizer.py", "2. Kaluza-Klein Cylinder", "kaluza_klein_visualization.png", ["--batch"])
    # Quantum Ring needs explicit call or check
    run_module("quantum_ring_visualizer.py", "3. Quantum Ring (Quantization)", "quantum_ring_visualization.png", ["--batch"])
    run_module("metric_tensor_visualizer.py", "4. Metric Tensor", "metric_tensor_visualization.png", ["--batch"])

    # 2. MATTER
    run_module("lattice_schematic.py", "5. Lattice Schematic (V4.2 Ratio)", "lattice_schematic.png")
    # Note: experiments/grid_locking is in a subdir, need to handle path carefully or assume module handles imports
    # The run_module function assumes scripts are in 'modules/', so we need to tweak if it's in a subdirectory
    # or just use the relative path "experiments/grid_locking.py"
    run_module(os.path.join("experiments", "grid_locking.py"), "6. Grid Locking Experiment", "experiment_locking.png")
    run_module("material_scanner.py", "7. Universal Material Scan", "material_resonance_scan.png")

    # 3. PROOF
    run_module("dispersion_validator.py", "8. Dispersion Proof", "dispersion_validation.png")
    run_module("kaluza_klein_tower.py", "9. KK Spectrum Tower", "kk_tower_spectrum.png", ["--batch"])

    # 4. VALIDATION
    # Use kagra_noise_simulation.py or kagra_validation.py? Based on inventory, we need kagra_noise_prediction.png
    # modules/kagra_noise_simulation.py likely produces it.
    run_module("kagra_noise_simulation.py", "10. KAGRA Noise Simulation", "kagra_noise_prediction.png")
    run_module("conoscopy_simulation.py", "11. Conoscopy (Visual Proof)", "experiment_conoscopy.png")
    run_module("tensor_simulation.py", "12. Tensor Anisotropy", "tensor_simulation_results.png")

    # 5. APPLICATIONS
    run_module("interactive_cloaking.py", "13. Cloaking Simulation", "cloaking_simulation_result.png", ["--batch"])
    run_module("optical_black_hole.py", "14. Optical Black Hole", "optical_black_hole.png")
    run_module("photoelasticity_5d.py", "15. Digital Photoelasticity", "stress_optics_5d.png")

    # 6. Protocol
    run_module("educational_proof.py", "16. Scientific Protocol Gen", "Math_for_Humans.txt")
    if os.path.exists("Math_for_Humans.txt") and not os.path.exists(os.path.join("docs", "Math_for_Humans.txt")):
         shutil.move("Math_for_Humans.txt", os.path.join("docs", "Math_for_Humans.txt"))

    # 7. Report Generation
    print("\n[EXEC] Running Final Report Generator...")
    cmd = ["python", "generate_report.py"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print("   -> SUCCESS: QRS_Final_Report.html generated.")
    else:
        print("   -> FAILED: Report generation error.")
        print(res.stderr)

    print("\n" + "="*60)
    print("ATLAS V4.2 GENERATION COMPLETE")
    print("="*60)

def launch_interactive_control_center():
    """Launches interactive modules."""
    print("\nLaunching Interactive Mode...")
    scripts = [
        ("interactive_prism.py", "Prism Simulation"),
        ("interactive_cloaking.py", "Cloaking Simulation"),
        ("tesseract_projection.py", "4D Tesseract Viewer"),
        ("field_explorer.py", "5D Field Explorer")
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = os.path.join(os.getcwd(), "modules")
    
    for script_name, label in scripts:
        print(f"   -> Starting {label}...")
        subprocess.Popen(["python", os.path.join("modules", script_name)], env=env, cwd=os.getcwd())

def main():
    print_header()
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", action="store_true", help="Run full batch")
    parser.add_argument("--interactive", action="store_true", help="Interactive Mode")
    args = parser.parse_args()
    
    if args.batch:
        run_batch_simulation()
    elif args.interactive:
        launch_interactive_control_center()
    else:
        print("Defaulting to Batch Mode for QA...")
        run_batch_simulation()

if __name__ == "__main__":
    main()
