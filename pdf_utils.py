import PyPDF2

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages[:3]:  # 🔥 LIMIT PAGES
        extracted = page.extract_text()
        if extracted:
            text += extracted + " "
    return text

def clean_pdf_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text
