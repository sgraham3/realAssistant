from PyPDF2 import PdfReader, PdfWriter

def write_metadata(files, metadata):
    for file_path in files:
        reader = PdfReader(file_path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata({
            '/Title': metadata.get('Title', ''),
            '/Author': metadata.get('Author', ''),
            '/Subject': metadata.get('Subject', ''),
            '/Keywords': metadata.get('Keywords', ''),
        })
        with open(file_path, 'wb') as f:
            writer.write(f)
