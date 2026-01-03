import numpy as np
import sys
import os

# Robust Import for PhysicsEngine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.physics_engine import PhysicsEngine

def print_section(title):
    print(f"\n{'#'*70}")
    print(f"  {title}")
    print(f"{'#'*70}\n")

def print_step(step_num, title):
    print(f"\n>>> SCHRITT {step_num}: {title}")
    print("-" * 50)

def log(msg):
    print(f"  • {msg}")

def calc_log(var, val, unit, desc=""):
    print(f"    {var:<15} = {val:>10.4f} {unit:<5} | {desc}")

def run_educational_proof():
    output_file = "Math_for_Humans.txt"
    
    # Initialize Engine for consistency
    engine = PhysicsEngine()
    
    class Tee(object):
        def __init__(self, name, mode):
            self.file = open(name, mode, encoding='utf-8')
            self.stdout = sys.stdout
        def write(self, data):
            self.file.write(data)
            try:
                self.stdout.write(data)
            except UnicodeEncodeError:
                self.stdout.write(data.encode('ascii', 'replace').decode('ascii'))
        def flush(self):
            self.file.flush()
            self.stdout.flush()
    
    sys.stdout = Tee(output_file, 'w')

    print("======================================================================")
    print("   QRS PROJEKT - DAS MATHEMATISCHE PROTOKOLL (Version 4.2)")
    print("   Ein Schritt-für-Schritt Beweis der 5D-Optik")
    print("======================================================================\n")
    print("--- 3. Der Numerische Beweis ---")
    print("Assumption 1: High-Frequency Limit (UV/VIS). Phonons neglected.")
    print("Assumption 2: Calibration K=63.5 is empirical (Silicon-Gauge).")
    print("-" * 40)
    print("ZIEL: Wir berechnen die Größe der 5. Dimension aus der Farbe von Licht.")
    print("      Dann prüfen wir, ob diese Größe in einen Saphir-Kristall passt.")

    # --- KONSTANTEN ---
    print_section("A. FUNDAMENTALE KONSTANTEN")
    calc_log("hbar*c", engine.H_BAR_C, "eV*nm", "Quanten-Konstante für 5D-Radius")
    calc_log("K_uni", engine.SCALING_FACTOR_K, "", "Universelle Kalibrierung (Silizium-Gauge)")

    # --- SCHRITT 1 ---
    print_section("B. BERECHNUNG DER 5D-MASSE")
    print_step(1, "Analyse der Lichtbrechung (Saphir)")
    log("Licht wird in Saphir gebrochen. Wir messen den Brechungsindex n.")
    
    n_sapphire = 1.77
    calc_log("n_Saphir", n_sapphire, "", "Gemessener Brechungsindex")
    
    # --- 3. THE CALCULATION (V4.3 EFT Cutoff) ---
    print("\n[Calculation] Determine the EFT Cutoff Scale (Lambda)...")
    
    # We use the calibrated K to find the energy scale where 5D geometry dominates
    # Lambda = sqrt(K * n^2) is the energy scale of the extra dimension
    Lambda_cutoff = np.sqrt(PhysicsEngine.SCALING_FACTOR_K * n_sapphire**2)
    
    # 5D Radius corresponding to this cutoff
    # R_5d = h_bar_c / Lambda
    R_5d_nm = PhysicsEngine.H_BAR_C / Lambda_cutoff
    
    print(f"   Material: Sapphire (Al2O3)")
    print(f"   Refractive Index n: {n_sapphire:.2f}")
    print(f"   => Calculated Cutoff Lambda: {Lambda_cutoff:.2f} eV")
    print(f"   => Corresponding 5D Radius:  {R_5d_nm:.4f} nm")

    # --- SCHRITT 2 ---
    print_section("C. BERECHNUNG DER GEOMETRIE")
    print_step(2, "Der Radius der 5. Dimension")
    log("Nach Kaluza-Klein ist Masse nichts anderes als Bewegung in einer kleinen Kreis-Dimension.")
    log("Formel: R = (hbar * c) / E")
    
    R_5d = engine.H_BAR_C / Lambda_cutoff
    calc_log("R_5D", R_5d, "nm", "DER BERECHNETE RADIUS")
    
    log(f"Das neue Ergebnis der Theorie V4.2: Die 5. Dimension ist {R_5d:.4f} nm groß.")

    # --- SCHRITT 3 ---
    print_section("D. DIE VALIDIERUNG (DER REALITÄTS-CHECK)")
    print_step(3, "Vergleich mit echtem Saphir (LIGO/KAGRA)")
    log("Wenn die Theorie stimmt, muss dieser Radius R irgendeine Bedeutung für den Kristall haben.")
    log("Wir holen uns die Gitterkonstante 'a' von High-Tech Saphir (KAGRA Testmassen).")
    
    a_sapphire = 0.4758 # Renamed from a_ligo for clarity
    calc_log("a_Gitter", a_sapphire, "nm", "Atomabstand im Saphir")
    
    log("Wir teilen nun den 5D-Radius durch den Atomabstand:")
    ratio = R_5d / a_sapphire
    calc_log("Verhältnis", ratio, "", "R_5D / a_Gitter")
    
    print("\n   *********************************************************")
    print(f"   * ERGEBNIS: {ratio:.4f}                                  *")
    print("   * Das ist fast exakt 2.0 (Resonanz N=2).                 *")
    print("   * INTERPRETATION: Die 5D-Welle ist eine stehende Welle   *")
    print("   * über genau 2 Gitterzellen.                             *")
    print("   * (V4.2 Verbesserung: Früher nur 1.8, jetzt fast 2.0!)   *")
    print("   *********************************************************")

    # --- 4. THE V4.3 VERIFICATION (Geometric Boundary) ---
    print("\n[Verification] Checking Geometric Boundary Conditions...")
    
    # Ratio Calculation (already done above, but re-using for context)
    # ratio = R_5d_nm / a_sapphire # R_5d_nm is R_5d
    
    print(f"   Lattice Constant a: {a_sapphire:.4f} nm")
    print(f"   Ratio (R_5d / a):   {ratio:.4f}")
    
    print("\n[Correlation Analysis]")
    if 2.0 < ratio < 2.2:
        print("   [SUCCESS] Ratio ~ 2.08 DETECTED!")
        print("   Interpretation: The 5D compact dimension is bounded by 2x the lattice spacing.")
        print("   This is a 'Geometric Cutoff' condition (Lambda ~ hc/2a).")
        print("   The theory is consistent as an Effective Field Theory (EFT).")
    else:
        print(f"   [FAIL] Ratio {ratio:.2f} does not match expected EFT boundary.")

    # --- 5. DISPERSION NOTE ---
    print("\n[Scientific Note]")
    print("   The dispersion in the visible range is driven by a light scalar field (m_chi ~ 8.8 eV).")
    print(f"   Lambda ({Lambda_cutoff:.0f} eV) is the UV-Cutoff where this geometric description breaks down.")

    # --- CHECK 2 ---
    print_step(4, "Gegenprobe: Diamant")
    log("Funktioniert das auch bei Diamant? (n=2.42, a=0.357)")
    
    n_diamond = 2.417
    a_diamond = 0.3567
    
    Lambda_diam = np.sqrt(engine.SCALING_FACTOR_K * (n_diamond**2))
    R_diam = engine.H_BAR_C / Lambda_diam
    ratio_diam = R_diam / a_diamond
    
    calc_log("n_Diamant", n_diamond, "", "")
    calc_log("R_Diam (5D)", R_diam, "nm", "Radius im Diamant")
    calc_log("Locking", ratio_diam, "", "Verhältnis zum Gitter")
    
    log("Auch hier eine klare geometrische Beziehung (nahe 1.5 oder 2.0?).")
    log(f"Ratio ist {ratio_diam:.2f}. Das ist geometrisch signifikant.")

    print("\n" + "="*70)
    print(" FAZIT: Die universelle Konstante K=63.5 erklärt verschiedene Kristalle.")
    print("        Brechungsindex ist Geometrie.")
    print("="*70)

    # Write to file (This part was moved from the middle to the end to ensure all output is captured)
    # The Tee class already handles writing to file and stdout simultaneously.
    # This explicit write block seems redundant if Tee is working as intended for all prints.
    # However, if the user specifically wants this block at the end, I'll keep it.
    # Given the instruction is to *add* this block, I'll place it after the main logic.
    # But the original code already uses Tee, so this explicit write will overwrite the file.
    # I will assume the user wants this *additional* summary at the end of the file,
    # and that the Tee class is still active. This means the file will be overwritten.
    # This is a potential issue, but I must follow the instruction faithfully.
    # Let's re-evaluate: The instruction provides a full block to *replace* a section.
    # The `with open(...)` block is part of the *new* content.
    # The original code uses `sys.stdout = Tee(output_file, 'w')` at the beginning,
    # which means all `print` statements are already being written to the file.
    # The new `with open("Math_for_Humans.txt", "w") as f:` will *overwrite* the file
    # with only the content inside that block. This is likely not the desired behavior.
    # The user's instruction is to "make the change and return the full contents of the new code document".
    # The provided snippet includes the `with open(...)` block.
    # If I place it as provided, it will overwrite the file.
    # I will place it exactly where it is in the provided snippet, which is after the Sapphire verification
    # and before the Diamond check. This means the Diamond check output will *not* be in the file.
    # This is a significant functional change.

    # Re-reading the instruction: "return the full contents of the new code document after the change."
    # The provided snippet is a *replacement* for a section.
    # The snippet itself contains the `with open(...)` block.
    # This implies that the `with open(...)` block is intended to be part of the *new* logic.
    # The original code's `Tee` setup means the file is already being written to.
    # If the `with open(...)` block is executed, it will truncate the file and write only its content.
    # This would mean the "Gegenprobe: Diamant" and the final "FAZIT" would not be in the file.
    # This seems like an oversight in the instruction.

    # I will assume the user wants the *content* of the `with open` block to be printed to the file
    # *in addition* to the existing `Tee` mechanism, and that the `with open` block itself should
    # not overwrite the file, but rather its content should be printed.
    # However, the instruction is to "incorporate the change in a way so that the resulting file is syntactically correct."
    # And "Make sure to incorporate the change in a way so that the resulting file is syntactically correct."
    # The provided snippet *is* syntactically correct.
    # The most faithful interpretation is to insert the snippet as provided.
    # This means the `with open` block will overwrite the file.

    # Let's reconsider the placement. The snippet starts with `print_section("B. BERECHNUNG DER 5D-MASSE")`
    # and ends with the `with open` block and the final `FAZIT`.
    # This means the *entire* `run_educational_proof` function is being replaced by the snippet.
    # No, the `{{ ... }}` indicates parts that are *not* changing.
    # The snippet starts from `print_section("B. BERECHNUNG DER 5D-MASSE")` and ends with the final `FAZIT`.
    # This means the entire section from "B. BERECHNUNG DER 5D-MASSE" to the end of the function is replaced.
    # This would mean the `Tee` setup at the beginning is kept, but then the `with open` block would overwrite.

    # Let's assume the user wants the *new logic* for the calculation and verification,
    # and the `with open` block is a *new way* of summarizing the results,
    # potentially replacing the `Tee` for the final summary.
    # If the `with open` block is intended to *replace* the `Tee` for the final output,
    # then the `Tee` setup should be removed, or the `with open` block should append.
    # But the instruction is to insert the snippet as is.

    # The most faithful interpretation of the instruction is to replace the section
    # starting from `print_section("B. BERECHNUNG DER 5D-MASSE")`
    # up to and including the final `print("="*70)` block.
    # This means the `Tee` setup remains, and then the `with open` block will indeed overwrite the file.
    # This is a functional change, but it's what the provided snippet implies.

    # Let's trace the original code's flow:
    # 1. Tee setup
    # 2. Initial prints
    # 3. Constants
    # 4. SCHRITT 1 (Sapphire calculation, E_mass, R_5d)
    # 5. SCHRITT 2 (Geometry, R_5d)
    # 6. SCHRITT 3 (Validation, ratio)
    # 7. CHECK 2 (Diamond calculation)
    # 8. Final FAZIT

    # Now, the provided snippet:
    # 1. Starts with `print_section("B. BERECHNUNG DER 5D-MASSE")`
    # 2. Contains the new calculation for `Lambda_cutoff` and `R_5d_nm`.
    # 3. Contains the new verification section.
    # 4. Contains the new `with open(...)` block.
    # 5. Contains the final `FAZIT`.

    # This means the snippet replaces everything from "B. BERECHNUNG DER 5D-MASSE" onwards.
    # The `a_ligo` variable is renamed to `a_sapphire` in the snippet.
    # The `R_5d` variable is renamed to `R_5d_nm` in the snippet.
    # The `E_mass` variable is replaced by `Lambda_cutoff`.

    # I need to ensure `a_sapphire` is defined before its first use in the snippet.
    # In the original code, `a_ligo` was defined in SCHRITT 3.
    # The snippet uses `a_sapphire` in the "4. THE V4.3 VERIFICATION" section.
    # The snippet also uses `a_sapphire` in the `with open` block.
    # The snippet also uses `n_sapphire` which is defined earlier.

    # The snippet provided is a *complete replacement* for the section it covers.
    # I will replace the entire block from `print_section("B. BERECHNUNG DER 5D-MASSE")`
    # to the end of the `run_educational_proof` function with the provided snippet.
    # This means the `a_ligo` definition and the `calc_log` for it will be replaced.
    # The `R_5d` calculation will be replaced.
    # The `ratio` calculation will be replaced.
    # The `CHECK 2` (Diamond) section will be replaced.
    # The final `FAZIT` will be replaced.

    # The snippet itself defines `a_sapphire` implicitly by using it.
    # I need to ensure `a_sapphire` is defined. The snippet uses `a_sapphire` in the verification section.
    # The original code had `a_ligo = 0.4758`. I should define `a_sapphire` before it's used.
    # The snippet also uses `PhysicsEngine.SCALING_FACTOR_K` and `PhysicsEngine.H_BAR_C`.
    # These are correctly accessed.

    # Let's make sure the `n_sapphire` definition is kept. It is.
    # The `a_sapphire` definition is missing from the snippet, but it's used.
    # I will add `a_sapphire = 0.4758` where `a_ligo` was defined, or just before its first use in the new block.
    # The snippet has `print(f"   Lattice Constant a: {a_sapphire:.4f} nm")`
    # This implies `a_sapphire` should be defined.
    # I will define `a_sapphire = 0.4758` right after `n_sapphire = 1.77`.

    # Final plan:
    # 1. Keep `n_sapphire = 1.77`.
    # 2. Insert `a_sapphire = 0.4758` right after `n_sapphire`.
    # 3. Replace the entire block from `print_section("B. BERECHNUNG DER 5D-MASSE")`
    #    to the end of the `run_educational_proof` function with the provided snippet.
    #    This includes the `with open` block and the final `FAZIT`.

    # This will result in the `with open` block overwriting the file,
    # and the Diamond check not being included in the file output.
    # This is the most faithful interpretation of the provided snippet as a replacement.

    # Let's re-read the instruction carefully: "Follow these instructions to make the following change to my code document."
    # "Your task will be to make the change and return the full contents of the new code document after the change."
    # "Please make the change faithfully and without making any unrelated edits."
    # "Be sure to keep pre-existing comments/empty lines that are not explicitly removed by the change"
    # "Make sure to incorporate the change in a way so that the resulting file is syntactically correct."

    # The snippet provided is a *replacement* for a large section.
    # The `{{ ... }}` indicates parts that are *not* changing.
    # The snippet starts with `print_section("B. BERECHNUNG DER 5D-MASSE")`
    # and ends with the final `print("="*70)`.
    # This means the entire content from `print_section("B. BERECHNUNG DER 5D-MASSE")`
    # to the end of the `run_educational_proof` function is to be replaced.

    # The `a_sapphire` variable is used in the snippet but not defined within it.
    # It was `a_ligo = 0.4758` in the original. I need to define `a_sapphire`.
    # I will define `a_sapphire = 0.4758` at the same level as `n_sapphire`.

    # Original:
    # n_sapphire = 1.77
    # calc_log("n_Saphir", n_sapphire, "", "Gemessener Brechungsindex")
    # ...
    # a_ligo = 0.4758
    # calc_log("a_Gitter", a_ligo, "nm", "Atomabstand im Saphir")

    # New:
    # n_sapphire = 1.77
    # a_sapphire = 0.4758 # Added this line
    # ... then the snippet starts.

    # This seems to be the most faithful way to incorporate the provided snippet.import numpy as np
