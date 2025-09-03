# actions/taxmap_rename.py

import os

folder_code_map = {
    "NorwichC": "81100", "AftonT": "82089", "AftonV": "82001", "BainbridgeT": "82289",
    "BainbridgeV": "82201", "ColumbusT": "82400", "CoventryT": "82600", "GermanT": "82800",
    "GreeneT": "83089", "GreeneV": "83001", "GuilfordT": "83200", "LincklaenT": "83400",
    "McDonoughT": "83600", "NewBerlinT": "83889", "NewBerlinV": "83801", "NorthNorwichT": "84000",
    "NorwichT": "84200", "OtselicT": "84400", "OxfordT": "84689", "OxfordV": "84601",
    "PharsaliaT": "84800", "PitcherT": "85000", "PlymouthT": "85200", "PrestonT": "85400",
    "SherburneT": "85603", "EarlvilleV": "85601", "SmithvilleT": "85800", "SmyrnaT": "86089",
    "SmyrnaV": "86001"
}

keyword_replacements = {
    "ROAD": "001.00",
    "SECTION": "002.00",
    "GREATLOT": "003.00",
    "83": "",
}

suffix = ".2025"

def rename_pdfs_by_folder_code(files, gui):
    gui.progress_bar.config(maximum=len(files))
    gui.progress_bar["value"] = 0
    renamed_count = 0

    for i, file_path in enumerate(files, 1):
        if not gui.is_running:
            gui.status_bar.config(text="Taxmap renaming cancelled.")
            return

        try:
            root = os.path.dirname(file_path)
            folder_name = os.path.basename(root)

            matched_code = next((code for key, code in folder_code_map.items() if folder_name.startswith(key)), None)
            if not matched_code:
                gui.status_bar.config(text=f"Skipped: No code match for folder '{folder_name}'")
                continue

            name, ext = os.path.splitext(os.path.basename(file_path))
            new_name = name.replace(folder_name, matched_code)

            for old, new in keyword_replacements.items():
                new_name = new_name.replace(old, new)

            new_name = new_name.replace("-", ".")
            new_name = f"{new_name}{suffix}{ext}"

            new_path = os.path.join(root, new_name)
            os.rename(file_path, new_path)
            renamed_count += 1

        except Exception as e:
            gui.status_bar.config(text=f"Error renaming {file_path}: {e}")

        gui.progress_bar["value"] = i
        gui.root.update_idletasks()

    gui.status_bar.config(text=f"Renamed {renamed_count} file(s) using folder codes.")
