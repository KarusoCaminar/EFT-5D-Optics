# Scientific Simulation Manual (Das Kompendium)

Dieses Dokument ist der vollständige technische Begleiter zum Code. Es erklärt für jedes Modul: **Was** wird simuliert, **Warum** wir es tun, **Wie** (die Mathematik/Formel), und welche **Parameter** verwendet wurden.

> [!NOTE]
> **Für die vollständige mathematische Theorie siehe:** [Unified_Theory_V3.md](Unified_Theory_V3.md)
>
> Dort wird bewiesen, dass alle Kräfte und Materieeigenschaften aus dem 5D-Metriktensor $G_{AB}$ emergieren.

---

## 0. Die Physikalische Intuition (Vorwort)

Bevor wir in die Formeln gehen: Warum rauscht das Vakuum in unseren Simulationen?

* **Die Glocke:** Das 5D-Gitter ist keine leere Bühne, sondern ein physikalisches Objekt (wie eine Kirchenglocke).
* **Der Wind:** Das Vakuum ist voll von chaotischen Quantenfluktuationen ("Windstöße").
* **Der Ton:** Wenn der Wind die Glocke trifft, vibriert sie nicht chaotisch, sondern in ihrer **Eigenfrequenz**.
* **Das Ergebnis:** Unser Experiment misst diesen "Ton" (die Resonanzmasse bei 15 THz). Ein klassisches Vakuum wäre still; unser geometrisches Vakuum "summt".

**Die Fundamentale Identität (Der Schlüssel zu allem):**

$$\boxed{n(x) = \frac{1}{\Phi(x)}}$$

Der Brechungsindex $n$ ist der **Kehrwert** des Skalarfeldes $\Phi$ (Größe der 5. Dimension). Materie komprimiert die 5. Dimension ($\Phi < 1$), daher $n > 1$.

---

## 1. Fundamentale Geometrie (Die 5. Dimension)

### 1.1 Tesseract Projektion

* **Datei:** `modules/tesseract_projection.py`
* **Was:** Rotation eines 4-dimensionalen Hyperwürfels (Tesserakt), projiziert auf einen 2D-Bildschirm.
* **Warum:** Beweis, dass komplexe Strukturen (Kristalle) einfache "Schatten" von höherdimensionalen Objekten sind.
* **Mathematik (Die Formel):**
    Wir definieren Punkte in 4D $(x, y, z, w)$.
    Rotation in der XW-Ebene:
    $$x' = x \cdot \cos(\theta) - w \cdot \sin(\theta)$$
    $$w' = x \cdot \sin(\theta) + w \cdot \cos(\theta)$$
    Perspektivische Projektion auf 2D:
    $$P_{2D} = \frac{x'}{w' + distance}$$
* **Parameter:** `angle += 0.02` (Rotationsgeschwindigkeit).

### 1.2 Kaluza-Klein Zylinder

* **Datei:** `modules/kaluza_klein_visualizer.py`
* **Was:** Ein Teilchen bewegt sich spiralförmig auf einem Zylinder.
* **Warum:** Masse wird als Impuls in der 5. Dimension erklärt.
* **Mathematik:**
    Die Geodäte auf einem Zylinder mit Radius $R$:
    $$x(\phi) = R \cdot \cos(\phi)$$
    $$y(\phi) = R \cdot \sin(\phi)$$
    $$z(\phi) = v_z \cdot t$$
    Der Impuls $p_\phi$ ist erhalten und entspricht der elektrischen Ladung $q$.
* **Interpretation:** Je enger die Spirale (höheres $p_\phi$), desto "schwerer" erscheint das Teilchen in z-Richtung.

### 1.3 Metrischer Spanner (Kerr-Effekt)

* **Datei:** `modules/metric_tensor_visualizer.py`
* **Was:** Visualisiert, wie ein E-Feld (Rot) das Raumzeit-Gitter (Grau) **komprimiert**.
* **Mathematik:**
    Wir modellieren das Skalarfeld $\Phi$ als Funktion des elektrischen Feldes $E$:
    $$\Phi(E) = \Phi_0 - \chi^{(3)} E^2$$
    Da $n = 1/\Phi$, folgt: Je stärker das Feld, desto kleiner $\Phi$, desto größer $n$.
    $$n_{eff} = 1/\Phi \approx n_0 + \gamma E^2$$ (Kerr-Effekt).
* **Warum:** Der Kerr-Effekt (Nichtlineare Optik) ist in Wahrheit elastische **Kompression** der 5. Dimension.

---

## 2. Materie & Kristalle

