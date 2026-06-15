from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(notes, transcript):

    pdf_path = "uploads/notes.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AI Generated Notes", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph(notes.replace("\n", "<br/>"), styles["BodyText"]))
    content.append(Spacer(1, 20))

    content.append(Paragraph("Transcript", styles["Heading2"]))
    content.append(Spacer(1, 12))

    content.append(
        Paragraph(
            transcript[:5000].replace("\n", "<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(content)

    return pdf_path