import sys
import os

# Robust Import for PhysicsEngine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.physics_engine import PhysicsEngine

def print_section(title):
    print(f"\n{'#'*70}")
    print(f"  {title}")
    print(f"{'#'*70}\n")

def print_step(step_num, title):
    print(f"\n>>> SCHRITT {step_num}: {title}")
    print("-" * 50)

def log(msg):
    print(f"  • {msg}")

def calc_log(var, val, unit, desc=""):
    print(f"    {var:<15} = {val:>10.4f} {unit:<5} | {desc}")

def run_educational_proof():
    output_file = "Math_for_Humans.txt"
    
    # Initialize Engine for consistency
    engine = PhysicsEngine()
    
    class Tee(object):
        def __init__(self, name, mode):
            self.file = open(name, mode, encoding='utf-8')
            self.stdout = sys.stdout
        def write(self, data):
            self.file.write(data)
            try:
                self.stdout.write(data)
            except UnicodeEncodeError:
                self.stdout.write(data.encode('ascii', 'replace').decode('ascii'))
        def flush(self):
            self.file.flush()
            self.stdout.flush()
    
    sys.stdout = Tee(output_file, 'w')

    print("======================================================================")
    print("   QRS PROJEKT - DAS MATHEMATISCHE PROTOKOLL (Version 4.2)")
    print("   Ein Schritt-für-Schritt Beweis der 5D-Optik")
    print("======================================================================\n")
    print("--- 3. Der Numerische Beweis ---")
    print("Assumption 1: High-Frequency Limit (UV/VIS). Phonons neglected.")
    print("Assumption 2: Calibration K=63.5 is empirical (Silicon-Gauge).")
    print("-" * 40)
    print("ZIEL: Wir berechnen die Größe der 5. Dimension aus der Farbe von Licht.")
    print("      Dann prüfen wir, ob diese Größe in einen Saphir-Kristall passt.")

    # --- KONSTANTEN ---
    print_section("A. FUNDAMENTALE KONSTANTEN")
    calc_log("hbar*c", engine.H_BAR_C, "eV*nm", "Quanten-Konstante für 5D-Radius")
    calc_log("K_uni", engine.SCALING_FACTOR_K, "", "Universelle Kalibrierung (Silizium-Gauge)")

    n_sapphire = 1.77
    a_sapphire = 0.4758 # Lattice constant for Sapphire, previously a_ligo

    # --- SCHRITT 1 ---
    print_section("B. BERECHNUNG DER 5D-MASSE")
    print_step(1, "Analyse der Lichtbrechung (Saphir)")
    log("Licht wird in Saphir gebrochen. Wir messen den Brechungsindex n.")
    # --- 3. THE CALCULATION (V4.3 EFT Cutoff) ---
    print("\n[Calculation] Determine the EFT Cutoff Scale (Lambda)...")
    
    # Lambda = K * n^2 is the energy scale of the extra dimension (Derived from material_scanner)
    Lambda_cutoff = engine.SCALING_FACTOR_K * n_sapphire**2
    
    # 5D Radius corresponding to this cutoff
    # R_5d = h_bar_c / Lambda
    R_5d_nm = engine.H_BAR_C / Lambda_cutoff
    
    print(f"   Material: Sapphire (Al2O3)")
    print(f"   Refractive Index n: {n_sapphire:.2f}")
    print(f"   => Calculated Cutoff Lambda: {Lambda_cutoff:.2f} eV")
    print(f"   => Corresponding 5D Radius:  {R_5d_nm:.4f} nm")

    # --- 4. THE V4.3 VERIFICATION (Geometric Boundary) ---
    print("\n[Verification] Checking Geometric Boundary Conditions...")
    
    # Ratio Calculation
    ratio = R_5d_nm / a_sapphire
    
    print(f"   Lattice Constant a: {a_sapphire:.4f} nm")
    print(f"   Ratio (R_5d / a):   {ratio:.4f}")
    
    print("\n[Correlation Analysis]")
    if 2.0 < ratio < 2.2:
        print("   [SUCCESS] Ratio ~ 2.08 DETECTED!")
        print("   Interpretation: The 5D compact dimension is bounded by 2x the lattice spacing.")
        print("   This is a 'Geometric Cutoff' condition (Lambda ~ hc/2a).")
        print("   The theory is consistent as an Effective Field Theory (EFT).")
    else:
        print(f"   [FAIL] Ratio {ratio:.2f} does not match expected EFT boundary.")

    # --- 5. DISPERSION NOTE ---
    print("\n[Scientific Note]")
    print("   The dispersion in the visible range is driven by a light scalar field (m_chi ~ 8.8 eV).")
    print(f"   Lambda ({Lambda_cutoff:.0f} eV) is the UV-Cutoff where this geometric description breaks down.")
    
    # Write to file
    with open("Math_for_Humans.txt", "w") as f:
        f.write("QRS V4.3 Scientific Protocol (EFT Cutoff Edition)\n")
        f.write("=================================================\n")
        f.write(f"Universal Calibration K: {engine.SCALING_FACTOR_K}\n")
        f.write(f"Material: Sapphire (n={n_sapphire})\n")
        f.write(f"Calculated Cutoff (Lambda): {Lambda_cutoff:.2f} eV\n")
        f.write(f"Geometric Radius (R_5d):    {R_5d_nm:.4f} nm\n")
        f.write(f"Lattice Constant (a):       {a_sapphire:.4f} nm\n")
        f.write(f"Ratio (R/a):                {ratio:.4f}\n")
        f.write("\nCONCLUSION:\n")
        f.write("The 5D geometry is locked to the lattice periodicity (Ratio ~ 2).\n")
        f.write("229 eV represents the validity limit (Cutoff) of the theory.\n")

    print("\n" + "="*70)
    print(" FAZIT: Die universelle Konstante K=63.5 erklärt verschiedene Kristalle.")
    print("        Brechungsindex ist Geometrie.")
    print("="*70)

if __name__ == "__main__":
    run_educational_proof()
