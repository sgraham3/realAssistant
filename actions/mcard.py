# actions/mcard.py

import os
import re

def remove_mcard_from_name(files, gui):
    gui.progress_bar.config(maximum=len(files))
    gui.progress_bar["value"] = 0
    updated_paths = []

    for i, file_path in enumerate(files, 1):
        if not gui.is_running:
            gui.status_bar.config(text="Remove MCARD operation cancelled.")
            break

        new_path = perform_remove_mcard(file_path, gui)
        if new_path and os.path.exists(new_path):
            updated_paths.append(new_path)
        elif os.path.exists(file_path):
            updated_paths.append(file_path)

        gui.progress_bar["value"] = i
        gui.status_bar.config(text=f"Processing file {i}/{len(files)}...")
        gui.root.update_idletasks()

    gui.current_files = updated_paths
    gui.status_bar.config(text="MCARD removal complete.")

def perform_remove_mcard(file_path, gui):
    try:
        dir_name = os.path.dirname(file_path)
        base_filename = os.path.basename(file_path)
        name_without_ext, ext = os.path.splitext(base_filename)

        new_name = re.sub(r'MCARD', '', name_without_ext, flags=re.IGNORECASE).strip(' _-')
        if not new_name or new_name == name_without_ext:
            gui.status_bar.config(text=f"Skipped '{base_filename}': No MCARD or empty name.")
            return None

        new_file_path = os.path.join(dir_name, new_name + ext)
        if os.path.exists(new_file_path) and os.path.abspath(file_path) != os.path.abspath(new_file_path):
            gui.status_bar.config(text=f"Error: '{new_name + ext}' already exists.")
            return None

        os.rename(file_path, new_file_path)
        return new_file_path
    except Exception as e:
        gui.status_bar.config(text=f"Error removing 'MCARD' from {file_path}: {e}")
        return None
