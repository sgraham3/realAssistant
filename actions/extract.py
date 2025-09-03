# actions/extract.py

import os
import re
import shutil
from PyPDF2 import PdfReader

def extract_and_rename(files, gui):
    gui.progress_bar.config(maximum=len(files))
    gui.progress_bar["value"] = 0
    updated_paths = []

    for i, file_path in enumerate(files, 1):
        if not gui.is_running:
            gui.status_bar.config(text="Extract and Rename cancelled.")
            break

        new_path = rename_pdf_from_text(file_path, gui)
        if new_path and os.path.exists(new_path):
            updated_paths.append(new_path)
        elif os.path.exists(file_path):
            updated_paths.append(file_path)

        gui.progress_bar["value"] = i
        gui.status_bar.config(text=f"Renaming file {i}/{len(files)}...")
        gui.root.update_idletasks()

    gui.current_files = updated_paths
    gui.status_bar.config(text="Extracting and renaming completed.")

def rename_pdf_from_text(file_path, gui):
    try:
        reader = PdfReader(file_path)
        if not reader.pages:
            gui.status_bar.config(text=f"Skipped {file_path}: No pages.")
            return None

        text = reader.pages[0].extract_text()
        if not text:
            gui.status_bar.config(text=f"Skipped {file_path}: No text.")
            return None

        match = re.search(r'(.*?)\s*east', text, re.IGNORECASE)
        if match:
            extracted_name = match.group(1).strip().replace(" ", "_")
            extracted_name = re.sub(r'[^\w_.-]', '', extracted_name)
            if not extracted_name:
                gui.status_bar.config(text=f"Skipped {file_path}: Empty name.")
                return None

            new_name = os.path.join(os.path.dirname(file_path), extracted_name + '.pdf')
            if os.path.exists(new_name) and os.path.abspath(file_path) != os.path.abspath(new_name):
                gui.status_bar.config(text=f"Error: '{extracted_name}.pdf' exists.")
                return None

            shutil.move(file_path, new_name)
            return new_name
        else:
            gui.status_bar.config(text=f"No pattern found in {file_path}")
            return None
    except Exception as e:
        gui.status_bar.config(text=f"Error renaming {file_path}: {e}")
        return None
