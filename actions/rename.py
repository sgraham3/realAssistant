# actions/rename.py

import os

def rename_pdf(files, gui):
    gui.progress_bar.config(maximum=len(files))
    gui.progress_bar["value"] = 0
    updated_paths = []

    for i, file_path in enumerate(files, 1):
        if not gui.is_running:
            gui.status_bar.config(text="Renaming cancelled.")
            break

        new_path = rename_file(file_path, gui)
        if new_path and os.path.exists(new_path):
            updated_paths.append(new_path)
        elif os.path.exists(file_path):
            updated_paths.append(file_path)

        gui.progress_bar["value"] = i
        gui.status_bar.config(text=f"Renaming file {i}/{len(files)}...")
        gui.root.update_idletasks()

    gui.current_files = updated_paths
    gui.status_bar.config(text="Renaming completed.")

def rename_file(file_path, gui):
    try:
        dir_name = os.path.dirname(file_path)
        base_filename = os.path.basename(file_path)
        if len(base_filename) < 5:
            gui.status_bar.config(text=f"Skipped: '{base_filename}' too short for rename.")
            return None

        new_name = base_filename[5:]
        new_file_path = os.path.join(dir_name, new_name)

        if os.path.exists(new_file_path):
            gui.status_bar.config(text=f"Error: '{new_name}' already exists.")
            return None

        os.rename(file_path, new_file_path)
        return new_file_path
    except Exception as e:
        gui.status_bar.config(text=f"Error renaming {file_path}: {e}")
        return None
