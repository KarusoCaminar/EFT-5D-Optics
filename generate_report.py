import os
import base64
import datetime

def get_base64_src(filepath, mime_type):
    if not filepath or not os.path.exists(filepath):
        return ""
    with open(filepath, "rb") as f:
        data = f.read()
    b64_data = base64.b64encode(data).decode('utf-8')
    return f"data:{mime_type};base64,{b64_data}"

def generate_report():
    print("--- Generating Professional Report (The Scientific Atlas V5.3) ---")
    
    # 1. VISUAL INVENTORY
    # We prioritize MP4s for the "Realtime" section (Chapter 7) for better quality in HTML.
    # We use PNGs/GIFs for everything else to ensure PDF compatibility.
    
    # Check if field explorer exists, otherwise use a fallback or skip
    field_gif = "images/animations/field_explorer.gif"
    if not os.path.exists(field_gif):
        # Fallback to a plot if animation is missing
        field_expl_src = "images/plots/field_explorer_snapshot.png" if os.path.exists("images/plots/field_explorer_snapshot.png") else ""
        field_type = "image"
    else:
        field_expl_src = field_gif
        field_type = "image" # It is a GIF image

    # MP4 Sources for Realtime Chapter (HTML Only - PDF will need static fallback logic if using xhtml2pdf, but simple img tags work best there)
    # Strategy: The user wants "MP4 videos directly embedded up top".
    # browsers handle <video> well. PDF converters DO NOT.
    # compromise: The script generates HTML. The HTML will use <video>.
    
    # INVENTORY
    inventory = {
        "tesseract": ("images/animations/tesseract_projection.gif", "image/gif"),
        "kaluza": ("images/plots/kaluza_klein_visualization.png", "image/png"),
        "ring": ("images/plots/quantum_ring_visualization.png", "image/png"),
        "metric": ("images/plots/metric_tensor_visualization.png", "image/png"),
        
        "scan": ("images/plots/material_resonance_scan.png", "image/png"),
        "lattice": ("images/plots/lattice_schematic.png", "image/png"),
        "locking": ("images/plots/experiment_locking.png", "image/png"),
        
        "dispersion": ("images/plots/dispersion_validation.png", "image/png"),
        "tower": ("images/plots/kk_tower_spectrum.png", "image/png"),
        
        "kagra": ("images/plots/kagra_noise_prediction.png", "image/png"),
        "galaxy": ("images/plots/galaxy_validation_analysis.png", "image/png"),
        "conoscopy": ("images/plots/experiment_conoscopy.png", "image/png"),
        
        "raytrace": ("images/plots/5d_raytracing_render.png", "image/png"),
        "diamond": ("images/plots/diamond_comparison.png", "image/png"),
        "stress": ("images/plots/stress_optics_5d.png", "image/png"),
        
        "tob": ("images/plots/quantum_tob_result.png", "image/png"),
        
        # Chapter 7 Realtime (Using MP4s where available and creating a video tag, else GIF)
        "cloaking": ("images/animations/cloaking_simulation.mp4", "video/mp4"),
        "prism": ("images/animations/prism_simulation.mp4", "video/mp4"),
        "fiber": ("images/plots/fiber_simulation.png", "image/png"), # Use the plot for fiber as it is static or generic
        "field": (field_expl_src, "image/gif") # Keep GIF for compatibility if MP4 missing
    }
    
    # Appendix Items
    appendix_inventory = {
        "Momentum Transfer (Impulserhaltung)": "images/plots/momentum_transfer.png",
        "Lorentz Invariance Proof": "images/plots/lorentz_proof.png",
        "Optical Black Hole (Event Horizon)": "images/plots/optical_black_hole.png",
        "Quantum Refractometer Data": "images/plots/quantum_refractometer_results_v2.png"
    }

    # Helper for rendering the visual card based on type
    def render_card(key, title, text):
        path, mime = inventory.get(key, ("", ""))
        if not path or not os.path.exists(path):
            return "" # Skip missing
        
        src = get_base64_src(path, mime)
        
        media_html = ""
        if "video" in mime:
            # HTML5 Video with Autoplay
            media_html = f'<video autoplay loop muted playsinline style="width:100%; height:auto;"><source src="{src}" type="{mime}"></video>'
        else:
            # Standard Image
             media_html = f'<img src="{src}" style="width:100%; height:auto;" />'

        return f"""
        <div class="visual-card">
            <div class="visual-media">{media_html}</div>
            <div class="visual-desc">
                <h4>{title}</h4>
                <p>{text}</p>
            </div>
        </div>
        """

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
            
            .header {{ text-align: center; margin-bottom: 50px; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            .section {{ margin-bottom: 50px; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); page-break-inside: avoid; }}
            
            .visual-card {{ display: flex; margin-bottom: 40px; background: #fff; border: 1px solid #eee; border-radius: 8px; overflow: hidden; page-break-inside: avoid; box-shadow: 0 2px 4px rgba(0,0,0,0.03); }}
            .visual-media {{ flex: 0 0 55%; background: #000; display: flex; align-items: center; justify-content: center; border-right: 1px solid #eee; padding: 0; min-height: 300px; }}
            .visual-desc {{ flex: 1; padding: 30px; display: flex; flex-direction: column; justify-content: center; }}
            .visual-desc h4 {{ margin-top: 0; color: #d35400; font-size: 14pt; margin-bottom: 15px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            
            .gallery-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; padding: 20px 0; }}
            .gallery-item {{ border: 1px solid #ddd; border-radius: 8px; overflow: hidden; background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            .gallery-item img {{ width: 100%; height: auto; display: block; }}
            .gallery-caption {{ padding: 10px; text-align: center; font-size: 9pt; color: #444; background: #fafafa; border-top: 1px solid #eee; font-weight: 600; }}
            
            @media print {{
                body {{ background: white; padding: 0; margin: 0; }}
                /* Videos won't print well, but images will */
            }}
        </style>
    </head>
    """

    html_body = f"""
    <body>
        <div class="header">
            <h1>QRS: The Effective Field Theory of 5D Optics</h1>
            <p><strong>The Scientific Atlas (Version 5.3 - Final Polish)</strong></p>
            <p class="timestamp">Generiert am: {datetime.datetime.now().strftime('%d. %B %Y')}</p>
        </div>

        <div class="section">
            <h2>1. Fundament: Die Geometrie des Raums</h2>
            {render_card("tesseract", "1.1 Die Projektion", "Materie ist der Schatten einer 5D-Struktur (Tesserakt-Rotation).")}
            {render_card("kaluza", "1.2 Der Kaluza-Klein Zylinder", "Ladung entsteht durch Impuls in der 5. Dimension.")}
        </div>

        <div class="section">
            <h2>2. Materie & Resonanz</h2>
            {render_card("scan", "2.1 Universeller Scan", "Alle stabilen Kristallgitter (Si, Al2O3) liegen auf 5D-Resonanzen.")}
            {render_card("lattice", "2.2 Saphir Locking", "Verhältnis 2.08: Geometrie wird vom Gitter erzwungen.")}
        </div>

        <div class="section">
            <h2>3. Spektrale Beweise</h2>
            {render_card("dispersion", "3.1 Dispersion", "Lichtbrechung wird durch die effektive Masse (~8.8 eV) verursacht.")}
            {render_card("tower", "3.2 Cutoff Scale", "Der EFT-Cutoff definiert die Grenze der geometrischen Optik.")}
        </div>

        <div class="section">
            <h2>4. Validierung</h2>
            {render_card("kagra", "4.1 KAGRA Noise", "Geometrisches Rauschen erklärt Gravitationswellen-Anomalien.")}
            {render_card("galaxy", "4.2 Data Connector: Galaxien", "Rotationskurven erklärt ohne Dunkle Materie (Geometry Drag).")}
            {render_card("conoscopy", "4.3 Visuelle Interferenz", "Konoskopie zeigt die 4D-Symmetrie im Kristall.")}
        </div>

        <div class="section">
            <h2>5. V5.0 Physics Engine</h2>
            {render_card("raytrace", "5.1 5D Raytracing (Engine)", "Lichtbahnen folgen Geodäten in der gekrümmten 5D-Metrik.")}
            {render_card("diamond", "5.2 Diamond Validation", "Vergleich: 5D-Sim (Weiß) vs. Snellius (Grün). Perfekte Übereinstimmung.")}
            {render_card("stress", "5.3 Stress-Optik", "Mechanische Spannung verändert die lokale Metrik (Isochromaten).")}
        </div>

        <div class="section">
            <h2>6. Quantum Architecture (TOB)</h2>
            {render_card("tob", "6.1 Das Optimale Gitter (Supraleitung)", "Globales Optimum bei 90° Twist-Winkel. Minimale geometrische Reibung.")}
        </div>

        <!-- 7. REALTIME SIMULATIONS (Revised) -->
        <div class="section">
            <h2>7. Echtzeit-Simulationen (Dynamik)</h2>
            <p>Die folgenden Simulationen zeigen die Zeitentwicklung der 5D-Wellenfunktion. Der "Lichtleiter" testet totale Reflexion.</p>
            
            {render_card("cloaking", "7.1 Invisibility Cloaking", "Die Metrik leitet die Wellenfronten um das Objekt herum (Active Flow).")}
            {render_card("prism", "7.2 Prismen-Brechung", "Echtzeit-Lösung der Wellengleichung im dispersiven Medium.")}
            {render_card("fiber", "7.3 5D Fiber Simulation", "Lichtleitung durch geometrische Totalreflexion (Core n=2).")}
            {render_card("field", "7.4 Field Explorer", "Visualisierung der 5D-Skalarfelder und ihrer Fluktuationen.")}
        </div>

        <!-- APPENDIX A: PLOTS -->
        <div class="section">
            <h2>Appendix A: Supplementary Archive</h2>
            <div class="gallery-grid">
            {
                "".join([
                    f'''
                    <div class="gallery-item">
                        <img src="{get_base64_src(path, 'image/png')}" />
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
    
    with open("QRS_Final_Report.html", "w", encoding="utf-8") as f:
        f.write(final_html)
    print("Report generated: QRS_Final_Report.html (Scientific Atlas Edition)")

    # PDF Logic (Simplified/Warning: PDF generation from <video> tags is tricky. PISA might ignore them)
    try:
        from xhtml2pdf import pisa
        with open("QRS_Final_Report.pdf", "wb") as pdf_file:
            pisa_status = pisa.CreatePDF(final_html, dest=pdf_file)
        if pisa_status.err:
            print("PDF generation error")
        else:
            print("PDF generated: QRS_Final_Report.pdf")
    except Exception as e:
        print(f"PDF Error: {e}")

if __name__ == "__main__":
    generate_report()
