from PyPDF2 import PdfReader, PdfWriter
import os

def split_pdf(file_path):
    reader = PdfReader(file_path)
    base = os.path.splitext(file_path)[0]
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        with open(f"{base}_page_{i+1}.pdf", 'wb') as f:
            writer.write(f)
