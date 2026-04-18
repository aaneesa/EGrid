import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

def generate_pdf(report_text: str, filename="ev_report.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)
    styles = getSampleStyleSheet()
    
    elements = []
    
    lines = report_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            elements.append(Spacer(1, 12))
            continue
            
        # 1. Escape XML characters
        line = line.replace('&', '&amp;')
        line = line.replace('<', '&lt;')
        line = line.replace('>', '&gt;')
        
        # 2. Identify style based on markdown prefix
        style = styles['Normal']
        if line.startswith('# '):
            style = styles['Heading1']
            line = line[2:].strip()
        elif line.startswith('## '):
            style = styles['Heading2']
            line = line[3:].strip()
        elif line.startswith('### '):
            style = styles['Heading3']
            line = line[4:].strip()
        elif line.startswith('- ') or line.startswith('* '):
            line = '&bull; ' + line[2:].strip()
            
        # 3. Apply inline markdown
        # Bold
        line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
        # Italic
        line = re.sub(r'\*(.+?)\*', r'<i>\1</i>', line)
        # Code
        line = re.sub(r'`(.+?)`', r'<font name="Courier">\1</font>', line)
        
        try:
            elements.append(Paragraph(line, style))
            elements.append(Spacer(1, 6))
        except Exception as e:
            # If ReportLab fails to parse the XML, just strip tags and render as normal
            clean_line = re.sub(r'<[^>]+>', '', line)
            elements.append(Paragraph(clean_line, style))
            elements.append(Spacer(1, 6))

    doc.build(elements)
    return filename