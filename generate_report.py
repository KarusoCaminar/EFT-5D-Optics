import os
import base64
import datetime

def get_image_base64(filepath):
    if not filepath or not os.path.exists(filepath):
        return ""
    with open(filepath, "rb") as image_file:
        data = image_file.read()
    return base64.b64encode(data).decode('utf-8')

def generate_report():
    print("--- Generating Professional Report (The Scientific Atlas V5.2) ---")
    
    # Files to include (The Master Inventory)
    images_inventory = {
        # 1. GEOMETRY
        "tesseract": "images/animations/tesseract_projection.gif",
        "kaluza": "images/plots/kaluza_klein_visualization.png",
        "ring": "images/plots/quantum_ring_visualization.png",
        "metric": "images/plots/metric_tensor_visualization.png",
        
        # 2. MATTER
        "scan": "images/plots/material_resonance_scan.png",
        "lattice": "images/plots/lattice_schematic.png",
        "locking": "images/plots/experiment_locking.png",
        
        # 3. SPECTRUM
        "dispersion": "images/plots/dispersion_validation.png",
        "tower": "images/plots/kk_tower_spectrum.png",
        
        # 4. VALIDATION
        "kagra": "images/plots/kagra_noise_prediction.png",
        "conoscopy": "images/plots/experiment_conoscopy.png",
        "galaxy": "images/plots/galaxy_validation_analysis.png",
        
        # 5. ENGINE
        "raytrace": "images/plots/5d_raytracing_render.png",
        "diamond": "images/plots/diamond_comparison.png",
        "stress": "images/plots/stress_optics_5d.png",
        
        # 6. TOB
        "tob": "images/plots/quantum_tob_result.png",
        
        # 7. ANIMATIONS (For Main Body)
        "cloaking": "images/animations/cloaking_simulation.gif",
        "prism": "images/animations/prism_simulation.gif",
        "field": "images/animations/field_explorer.gif"
    }
    
    # Appendix Inventory (Curated)
    appendix_inventory = {
        "Momentum Transfer (Impulserhaltung)": "images/plots/momentum_transfer.png",
        "Lorentz Invariance Proof": "images/plots/lorentz_proof.png",
        "Optical Black Hole (Event Horizon)": "images/plots/optical_black_hole.png",
        "5D Fiber Simulation": "images/plots/fiber_simulation.png",
        "Quantum Refractometer Data": "images/plots/quantum_refractometer_results_v2.png"
    }

    # HTML Header
    html_head = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>QRS Final Report: The Scientific Atlas</title>
        <style>
            body {{ font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 1000px; margin: 0 auto; padding: 40px; background-color: #f9f9f9; }}
            h1 {{ color: #2c3e50; border-bottom: 4px solid #3498db; padding-bottom: 15px; text-align: center; font-size: 28pt; margin-bottom: 30px; letter-spacing: 1px; }}
            h2 {{ color: #2980b9; margin-top: 60px; border-bottom: 2px solid #bdc3c7; padding-bottom: 10px; font-size: 20pt; page-break-after: avoid; }}
            h3 {{ color: #16a085; margin-top: 30px; font-size: 16pt; }}
            p {{ font-size: 11pt; text-align: justify; margin-bottom: 15px; }}
            
            .header {{ text-align: center; margin-bottom: 50px; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            .section {{ margin-bottom: 50px; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); page-break-inside: avoid; }}
            
            .visual-card {{ display: flex; margin-bottom: 40px; background: #fff; border: 1px solid #eee; border-radius: 8px; overflow: hidden; page-break-inside: avoid; box-shadow: 0 2px 4px rgba(0,0,0,0.03); }}
            .visual-card:last-child {{ margin-bottom: 0; }}
            .visual-img {{ flex: 0 0 55%; background: #f8f9fa; display: flex; align-items: center; justify-content: center; border-right: 1px solid #eee; padding: 0; }}
            .visual-img img {{ width: 100%; height: auto; display: block; }}
            .visual-desc {{ flex: 1; padding: 30px; display: flex; flex-direction: column; justify-content: center; }}
            .visual-desc h4 {{ margin-top: 0; color: #d35400; font-size: 14pt; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            
            .gallery-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; padding: 20px 0; }}
            .gallery-item {{ border: 1px solid #ddd; border-radius: 8px; overflow: hidden; background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            .gallery-item img {{ width: 100%; height: auto; display: block; }}
            .gallery-item video {{ width: 100%; height: auto; display: block; }}
            .gallery-caption {{ padding: 15px; text-align: center; font-size: 10pt; color: #444; background: #fafafa; border-top: 1px solid #eee; font-weight: 600; }}
            
            @media print {{
                body {{ background: white; padding: 0; margin: 0; }}
                .gallery-grid {{ display: block; }}
                .gallery-item {{ margin-bottom: 20px; page-break-inside: avoid; }}
            }}
        </style>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    </head>
    """

    html_body = f"""
    <body>
        <div class="header">
            <h1>QRS: The Effective Field Theory of 5D Optics</h1>
            <p><strong>The Scientific Atlas (Version 5.2 - Final Polish)</strong></p>
            <p class="timestamp">Generiert am: {datetime.datetime.now().strftime('%d. %B %Y')}</p>
        </div>

        <!-- CHAPTERS 1-6 (Standard Structure) -->
        <div class="section">
            <h2>1. Fundament: Die Geometrie des Raums</h2>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/gif;base64,{get_image_base64(images_inventory.get('tesseract'))}" /></div>
                <div class="visual-desc"><h4>1.1 Die Projektion</h4><p>Materie ist der Schatten einer 5D-Struktur (Tesserakt-Rotation).</p></div>
            </div>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('kaluza'))}" /></div>
                <div class="visual-desc"><h4>1.2 Der Kaluza-Klein Zylinder</h4><p>Ladung entsteht durch Impuls in der 5. Dimension.</p></div>
            </div>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('ring'))}" /></div>
                <div class="visual-desc"><h4>1.3 Quantisierung</h4><p>Elektronen sind stehende Wellen (grün = stabil).</p></div>
            </div>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('metric'))}" /></div>
                <div class="visual-desc"><h4>1.4 Der Metrische Spanner</h4><p>Brechungsindex = Raumzeit-Dichte.</p></div>
            </div>
        </div>

        <div class="section">
            <h2>2. Materie & Resonanz</h2>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('scan'))}" /></div>
                <div class="visual-desc"><h4>2.1 Universeller Scan</h4><p>Alle stabilen Kristallgitter (Si, Al2O3) liegen auf 5D-Resonanzen.</p></div>
            </div>
             <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('lattice'))}" /></div>
                <div class="visual-desc"><h4>2.2 Saphir Locking</h4><p>Verhältnis 2.08: Geometrie wird vom Gitter erzwungen.</p></div>
            </div>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('locking'))}" /></div>
                <div class="visual-desc"><h4>2.3 Geometric Locking</h4><p>Nyquist-Limit Stabilisierung bei 199 eV.</p></div>
            </div>
        </div>

        <div class="section">
            <h2>3. Spektrale Beweise</h2>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('dispersion'))}" /></div>
                <div class="visual-desc"><h4>3.1 Dispersion</h4><p>Lichtbrechung wird durch die effektive Masse (~8.8 eV) verursacht.</p></div>
            </div>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('tower'))}" /></div>
                <div class="visual-desc"><h4>3.2 Cutoff Scale</h4><p>Der EFT-Cutoff definiert die Grenze der geometrischen Optik.</p></div>
            </div>
        </div>

        <div class="section">
            <h2>4. Validierung</h2>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('kagra'))}" /></div>
                <div class="visual-desc"><h4>4.1 KAGRA Noise</h4><p>Geometrisches Rauschen erklärt Gravitationswellen-Anomalien.</p></div>
            </div>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('galaxy'))}" /></div>
                <div class="visual-desc"><h4>4.2 Data Connector: Galaxien</h4><p>Rotationskurven erklärt ohne Dunkle Materie (Geometry Drag).</p></div>
            </div>
             <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('conoscopy'))}" /></div>
                <div class="visual-desc"><h4>4.3 Visuelle Interferenz</h4><p>Konoskopie zeigt die 4D-Symmetrie im Kristall.</p></div>
            </div>
        </div>

        <div class="section">
            <h2>5. V5.0 Physics Engine</h2>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('raytrace'))}" /></div>
                <div class="visual-desc"><h4>5.1 5D Raytracing (Engine)</h4><p>Lichtbahnen folgen Geodäten in der gekrümmten 5D-Metrik.</p></div>
            </div>
             <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('diamond'))}" /></div>
                <div class="visual-desc"><h4>5.2 Diamond Validation</h4><p>Vergleich: 5D-Sim (Weiß) vs. Snellius (Grün). Perfekte Übereinstimmung.</p></div>
            </div>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('stress'))}" /></div>
                <div class="visual-desc"><h4>5.3 Stress-Optik</h4><p>Mechanische Spannung verändert die lokale Metrik (Isochromaten).</p></div>
            </div>
        </div>

        <div class="section">
            <h2>6. Quantum Architecture (TOB)</h2>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images_inventory.get('tob'))}" /></div>
                <div class="visual-desc">
                    <h4>6.1 Das Optimale Gitter (Supraleitung)</h4>
                    <p>Globales Optimum bei 90° Twist-Winkel. Minimale geometrische Reibung.</p>
                </div>
            </div>
        </div>

        <!-- 7. REALTIME SIMULATIONS (Standardized Layout) -->
        <div class="section">
            <h2>7. Echtzeit-Simulationen (Dynamik)</h2>
            <p>Hier untersuchen wir das dynamische Verhalten der Felder (Zeitabhängige Lösungen).</p>
            
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/gif;base64,{get_image_base64(images_inventory.get('cloaking'))}" /></div>
                <div class="visual-desc">
                    <h4>7.1 Invisibility Cloaking</h4>
                    <p>Die Metrik leitet die Wellenfronten um das Objekt herum.</p>
                </div>
            </div>

            <div class="visual-card">
                <div class="visual-img"><img src="data:image/gif;base64,{get_image_base64(images_inventory.get('prism'))}" /></div>
                <div class="visual-desc">
                    <h4>7.2 Prismen-Brechung</h4>
                    <p>Echtzeit-Lösung der Wellengleichung im Medium.</p>
                </div>
            </div>
            
             <div class="visual-card">
                <div class="visual-img"><img src="data:image/gif;base64,{get_image_base64(images_inventory.get('field'))}" /></div>
                <div class="visual-desc">
                    <h4>7.3 Field Explorer</h4>
                    <p>Visualisierung der 5D-Skalarfelder und ihrer Fluktuationen.</p>
                </div>
            </div>
        </div>

        <!-- APPENDIX A: IMAGES -->
        <div class="section">
            <h2>Appendix A: Supplementary Archive</h2>
            <p>Detaillierte Analyse-Plots und mathematische Beweise.</p>
            <div class="gallery-grid">
            {
                "".join([
                    f'''
                    <div class="gallery-item">
                        <img src="data:image/png;base64,{get_image_base64(path)}" />
                        <div class="gallery-caption">{title}</div>
                    </div>
                    '''
                    for title, path in appendix_inventory.items()
                    if os.path.exists(path)
                ])
            }
            </div>
        </div>

        <!-- APPENDIX B: VIDEOS (Restored) -->
        <div class="section">
            <h2>Appendix B: Video Animations (Source Files)</h2>
            <p>Alle generierten MP4-Simulationen im Überblick.</p>
            <div class="gallery-grid">
            {
                "".join([
                    f'''
                    <div class="gallery-item">
                        <video controls>
                            <source src="data:video/mp4;base64,{get_image_base64(os.path.join("images/animations", f))}" type="video/mp4">
                        </video>
                        <div class="gallery-caption">{f} (MP4)</div>
                    </div>
                    '''
                    for f in sorted(os.listdir("images/animations"))
                    if f.endswith(".mp4")
                ])
            }
            </div>
        </div>

    </body>
    </html>
    """

    final_html = html_head + html_body
    
    with open("QRS_Final_Report.html", "w", encoding="utf-8") as f:
        f.write(final_html)
    
    print("Report generated: QRS_Final_Report.html (Scientific Atlas Edition)")
    
    # PDF generation
    try:
        from xhtml2pdf import pisa
        with open("QRS_Final_Report.pdf", "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(final_html, dest=pdf_file)
        if pisa_status.err:
            print("PDF error")
        else:
            print("PDF generated: QRS_Final_Report.pdf")
    except Exception as e:
        print(f"PDF Error: {e}")

if __name__ == "__main__":
    generate_report()
