# Quellenverzeichnis & Datenherkunft

Dieses Projekt basiert auf physikalischen Gesetzmäßigkeiten und etablierten Materialdaten. Hier sind die spezifischen Quellen für die verwendeten Werte und die Validierungskurven.

## 1. KAGRA Gravitationswellen-Detektor (NASA/JAXA)

* **Verwendung:** Validierung der Rauschgrenze in `modules/experiments/kagra_validation.py`.
* **Quelle:** Akutsu, T., et al. (KAGRA Collaboration). (2020). "Overview of KAGRA: Detector design and construction history." *Progress of Theoretical and Experimental Physics*, 2021(5), 05A101.
* **Link/DOI:** [10.1093/ptep/ptaa125](https://doi.org/10.1093/ptep/ptaa125)
* **Spezifische Daten:** "Figure 2: Target sensitivity of KAGRA". Wir verwenden die "Thermal Noise" Kurve (dominiert durch Saphir-Spiegel bei 20K).
* **Excess Noise (Birefringence):**
  * Aso, Y., et al. (2013). "Interferometer design of the KAGRA gravitational wave detector". *Phys. Rev. D* 88, 043007.
  * Somiaya, K. (2012). "Detector configuration of KAGRA". *Class. Quantum Grav.* 29, 124007.
  * Beide Papers diskutieren "Birefringence Noise" als limitierenden Faktor bei Saphir. Unsere Theorie identifiziert dies als 5D-Effekt.
* **Hinweis:** Die Kurve im Skript ist eine analytische Näherung (`1e-23 * (100/f)^0.5`), die den publizierten Verlauf im Bereich 10Hz-1kHz reproduziert.

## 2. Saphir Material-Eigenschaften

* **Verwendung:** Berechnung der 5D-Masse und Simulation des Prismas.
* **Quelle (Brechungsindex):** Malitson, I. H. (1962). "Refraction and Dispersion of Synthetic Sapphire." *Journal of the Optical Society of America*, 52(12), 1377-1379.
* **Daten:** Sellmeier-Koeffizienten für den ordentlichen Strahl ($n_o$).
* **Quelle (Gitterstruktur):** Dobrovinskaya, E. R., Lytvynov, L. A., & Pishchik, V. (2009). *Sapphire: Material, Manufacturing, Applications*. Springer.
* **Daten:** Gitterkonstante $a = 4.758$ Å ($0.4758$ nm), verwendet in `modules/experiments/grid_locking.py`.

## 3. Optische Theorie (Konoskopie)

* **Verwendung:** Simulation des Malteser-Kreuzes in `modules/experiments/conoscopy_simulation.py`.
* **Quelle:** Born, M., & Wolf, E. (1999). *Principles of Optics*. Cambridge University Press. (Kapitel 14: Crystal Optics).
* **Konzept:** Die theoretische Vorhersage für Interferenzbilder uniaxialer Kristalle ("Isogyren" und "Isochromen") dient als "Ground Truth" für unsere 5D-Geometrie-Simulation.

## 4. Galaktische Rotationskurven

* **Verwendung:** Vergleich der Kepler-Kurve mit der 5D-Kurve in `modules/galactic_curve.py`.
* **Standard-Referenz:** Rubin, V. C., & Ford, W. K. J. (1970). "Rotation of the Andromeda Nebula from a Spectroscopic Survey of Emission Regions." *The Astrophysical Journal*, 159, 379.
* **Konzept:** Die Beobachtung der "flachen Rotationskurven" ist das fundamentale Phänomen, das wir geometrisch (ohne Dunkle Materie) reproduzieren.

## 5. Numerische Methoden & Simulationen

* **FDTD (Finite-Difference Time-Domain):**
  * Verwendet in: `modules/field_explorer.py`, `generate_prism_image.py`, `generate_cloaking_image.py`.
  * Standard-Algorithmus zur Lösung der Maxwell-Gleichungen.
  * Referenz: Taflove, A., & Hagness, S. C. (2005). *Computational Electrodynamics: The Finite-Difference Time-Domain Method*. Artech House.
* **Geodätischer Integrator (Runge-Kutta):**
  * Verwendet in: `modules/raytracer_5d.py`.
  * Löst die Einstein-Geodäten-Gleichung $\ddot{x} + \Gamma \dot{x}\dot{x} = 0$.
  * Standard `scipy.integrate.solve_ivp` Solver (Dormand-Prince Methode).

## 6. Fundamentale Konstanten

* Alle Naturkonstanten ($c$, $h$, $\hbar$, $eV$) entstammen dem **CODATA 2018** Datensatz.
  * Quelle: NIST Reference on Constants, Units, and Uncertainty.
  * Werte:
    * $c = 299,792,458$ m/s
    * $h = 4.135667696 \times 10^{-15}$ eV·s
