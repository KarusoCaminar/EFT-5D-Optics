import os
import base64
import datetime

def get_image_base64(filepath):
    if not filepath or not os.path.exists(filepath):
        # Return a placeholder or empty string if file missing
        return ""
    with open(filepath, "rb") as image_file:
        data = image_file.read()
    return base64.b64encode(data).decode('utf-8')

def generate_report():
    print("--- Generating Professional Report (The Scientific Atlas V5.1) ---")
    
    # Files to include (The Master Inventory - V5.1 TOB Edition)
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
        
        # 6. ANIMATIONS
        "cloaking": "images/animations/cloaking_simulation.gif",
        "prism": "images/animations/prism_simulation.gif",
        "field": "images/animations/field_explorer.gif",
        
        # 7. QUANTUM TOB (NEW)
        "tob": "images/plots/quantum_tob_result.png"
    }
    
    # Appendix Inventory (Curated)
    appendix_inventory = {
        "Impulsumleitung (Momentum Transfer)": "images/plots/momentum_transfer.png",
        "Lorentz-Invarianz & 5D-Konsistenz": "images/plots/lorentz_proof.png",
        "Das Optische Schwarze Loch (Eereignishorizont)": "images/plots/optical_black_hole.png",
        "5D-Lichtleiter (Fiber Simulation)": "images/plots/fiber_simulation.png",
        "Quanten-Refraktometer (Temperatur-Drift)": "images/plots/quantum_refractometer_results_v2.png"
    }
    
    # Helper to check if file exists
    images = {k: v for k, v in images_inventory.items() if os.path.exists(v)}

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
            .visual-desc p {{ margin-bottom: 10px; font-size: 10pt; line-height: 1.5; }}
            
            .callout {{ background: #fff3cd; border-left: 5px solid #ffc107; padding: 20px; margin: 30px 0; border-radius: 4px; }}
            
            .gallery-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; padding: 20px 0; }}
            .gallery-item {{ border: 1px solid #ddd; border-radius: 8px; overflow: hidden; background: white; }}
            .gallery-item img {{ width: 100%; height: auto; display: block; }}
            .gallery-caption {{ padding: 10px; text-align: center; font-size: 9pt; color: #555; background: #fafafa; border-top: 1px solid #eee; font-weight: 600; }}
            
            @media print {{
                body {{ background: white; padding: 0; margin: 0; }}
                .header, .section {{ box-shadow: none; border: none; padding: 0; margin-bottom: 30px; }}
                .visual-card {{ border: 1px solid #ddd; page-break-inside: avoid; }}
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
            <p><strong>The Scientific Atlas (Version 5.1 - Quantum Architecture)</strong></p>
            <p class="timestamp">Generiert am: {datetime.datetime.now().strftime('%d. %B %Y')}</p>
        </div>

        <div class="section">
            <h2>1. Fundament: Die Geometrie des Raums</h2>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/gif;base64,{get_image_base64(images.get('tesseract'))}" /></div>
                <div class="visual-desc"><h4>1.1 Die Projektion</h4><p>Materie ist der Schatten einer 5D-Struktur.</p></div>
            </div>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images.get('kaluza'))}" /></div>
                <div class="visual-desc"><h4>1.2 Der Kaluza-Klein Zylinder</h4><p>Ladung = Bewegung in 5D.</p></div>
            </div>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images.get('ring'))}" /></div>
                <div class="visual-desc"><h4>1.3 Quantisierung</h4><p>Elektronen sind stehende Wellen (grün = stabil).</p></div>
            </div>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images.get('metric'))}" /></div>
                <div class="visual-desc"><h4>1.4 Der Metrische Spanner</h4><p>Brechungsindex = Raumzeit-Dichte.</p></div>
            </div>
        </div>

        <div class="section">
            <h2>2. Materie: Der Resonanz-Beweis</h2>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images.get('scan'))}" /></div>
                <div class="visual-desc"><h4>2.1 Universeller Scan</h4><p>Silizium (N=0.5) und Saphir (N=2.0) folgen der 5D-Harmotik.</p></div>
            </div>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images.get('lattice'))}" /></div>
                <div class="visual-desc"><h4>2.2 Saphir Locking</h4><p>Verhältnis 2.08: Geometrie wird vom Gitter erzwungen.</p></div>
            </div>
        </div>

        <div class="section">
            <h2>3. Spektrum & Cutoff</h2>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images.get('dispersion'))}" /></div>
                <div class="visual-desc"><h4>3.1 Dispersion</h4><p>Die Masse der Fluktuationen (~8.8 eV) erzeugt die Lichtbrechung.</p></div>
            </div>
        </div>

        <div class="section">
            <h2>4. Validierung</h2>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images.get('kagra'))}" /></div>
                <div class="visual-desc"><h4>4.1 KAGRA Noise</h4><p>Geometrisches Rauschen bei 20K.</p></div>
            </div>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images.get('galaxy'))}" /></div>
                <div class="visual-desc"><h4>4.2 Data Connector: Galaxien</h4><p>Rotation ohne Dunkle Materie erklärt durch 5D-Metrik.</p></div>
            </div>
        </div>

        <div class="section">
            <h2>5. V5.0 Physics Engine</h2>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images.get('raytrace'))}" /></div>
                <div class="visual-desc"><h4>5.1 5D Raytracing</h4><p>Prozedurale Berechnung von Geodäten (Lichtkrümmung).</p></div>
            </div>
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images.get('diamond'))}" /></div>
                <div class="visual-desc"><h4>5.2 Beweis: Brechung = Geometrie</h4><p>Weiß (5D) und Grün (Snellius) sind identisch.</p></div>
            </div>
        </div>

        <!-- NEW CHAPTER -->
        <div class="section">
            <h2>6. Quantum Architecture (TOB)</h2>
            <p>Neu in V5.1: Wir wenden <strong>Topology Optimization (TOB)</strong> auf die Raumzeit an. Ziel: Ein Gitter ohne geometrische Reibung (Supraleitung).</p>
            
            <div class="visual-card">
                <div class="visual-img"><img src="data:image/png;base64,{get_image_base64(images.get('tob'))}" /></div>
                <div class="visual-desc">
                    <h4>6.1 Das Optimale Gitter</h4>
                    <p><strong>Die Simulation:</strong> Ein evolutionärer Algorithmus sucht die perfekten Gitter-Parameter.</p>
                    <p><strong>Ergebnis:</strong> Ein Twist-Winkel von ~90° minimiert die effektive Masse. Das erklärt "Magic Angle Graphene".</p>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>7. Echtzeit-Simulationen</h2>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div class="visual-card" style="margin:0; flex-direction:column;">
                     <div class="visual-img" style="border:none; border-bottom:1px solid #eee;"><img src="data:image/gif;base64,{get_image_base64(images.get('cloaking'))}" /></div>
                     <div class="visual-desc" style="padding:15px;"><h4>Cloaking</h4></div>
                </div>
                <div class="visual-card" style="margin:0; flex-direction:column;">
                     <div class="visual-img" style="border:none; border-bottom:1px solid #eee;"><img src="data:image/gif;base64,{get_image_base64(images.get('prism'))}" /></div>
                     <div class="visual-desc" style="padding:15px;"><h4>Prisma</h4></div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Appendix A: Supplementary Archive</h2>
            <p>Vertiefende Analysen (Kuratiert).</p>
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
    </body>
    </html>
    """

    final_html = html_head + html_body
    
    with open("QRS_Final_Report.html", "w", encoding="utf-8") as f:
        f.write(final_html)
    
    print("Report generated: QRS_Final_Report.html (Scientific Atlas Edition)")
    
    # PDF Conversion attempt
    try:
        from xhtml2pdf import pisa
        with open("QRS_Final_Report.pdf", "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(final_html, dest=pdf_file)
        if pisa_status.err:
            print("PDF generation error")
        else:
            print("PDF generated: QRS_Final_Report.pdf")
    except ImportError:
        print("xhtml2pdf not installed, skipping PDF generation.")
    except Exception as e:
        print(f"PDF Error: {e}")

if __name__ == "__main__":
    generate_report()