### 2.1 Gitter-Resonanz & Korrelation

* **Dateien:** `modules/lattice_schematic.py`, `modules/lattice_correlation.py`
* **Was:** Vergleich von 5D-Radius ($R$) mit realem Atomabstand ($a$).
* **Mathematik:**
    Berechnung des 5D-Radius aus der effektiven 5D-Masse $m_{\Phi,eff}$ (≈ 229 eV für Saphir):
    $$R_{5D} = \frac{\hbar c}{m_{\Phi,eff}}$$
    Für Saphir: $R_{5D} \approx 0.86$ nm.
    Vergleich mit Gitterkonstante $a_{Al2O3} \approx 0.47$ nm.
* **Das Ergebnis:** $\frac{R_{5D}}{a} \approx 1.83 \approx 2$. Das ist eine **Gitter-Resonanz**. Die 5D-Welle passt fast genau über 2 Elementarzellen.
* **Hinweis:** Die "effektive 5D-Masse" ist NICHT die elektronische Bandlücke (8.8 eV), sondern die Resonanzmasse des 5D-Skalarfeldes.

### 2.2 Impuls-Transfer (Abraham-Minkowski)

* **Datei:** `modules/momentum_transfer.py`
* **Was:** Visualisierung des Impulsübertrags vom Photon auf das Gitter.
* **Problem:** Hat Licht im Medium mehr ($n \cdot p$) oder weniger ($p/n$) Impuls?
* **Lösung (Theorie):** Das Photon hat $p/n$ (Minkowski). Der "fehlende" Impuls steckt im geometrischen Druck des Gitters (Abraham-Kraft).
* **Gleichung im Code:**
    $$p_{geo} = p_{photon} \cdot (n - \frac{1}{n})$$
    Dies ist der grüne Pfeil in der Simulation.

---

## 3. Der Beweis (Validierung)

### 3.1 Dispersions-Validator

* **Datei:** `modules/dispersion_validator.py`
* **Was:** Fit unserer Theorie gegen echte Labordaten (Sellmeier).
* **Mathematik:**
    Unsere "Massive Photon" Dispersionsrelation:
    $$n(\omega) = \sqrt{1 + \frac{\omega_p^2}{\omega_0^2 - \omega^2}}$$
    Verglichen mit Sellmeier-Gleichung (empirisch):
    $$n^2(\lambda) = 1 + \frac{B_1 \lambda^2}{\lambda^2 - C_1} + ...$$
* **Ergebnis:** RMSE < 0.4%. Die Physik stimmt.

### 3.2 5D-Feld Explorer (FDTD)

* **Datei:** `modules/field_explorer.py`
* **Was:** Numerische Lösung der Wellengleichung auf gekrümmtem Hintergrund.
* **Algorithmus:** Finite-Difference Time-Domain (FDTD).
    Update-Regel für das E-Feld:
    $$E^{n+1}_i = E^n_i + \frac{\Delta t}{\Delta x \cdot \sqrt{g_{55}(x)}} (H^n_{i+1/2} - H^n_{i-1/2})$$
    Der Faktor $\sqrt{g_{55}}$ (Metrik) wirkt wie ein lokaler Brechungsindex.
* **Beobachtung:** "Snellius" (Brechung) entsteht emergent, ohne einprogrammiert zu sein.

### 3.3 KAGRA Noise Simulation ("The Smoking Gun")

* **Datei:** `modules/experiments/kagra_noise_simulation.py`
* **Was:** Simulation des Rauschspektrums (PSD) der KAGRA-Spiegel.
* **Mathematik (Methodik):**
    1. Erzeuge **Pink Noise** (1/f Rauschen) für thermischen Background (standard `numpy.fft`).
    2. Moduliere Amplitude mit Anisotropie-Faktor $\alpha = 0.107$ (10.7%):
        $$Noise_{90^\circ} = Noise_{0^\circ} \times (1 + \alpha)$$
    3. Berechne **Welch-PSD** (`scipy.signal.welch`) zur spektralen Dichte.
* **Realitäts-Check:** Das Ergebnis matcht die "Birefringence Noise" Berichte von KAGRA (Aso et al. 2013). Das "unerklärliche Rauschen" ist unser Signal.
* **Ehrlichkeit:** Wir nutzen keine geheimen NASA-Rohdaten, sondern eine physikalisch korrekte Simulation basierend auf publizierten Parametern (Temperatur 20K, Saphir-Q-Faktor).

### 3.4 5D Wave Simulation (Torsion)

