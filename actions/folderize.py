# actions/folderize.py

import os
import shutil

def create_folder_for_each_pdf(files, gui):
    gui.progress_bar.config(maximum=len(files))
    gui.progress_bar["value"] = 0
    updated_paths = []

    for i, file_path in enumerate(files, 1):
        if not gui.is_running:
            gui.status_bar.config(text="Create folder operation cancelled.")
            break

        new_path = perform_create_folder(file_path, gui)
        if new_path and os.path.exists(new_path):
            updated_paths.append(new_path)
        elif os.path.exists(file_path):
            updated_paths.append(file_path)

        gui.progress_bar["value"] = i
        gui.status_bar.config(text=f"Processing file {i}/{len(files)}...")
        gui.root.update_idletasks()

    gui.current_files = updated_paths
    gui.status_bar.config(text="Folder creation complete.")

def perform_create_folder(file_path, gui):
    try:
        dir_name = os.path.dirname(file_path)
        base_filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(base_filename)[0]
        new_folder_path = os.path.join(dir_name, name_without_ext)

        if os.path.exists(new_folder_path):
            gui.status_bar.config(text=f"Skipped '{base_filename}': Folder exists.")
            return None

        os.makedirs(new_folder_path)
        new_file_path = os.path.join(new_folder_path, base_filename)
        shutil.move(file_path, new_file_path)
        return new_file_path
    except Exception as e:
        gui.status_bar.config(text=f"Error creating folder for {file_path}: {e}")
        return None
