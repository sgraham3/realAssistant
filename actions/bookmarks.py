# actions/bookmarks.py

import fitz  # PyMuPDF
import os
import re

def extract_bookmarks(doc):
    toc = doc.get_toc(simple=True)
    return [(title, page + 1) for level, title, page in toc]

def ensure_pdf_extension(name):
    return name if name.lower().endswith(".pdf") else name + ".pdf"

#def sanitize_filename(name):
#    return "".join(c if c.isalnum() or c in " _-" else "_" for c in name).strip()

def sanitize_filename(name):
    # Allow alphanumeric, space, underscore, hyphen, and dot
    name = re.sub(r'[^\w\s.-]', '_', name)
    # Replace multiple spaces or underscores with a single underscore
    name = re.sub(r'[\s_]+', '_', name)
    # Strip leading/trailing underscores or dots
    return name.strip('._')


def split_pdf_by_bookmarks(files, gui):
    gui.progress_bar.config(maximum=len(files))
    gui.progress_bar["value"] = 0

    for i, pdf_path in enumerate(files, 1):
        if not gui.is_running:
            gui.status_bar.config(text="Bookmark split cancelled.")
            return

        try:
            doc = fitz.open(pdf_path)
            bookmarks = extract_bookmarks(doc)
            total_pages = doc.page_count

            if not bookmarks:
                gui.status_bar.config(text=f"No bookmarks found in: {pdf_path}")
                continue

            output_dir = os.path.dirname(pdf_path)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]

            for j, (title, start_page) in enumerate(bookmarks):
                end_page = bookmarks[j + 1][1] - 1 if j + 1 < len(bookmarks) else total_pages
                new_doc = fitz.open()
                for page_num in range(start_page - 1, end_page):
                    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

                safe_title = sanitize_filename(title or f"bookmark_{j}")
                if safe_title.lower().startswith(base_name.lower()):
                    filename = ensure_pdf_extension(f"{safe_title}")
                else:
                    filename = ensure_pdf_extension(f"{base_name}_{safe_title}")

                output_path = os.path.join(output_dir, filename)
                new_doc.save(output_path)
                new_doc.close()

            doc.close()
            gui.status_bar.config(text=f"Split by bookmarks complete for {pdf_path}")
        except Exception as e:
            gui.status_bar.config(text=f"Error processing {pdf_path}: {e}")

        gui.progress_bar["value"] = i
        gui.root.update_idletasks()

    gui.status_bar.config(text="All bookmark splits complete.")
