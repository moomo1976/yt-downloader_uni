#!/usr/bin/env python3
"""
Convert Markdown documentation to PDF
"""
import markdown
import pdfkit
import os
from datetime import datetime

def convert_md_to_pdf(md_file_path, output_pdf_path):
    """Convert Markdown file to PDF"""
    try:
        # Read markdown file
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        md = markdown.Markdown(extensions=['tables', 'toc'])
        html_content = md.convert(md_content)
        
        # Add CSS styling for better PDF appearance
        html_with_style = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    border-bottom: 1px solid #bdc3c7;
                    padding-bottom: 5px;
                }}
                h3 {{
                    color: #7f8c8d;
                }}
                code {{
                    background-color: #f8f9fa;
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                }}
                pre {{
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-radius: 5px;
                    padding: 15px;
                    overflow-x: auto;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 15px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                    font-weight: bold;
                }}
                .emoji {{
                    font-size: 1.2em;
                }}
                blockquote {{
                    border-left: 4px solid #3498db;
                    margin: 0;
                    padding-left: 20px;
                    background-color: #f8f9fa;
                }}
            </style>
        </head>
        <body>
            {html_content}
            <hr style="margin-top: 50px; border: 1px solid #bdc3c7;">
            <p style="text-align: center; color: #7f8c8d; font-size: 0.9em;">
                Vygenerováno: {datetime.now().strftime('%d.%m.%Y %H:%M')} | YouTube Downloader Pro
            </p>
        </body>
        </html>
        """
        
        # PDF options for better formatting
        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }
        
        # Convert HTML to PDF
        pdfkit.from_string(html_with_style, output_pdf_path, options=options)
        print(f"PDF uspesne vytvoren: {output_pdf_path}")
        return True
        
    except Exception as e:
        print(f"Chyba pri konverzi: {e}")
        
        # Fallback - simple HTML to PDF without wkhtmltopdf
        try:
            from weasyprint import HTML, CSS
            HTML(string=html_with_style).write_pdf(output_pdf_path)
            print(f"PDF vytvoren pomoci WeasyPrint: {output_pdf_path}")
            return True
        except ImportError:
            print("Zkousim alternativni metodu...")
            
            # Last resort - save as HTML
            html_path = output_pdf_path.replace('.pdf', '.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_with_style)
            print(f"Ulozeno jako HTML: {html_path}")
            print("Pro PDF nainstalujte: pip install weasyprint")
            return False

if __name__ == "__main__":
    # Convert the main documentation
    md_file = "Release/NÁVOD.md"
    pdf_file = "Release/NÁVOD.pdf"
    
    if os.path.exists(md_file):
        print("Konvertuji NAVOD.md na PDF...")
        convert_md_to_pdf(md_file, pdf_file)
    else:
        print("NAVOD.md nenalezen!")