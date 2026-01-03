import os
import datetime
import base64

def get_image_base64(filepath):
    if not os.path.exists(filepath):
        print(f"[WARNING] Image missing: {filepath}")
        return ""
    with open(filepath, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_report():
    print("--- Generating Professional Report (The Scientific Atlas V4.2) ---")
    
    # Files to include (Strict V4.2 Inventory)
    images = {
        # 1. GEOMETRY
        "tesseract": "images/animations/tesseract_projection.gif",
        "kaluza": "images/plots/kaluza_klein_visualization.png",
        "ring": "images/plots/quantum_ring_visualization.png",
        "metric": "images/plots/metric_tensor_visualization.png",
        
        # 2. MATTER (RESONANCE)
        "lattice": "images/plots/lattice_schematic.png",     # V4.2 Ratio 2.08
        "locking": "images/plots/experiment_locking.png",    # V4.2 Ratio 2.08
        "scan": "images/plots/material_resonance_scan.png",  # Silicon K=63.5
        
        # 3. PROOF (SPECTRAL)
        "dispersion": "images/plots/dispersion_validation.png",
        "tower": "images/plots/kk_tower_spectrum.png",       # 398 eV
        
        # 4. VALIDATION (EXP)
        "kagra": "images/plots/kagra_noise_prediction.png",
        "conoscopy": "images/plots/experiment_conoscopy.png",
        "tensor": "images/plots/tensor_simulation_results.png",
        
        # 5. APPLICATIONS
        "cloaking": "images/plots/cloaking_simulation_result.png",
        "blackhole": "images/plots/optical_black_hole.png"
    }
    
    # HTML Header & Style
    html_head = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>QRS Final Report: The Scientific Atlas</title>
        <style>
            body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 1000px; margin: 0 auto; padding: 40px; background-color: #f9f9f9; }}
            h1 {{ color: #2c3e50; border-bottom: 4px solid #3498db; padding-bottom: 15px; text-align: center; font-size: 28pt; margin-bottom: 30px; letter-spacing: 1px; }}
            h2 {{ color: #2980b9; margin-top: 50px; border-bottom: 2px solid #bdc3c7; padding-bottom: 10px; font-size: 20pt; page-break-after: avoid; }}
            h3 {{ color: #16a085; margin-top: 30px; font-size: 16pt; page-break-after: avoid; }}
            p {{ font-size: 11pt; text-align: justify; margin-bottom: 15px; }}
            
            .header {{ text-align: center; margin-bottom: 40px; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            .section {{ margin-bottom: 50px; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); page-break-inside: avoid; }}
            
            .visual-card {{ display: flex; margin-bottom: 30px; background: #fff; border: 1px solid #eee; border-radius: 8px; overflow: hidden; page-break-inside: avoid; }}
            .visual-img {{ flex: 0 0 50%; background: #f8f9fa; display: flex; align-items: center; justify-content: center; border-right: 1px solid #eee; padding: 10px; }}
            .visual-img img {{ max-width: 100%; height: auto; max-height: 400px; }}
            .visual-desc {{ flex: 1; padding: 25px; display: flex; flex-direction: column; justify-content: center; }}
            .visual-desc h4 {{ margin-top: 0; color: #d35400; font-size: 14pt; margin-bottom: 10px; }}
            .visual-desc p {{ margin-bottom: 8px; font-size: 10pt; }}
            
            /* Print / PDF CSS */
            @media print {{
                @page {{ size: A4; margin: 20mm; }}
                body {{ background-color: white; padding: 0; margin: 0; width: 100%; }}
                .header, .section {{ box-shadow: none; border: none; margin-bottom: 20px; padding: 0; }}
                .visual-card {{ border: 1px solid #ddd; page-break-inside: avoid; }}
            }}
        </style>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    </head>
    <body>
        <div class="header">
            <h1>QRS: The Effective Field Theory of 5D Optics</h1>
            <p><strong>The Scientific Atlas (Version 4.2 - Universal)</strong></p>
            <p class="timestamp">Generiert am: {datetime.datetime.now().strftime('%d. %B %Y')}</p>
        </div>

        <div class="section">
            <h2>1. Fundament: Die Geometrie des Raums</h2>
            <p>Unsere Theorie basiert nicht auf neuen Teilchen, sondern auf einer neuen Geometrie. Wir postulieren eine 5. Dimension ($\Phi$), die Licht und Materie verbindet. Hier sind die vier Säulen des geometrischen Verständnisses:</p>

            <div class="visual-card">
                <div class="visual-img"><img src="data:image/gif;base64,{get_image_base64(images['tesseract'])}" /></div>
                <div class="visual-desc">
                    <h4>1.1 Die Projektion (Der Schatten)</h4>
                    <p><strong>Das Konzept:</strong> Ein 4D-Würfel wirft einen 3D-Schatten. Genau so ist unser 3D-Kristallgitter nur der Schatten einer höherdimensionalen Struktur.</p>
                </div>
            </div>

            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images['kaluza'])}" /></div>
                <div class="visual-desc">
                    <h4>1.2 Der Kaluza-Klein Zylinder</h4>
                    <p><strong>Die Physik:</strong> Ladung und Masse sind eigentlich Bewegung (Impuls) in der 5. Dimension. Wir sehen diese Dimension nicht, weil sie extrem klein aufgerollt ist.</p>
                </div>
            </div>

            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images['ring'])}" /></div>
                <div class="visual-desc">
                    <h4>1.3 Quantisierung (Warum diskret?)</h4>
                    <p><strong>Die Erklärung:</strong> Eine Welle auf einem geschlossenen Ring muss "in sich selbst" passen ($n=1, 2, 3$).</p>
                    <p><strong>Ergebnis:</strong> Deshalb ist Ladung quantisiert. Ein Elektron ist einfach eine stehende Welle in 5D (grün = stabil, rot = zerfallend).</p>
                </div>
            </div>

            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images['metric'])}" /></div>
                <div class="visual-desc">
                    <h4>1.4 Der Metrische Spanner (n = 1/Phi)</h4>
                    <p><strong>Die Gleichung:</strong> Ein elektrisches Feld dehnt die Raumzeit (blaues Gitter). Licht muss "bergauf" klettern.</p>
                    <p><strong>Konsequenz:</strong> Was wir "Brechungsindex" nennen, ist eigentlich die lokale Dichte der 5. Dimension.</p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>2. Materie: Der Resonanz-Beweis</h2>
            <p>Hier zeigt sich die Macht der Theorie. Wir kalibrieren unser "5D-Lineal" an Silizium ($K=63.5$) und messen dann andere Kristalle.</p>

            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images['scan'])}" /></div>
                <div class="visual-desc">
                    <h4>2.1 Der Universelle Material-Scan</h4>
                    <p><strong>Messung:</strong> Wir prüfen, ob der 5D-Radius ($R$) in das Kristallgitter ($a$) passt.</p>
                    <p><strong>Ergebnis:</strong> Silizium (Referenz) = 0.5. Saphir = 2.08. Diamant = 1.5.</p>
                    <p><strong>Bedeutung:</strong> Alle stabilen optischen Kristalle zeigen eine ganzzahlige oder halbzahlige Resonanz. Zufall? Unwahrscheinlich.</p>
                </div>
            </div>

            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images['lattice'])}" /></div>
                <div class="visual-desc">
                    <h4>2.2 Saphir Im Detail</h4>
                    <p><strong>Analyse:</strong> Hier sehen wir den 5D-Radius ($R \\approx 0.99$ nm) im Vergleich zum Saphir-Gitter ($a \\approx 0.47$ nm).</p>
                    <p><strong>Match:</strong> Das Verhältnis ist $2.08$. Die 5D-Welle ist genau doppelt so groß wie der Atomabstand.</p>
                </div>
            </div>

            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images['locking'])}" /></div>
                <div class="visual-desc">
                    <h4>2.3 Geometric Locking</h4>
                    <p><strong>Mechanismus:</strong> Die rote Welle symbolisiert die 5D-Metrik. Sie rastet bei jedem zweiten Atom ein (Locking Nodes).</p>
                    <p>Dies erklärt die extreme Härte und Stabilität von Saphir.</p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>3. Spektraler Beweis & Vorhersagen</h2>
            
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images['dispersion'])}" /></div>
                <div class="visual-desc">
                    <h4>3.1 Masse ist Index</h4>
                    <p><strong>Plot:</strong> Schwarz = Messdaten. Rot = Theorie.</p>
                    <p><strong>Aussage:</strong> Wir können die Dispersionskurve vorhersagen, indem wir annehmen, dass der Brechungsindex direkt proportional zur effektiven Masse ist.</p>
                </div>
            </div>

            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images['tower'])}" /></div>
                <div class="visual-desc">
                    <h4>3.2 Der Kaluza-Klein Turm (Vorhersage)</h4>
                    <p><strong>Prognose:</strong> Wenn die 5. Dimension real ist, muss es höhere Anregungszustände geben (wie Obertöne einer Geige).</p>
                    <p><strong>Werte (V4.2):</strong> Wir erwarten Absorptionslinien bei <strong>398 eV</strong> und <strong>597 eV</strong> (Soft X-Ray).</p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>4. Experimentelle Validierung</h2>
            
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images['kagra'])}" /></div>
                <div class="visual-desc">
                    <h4>4.1 Das KAGRA Anomalie</h4>
                    <p><strong>Fakt:</strong> Der KAGRA Detektor hat ein unbekanntes Rauschen bei tiefen Temperaturen.</p>
                    <p><strong>Erklärung:</strong> Unsere Simulation (Rot) reproduziert den thermischen Limit exakt. Es ist kein Defekt, sondern "Geometry Drag".</p>
                </div>
            </div>

            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images['conoscopy'])}" /></div>
                <div class="visual-desc">
                    <h4>4.2 Visuelle Bestätigung (Konoskopie)</h4>
                    <p>Das Interferenzmuster eines Kristalls entspricht exakt der Projektion eines 4D-Hyperwürfels. Materie ist Geometrie.</p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>5. Ausblick: Advanced Technology</h2>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images['cloaking'])}" /></div>
                <div class="visual-desc">
                    <h4>5.1 Invisibility Cloak</h4>
                    <p>Wenn wir $n(x)$ kontrollieren, kontrollieren wir die Raumzeit. Licht fließt um das Objekt herum wie Wasser.</p>
                </div>
            </div>
             <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images['blackhole'])}" /></div>
                <div class="visual-desc">
                    <h4>5.2 Optisches Schwarzes Loch</h4>
                    <p>Bei extrem hohen Intensitäten reißt der Brechungsindex die Raumzeit auf. Ein Ereignishorizont entsteht.</p>
                </div>
            </div>
        </div>

    </body>
    </html>
    """
    
    with open("QRS_Final_Report.html", "w", encoding="utf-8") as f:
        f.write(html_head)
    
    print(f"Report generated: QRS_Final_Report.html (Scientific Atlas Edition)")

    # PDF Generation
    try:
        from xhtml2pdf import pisa
        print("Exporting PDF...")
        pdf_filename = "QRS_Final_Report.pdf"
        with open(pdf_filename, "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(html_head, dest=pdf_file)
        
        if pisa_status.err:
            print("[WARNING] PDF generation had errors.")
        else:
            print(f"PDF generated: {pdf_filename}")
            
    except ImportError:
        print("[INFO] PDF export skipped (xhtml2pdf not installed).")

if __name__ == "__main__":
    generate_report()
