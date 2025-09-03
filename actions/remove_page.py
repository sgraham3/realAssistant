# actions/remove_page.py

from PyPDF2 import PdfReader, PdfWriter

def remove_first_page_of_pdfs(files, gui):
    gui.progress_bar.config(maximum=len(files))
    gui.progress_bar["value"] = 0

    for i, file_path in enumerate(files, 1):
        if not gui.is_running:
            gui.status_bar.config(text="Remove First Page cancelled.")
            return

        remove_first_page(file_path, gui)

        gui.progress_bar["value"] = i
        gui.root.update_idletasks()

    gui.status_bar.config(text="Remove First Page complete.")

def remove_first_page(file_path, gui):
    try:
        with open(file_path, 'rb') as infile:
            reader = PdfReader(infile)
            if len(reader.pages) <= 1:
                gui.status_bar.config(text=f"Skipped '{file_path}': One page or less.")
                return

            writer = PdfWriter()
            for page in reader.pages[1:]:
                writer.add_page(page)

        with open(file_path, 'wb') as outfile:
            writer.write(outfile)

        gui.status_bar.config(text=f"Removed first page from {file_path}")
    except Exception as e:
        gui.status_bar.config(text=f"Error removing first page from {file_path}: {e}")
