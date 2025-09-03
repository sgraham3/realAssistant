# actions/swisscode.py

import os

def add_swiss_code_to_name(files, gui):
    gui.progress_bar.config(maximum=len(files))
    gui.progress_bar["value"] = 0
    updated_paths = []

    for i, file_path in enumerate(files, 1):
        if not gui.is_running:
            gui.status_bar.config(text="Adding Swiss code cancelled.")
            break

        new_path = perform_add_swiss_code(file_path, gui)
        if new_path and os.path.exists(new_path):
            updated_paths.append(new_path)
        elif os.path.exists(file_path):
            updated_paths.append(file_path)

        gui.progress_bar["value"] = i
        gui.status_bar.config(text=f"Processing file {i}/{len(files)}...")
        gui.root.update_idletasks()

    gui.current_files = updated_paths
    gui.status_bar.config(text="Swiss code addition complete.")

def perform_add_swiss_code(file_path, gui):
    try:
        dir_name = os.path.dirname(file_path)
        base_filename = os.path.basename(file_path)
        parent_dir_name = os.path.basename(dir_name)

        if not parent_dir_name:
            gui.status_bar.config(text=f"Skipped '{base_filename}': No parent dir name.")
            return None

        if base_filename.startswith(f"{parent_dir_name}_"):
            gui.status_bar.config(text=f"Skipped '{base_filename}': Already coded.")
            return file_path

        new_filename = f"{parent_dir_name}_{base_filename}"
        new_file_path = os.path.join(dir_name, new_filename)

        if os.path.exists(new_file_path):
            gui.status_bar.config(text=f"Error: '{new_filename}' already exists.")
            return None

        os.rename(file_path, new_file_path)
        return new_file_path
    except Exception as e:
        gui.status_bar.config(text=f"Error adding Swiss code to {file_path}: {e}")
        return None