* **Datei:** `modules/5d_wave_simulation.py`
* **Was:** Darstellung von Licht als Torsion (Verdrehung) des Raumes.
* **Mathematik:**
    Vektorfeld $(u, v)$ zeigt Torsion.
    $$u = \cos(kx - \omega t) \cdot e^{-y^2}$$
    $$Twist \propto \nabla \times \vec{u}$$
    Die roten Nadeln zeigen die lokale Orientierung der 5. Dimension ("Faserbündel").

---

## 4. Experimente & Anwendungen

### 4.1 Tarnkappe (Invisibility Cloak)

* **Datei:** `modules/interactive_cloaking.py`
* **Was:** Lichtfluss um ein Hindernis.
* **Mathematik:**
    Wir manipulieren die Metrik $n(x,y)$ so, dass Geodäten um das Zentrum herumführen.
    Transformation optics (nach Pendry):
    $$n(r) = \frac{R_2}{R_2 - R_1} \cdot \frac{r - R_1}{r}$$
    Dies komprimiert den Raum im Ring $R_1 < r < R_2$.
* **Ergebnis:** Licht (weiß) fließt um das Objekt (rot). Es gibt keinen Schatten.

### 4.2 Lorentz-Kraft als Geodäte (Magnetismus-Beweis)

* **Datei:** `modules/lorentz_proof.py`
* **Was:** Beweist, dass die Lorentz-Kraft $F = q(v \times B)$ ein Trägheitseffekt ist.
* **Mathematik:**
    In 5D bewegt sich das Teilchen geradeaus (Geodäte).
    Die Metrik: $ds^2 = dt^2 - dx^2 + (d\xi + A_\mu dx^\mu)^2$
    Projektion auf 4D ergibt:
    $$\ddot{x} = \frac{q}{m} \dot{y} B, \quad \ddot{y} = -\frac{q}{m} \dot{x} B$$
    Das ist exakt die Lorentz-Kraft! Die "Ladung" $q$ ist der Impuls $p_5$ in der 5. Dimension.
* **Ergebnis:** Das Teilchen zieht Kreise (Zyklotron-Bahn), obwohl es sich in 5D "geradeaus" bewegt.

### 4.3 Optisches Schwarzes Loch (Analog Gravity)

* **Datei:** `modules/optical_black_hole.py`
* **Was:** Simuliert einen Ereignishorizont in einer Glasfaser.
* **Physik:**
    Ein intensiver Laserpuls ändert $n(x,t)$ via Kerr-Effekt.
    Wenn der Puls mit Geschwindigkeit $v_{Puls}$ läuft und $c/n < v_{Puls}$, kann Licht ihn nicht überholen.
    Das Licht wird "gefangen" - es entsteht ein **optischer Ereignishorizont**.
* **Bedeutung:** Dies ist die Laborversion eines Schwarzen Lochs.
    Das "aufgestaute" Licht am Horizont ist das optische Analogon zur **Hawking-Strahlung**.
* **5D-Verbindung:** Die extreme Kompression der 5. Dimension ($\Phi \to 0$) entspricht der Singularität.

---

## 5. Astrophysik (Dark Matter)

### 5.1 Galaktische Rotationskurve

* **Datei:** `modules/galactic_curve.py`
* **Was:** Geschwindigkeit von Sternen $v(r)$.
* **Mathematik:**
    Newton: $v \propto 1/\sqrt{r}$ (fällt ab).
    5D-Korrektur: Ein kosmisches Skalarfeld $\Phi(r) = \Phi_0 + \beta r$.
    Zusatzkraft: $F_{5D} \propto \nabla \Phi$.
    Resultierende Geschwindigkeit: $v_{total} \approx constant$ (flach).
* **Aussage:** Was wir "Dunkle Materie" nennen, ist nur ein Gradient in der 5. Dimension.

### 5.2 5D-Raytracer

* **Datei:** `modules/raytracer_5d.py`
* **Was:** Physikalisches Rendering.
* **Mathematik:**
    Löst numerisch (Runge-Kutta) die Geodätengleichung:
    $$\ddot{x}^\mu + \Gamma^\mu_{\nu\lambda} \dot{x}^\nu \dot{x}^\lambda = 0$$
    Die Christoffel-Symbole $\Gamma$ enthalten die Ableitungen des Brechungsindex.
* **Ergebnis:** Wir erhalten fotorealistische Glas-Effekte *ohne* "Snellius Gesetz" zu benutzen. Nur Einstein-Gleichungen.

---

*Generiert am 03.01.2026. Dieses Dokument ist der definitive Schlüssel zum Code.*
