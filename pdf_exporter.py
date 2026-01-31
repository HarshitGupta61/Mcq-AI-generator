from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(mcqs, path):
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    x, y = 40, height - 40

    for i, mcq in enumerate(mcqs, start=1):
        if y < 100:
            c.showPage()
            y = height - 40

        c.setFont("Helvetica-Bold", 11)
        c.drawString(x, y, f"Q{i}. {mcq['question']}")
        y -= 18

        c.setFont("Helvetica", 10)
        for key, value in mcq["options"].items():
            prefix = "✔ " if key == mcq["answer"] else ""
            c.drawString(x + 15, y, f"{prefix}{key}. {value}")
            y -= 14

        y -= 10

    c.save()
