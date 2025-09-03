from PyPDF2 import PdfReader, PdfWriter

def merge_pdfs(files, output_path):
    writer = PdfWriter()
    for file_path in files:
        reader = PdfReader(file_path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, 'wb') as f:
        writer.write(f)
