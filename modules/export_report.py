import markdown
import os
import base64
import re

def get_image_base64(filepath):
    # filepath coming from markdown is like "../images/..." or "images/..."
    # We need to resolve it relative to the MD file location (docs/)
    
    # Base dir: c:\Users\Moritz\Documents\QRS\docs
    base_dir = r"c:\Users\Moritz\Documents\QRS\docs"
    
    # Resolve path
    full_path = os.path.normpath(os.path.join(base_dir, filepath))
    
    if not os.path.exists(full_path):
        print(f"Warning: Image not found: {full_path}")
        return ""
        
    with open(full_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def export_report():
    input_file = r"c:\Users\Moritz\Documents\QRS\docs\Final_Scientific_Report.md"
    output_file = r"c:\Users\Moritz\Documents\QRS\Final_Report_Printable.html"
    
    print(f"Reading {input_file}...")
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read()

    # Pre-process images to embed them as Base64
    # Regex to find ![alt](path)
    # We want to replace path with data:image/...;base64,...
    
    def image_replacer(match):
        alt_text = match.group(1)
        path = match.group(2)
        
        # Determine mime type
        ext = os.path.splitext(path)[1].lower()
        mime = "image/png"
        if ext == ".gif": mime = "image/gif"
        if ext == ".jpg" or ext == ".jpeg": mime = "image/jpeg"
        
        b64 = get_image_base64(path)
        if b64:
            return f'<img src="data:{mime};base64,{b64}" alt="{alt_text}" style="max-width:100%;">' 
        else:
            return f'![{alt_text}]({path})'

    # Pattern: ![alt](url)
    text_embedded = re.sub(r'!\[(.*?)\]\((.*?)\)', image_replacer, text)

    # Convert to HTML
    html_body = markdown.markdown(text_embedded, extensions=['tables', 'fenced_code'])
    
    # Wrap in nice CSS for printing
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>QRS Final Report</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; max-width: 900px; margin: 0 auto; padding: 40px; line-height: 1.6; color: #333; }}
            h1, h2, h3 {{ color: #2c3e50; }}
            h1 {{ border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            img {{ display: block; margin: 20px auto; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            code {{ background: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-family: Consolas, monospace; }}
            pre {{ background: #f8f8f8; padding: 15px; overflow-x: auto; border-radius: 5px; }}
            @media print {{
                body {{ padding: 0; }}
                h1 {{ page-break-before: always; }}
                h1:first-of-type {{ page-break-before: auto; }}
            }}
        </style>
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <script>
          window.MathJax = {{ tex: {{ inlineMath: [['$', '$'], ['\\\\(', '\\\\)']] }} }};
        </script>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Success! Printable Report saved to: {output_file}")

if __name__ == "__main__":
    export_report()
