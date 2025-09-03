# actions/rotate.py
from PyPDF2 import PdfReader, PdfWriter

def rotate_pdf(files, angle, gui):
    for file_path in files:
        if not gui.is_running:
            gui.status_bar.config(text="Rotate PDF cancelled.")
            return
        try:
            with open(file_path, 'rb') as f:
                reader = PdfReader(f)
                writer = PdfWriter()
                for page in reader.pages:
                    page.rotate(angle)
                    writer.add_page(page)
            with open(file_path, 'wb') as f:
                writer.write(f)
            gui.status_bar.config(text=f"Rotated {file_path}")
        except Exception as e:
            gui.status_bar.config(text=f"Error rotating {file_path}: {e}")
