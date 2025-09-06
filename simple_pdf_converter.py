#!/usr/bin/env python3
"""
Simple Markdown to PDF converter using FPDF
"""
import re
import os
from fpdf import FPDF
from datetime import datetime

class SimplePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'YouTube Downloader Pro - Návod', 0, 1, 'C')
        self.ln(10)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Strana {self.page_no()} | Vygenerováno: {datetime.now().strftime("%d.%m.%Y %H:%M")}', 0, 0, 'C')

def convert_md_to_simple_pdf(md_file, pdf_file):
    """Convert Markdown to simple PDF"""
    try:
        # Read markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Create PDF
        pdf = SimplePDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Process line by line
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                pdf.ln(5)
                continue
                
            # Headers
            if line.startswith('# '):
                pdf.ln(10)
                pdf.set_font('Arial', 'B', 16)
                text = line[2:].strip()
                # Remove emojis for PDF compatibility
                text = re.sub(r'[^\w\s\-.,!?()]', '', text)
                pdf.cell(0, 10, text.encode('latin1', 'ignore').decode('latin1'), 0, 1)
                pdf.ln(5)
                
            elif line.startswith('## '):
                pdf.ln(8)
                pdf.set_font('Arial', 'B', 14)
                text = line[3:].strip()
                text = re.sub(r'[^\w\s\-.,!?()]', '', text)
                pdf.cell(0, 10, text.encode('latin1', 'ignore').decode('latin1'), 0, 1)
                pdf.ln(3)
                
            elif line.startswith('### '):
                pdf.ln(5)
                pdf.set_font('Arial', 'B', 12)
                text = line[4:].strip()
                text = re.sub(r'[^\w\s\-.,!?()]', '', text)
                pdf.cell(0, 8, text.encode('latin1', 'ignore').decode('latin1'), 0, 1)
                pdf.ln(2)
                
            # Lists
            elif line.startswith('- ') or line.startswith('* '):
                pdf.set_font('Arial', '', 10)
                text = "• " + line[2:].strip()
                text = re.sub(r'[^\w\s\-.,!?()•]', '', text)
                pdf.cell(0, 6, text.encode('latin1', 'ignore').decode('latin1'), 0, 1)
                
            # Bold text (simplified)
            elif '**' in line:
                pdf.set_font('Arial', 'B', 10)
                text = line.replace('**', '')
                text = re.sub(r'[^\w\s\-.,!?()]', '', text)
                pdf.cell(0, 6, text.encode('latin1', 'ignore').decode('latin1'), 0, 1)
                
            # Code blocks
            elif line.startswith('```'):
                continue
                
            # Tables (simplified)
            elif '|' in line and not line.startswith('|---'):
                pdf.set_font('Arial', '', 9)
                parts = [p.strip() for p in line.split('|')[1:-1]]  # Remove empty first/last
                text = " | ".join(parts)
                text = re.sub(r'[^\w\s\-.,!?()|]', '', text)
                pdf.cell(0, 5, text.encode('latin1', 'ignore').decode('latin1'), 0, 1)
                
            # Regular text
            elif line and not line.startswith('|---') and not line.startswith('```'):
                pdf.set_font('Arial', '', 10)
                text = re.sub(r'[^\w\s\-.,!?()]', '', line)
                if len(text.strip()) > 0:
                    # Split long lines
                    if len(text) > 80:
                        words = text.split()
                        current_line = ""
                        for word in words:
                            if len(current_line + word) > 80:
                                if current_line:
                                    pdf.cell(0, 6, current_line.encode('latin1', 'ignore').decode('latin1'), 0, 1)
                                current_line = word + " "
                            else:
                                current_line += word + " "
                        if current_line:
                            pdf.cell(0, 6, current_line.encode('latin1', 'ignore').decode('latin1'), 0, 1)
                    else:
                        pdf.cell(0, 6, text.encode('latin1', 'ignore').decode('latin1'), 0, 1)
        
        # Save PDF
        pdf.output(pdf_file)
        print(f"PDF uspesne vytvoren: {pdf_file}")
        return True
        
    except Exception as e:
        print(f"Chyba pri konverzi: {e}")
        return False

if __name__ == "__main__":
    md_file = "Release/NÁVOD.md"
    pdf_file = "Release/NÁVOD.pdf"
    
    if os.path.exists(md_file):
        print("Konvertuji NAVOD.md na PDF...")
        convert_md_to_simple_pdf(md_file, pdf_file)
    else:
        print("NAVOD.md nenalezen!")
        # List files to debug
        print("Soubory v Release:")
        try:
            for f in os.listdir("Release"):
                print(f"  - {f}")
        except:
            print("Slozka Release nenalezena!")