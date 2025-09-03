# gui.py

import tkinter as tk
from tkinter import filedialog, ttk
import os
import threading
import sys

from actions import bookmarks
from actions import taxmap_rename
from utils.config_loader import load_metadata
from actions import (
    metadata, rotate, split, merge, rename, extract,
    swisscode, mcard, folderize, remove_page
)

class PDFCreateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("realAssistant")
        self.root.geometry("500x550")

        # Load metadata
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        ini_path = os.path.join(application_path, 'metadata.ini')
        self.metadata = load_metadata(ini_path)

        self.is_running = False
        self.current_files = []

        # Action groups
        self.action_groups = {
            "MCARD Operations": [
                "Remove MCARD From Name",
                "Create Folder For Each PDF",
                "Split PDF",
                "Extract and Rename",
                "Add Swiss Code To Name",
            ],
            "PDF Content": [
                "Remove First Page",
                "Rotate PDF",
                "Merge PDF",
            ],
            "Metadata": [
                "Remove All Metadata",
                "Write Metadata",
            ],
            "Taxmaps Operations": [
                "Split PDF by Bookmarks",
                "Rename PDFs by Folder Code",
            ],
        }   

        # File list
        self.file_listbox = tk.Listbox(root, height=10, width=60, selectmode=tk.MULTIPLE)
        self.file_listbox.pack(pady=10)

        # File buttons
        button_frame = tk.Frame(root)
        button_frame.pack()
        tk.Button(button_frame, text="Add File(s)", command=self.add_files).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Add Folder", command=self.add_folder).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete", command=self.delete_file).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Clear", command=self.clear_files).grid(row=0, column=3, padx=5)

        # Group selection
        ttk.Label(root, text="Select Action Group:").pack(pady=5)
        self.group_cb = ttk.Combobox(root, width=30, values=list(self.action_groups.keys()))
        self.group_cb.current(0)
        self.group_cb.pack()
        self.group_cb.bind("<<ComboboxSelected>>", self.on_group_select)

        # Action selection
        ttk.Label(root, text="Choose Action:").pack(pady=5)
        self.action_cb = ttk.Combobox(root, width=30)
        self.action_cb.pack()
        self.action_cb.bind("<<ComboboxSelected>>", self.on_action_select)

        # Metadata profile selection
        self.metadata_profile_frame = tk.Frame(root)
        ttk.Label(self.metadata_profile_frame, text="Select Metadata Profile:").pack(pady=2)
        self.profile_cb = ttk.Combobox(self.metadata_profile_frame, width=30, values=list(self.metadata.keys()))
        self.profile_cb.current(0)
        self.profile_cb.pack(pady=2)
        self.metadata_profile_frame.pack_forget()

        # Rotation options
        self.rotation_options_frame = tk.Frame(root)
        ttk.Label(self.rotation_options_frame, text="Rotation Angle:").pack(pady=2)
        self.rotation_angle_cb = ttk.Combobox(self.rotation_options_frame, width=30, values=[90, 180, 270])
        self.rotation_angle_cb.current(0)
        self.rotation_angle_cb.pack(pady=2)
        self.rotation_options_frame.pack_forget()

        # Execute/Cancel buttons
        self.button_frame2 = tk.Frame(root)
        self.button_frame2.pack(pady=10)
        self.execute_button = tk.Button(self.button_frame2, text="Execute Action", command=self.execute_action)
        self.execute_button.grid(row=0, column=0, padx=5)
        self.cancel_button = tk.Button(self.button_frame2, text="Cancel", command=self.cancel_action)
        self.cancel_button.grid(row=0, column=1, padx=5)

        # Status and progress
        self.status_bar = tk.Label(root, text="Ready", relief=tk.SUNKEN, anchor="w")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(side=tk.BOTTOM, pady=5)

        # Initialize actions for the first group
        self.update_action_list(self.group_cb.get())

    # Group and action logic
    def on_group_select(self, event):
        selected_group = self.group_cb.get()
        self.update_action_list(selected_group)

    def update_action_list(self, group_name):
        actions = self.action_groups.get(group_name, [])
        self.action_cb["values"] = actions
        if actions:
            self.action_cb.current(0)
        self.on_action_select(None)

    def on_action_select(self, event):
        self.rotation_options_frame.pack_forget()
        self.metadata_profile_frame.pack_forget()
        selected_action = self.action_cb.get()
        if selected_action == "Rotate PDF":
            self.rotation_options_frame.pack(pady=5, before=self.button_frame2)
        elif selected_action == "Write Metadata":
            self.metadata_profile_frame.pack(pady=5, before=self.button_frame2)

    # File management
    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for file in files:
            if file not in self.current_files:
                self.current_files.append(file)
        self.refresh_file_listbox()

    def add_folder(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            for root_dir, _, files in os.walk(folder):
                for filename in files:
                    if filename.lower().endswith(".pdf"):
                        file_path = os.path.join(root_dir, filename)
                        if file_path not in self.current_files:
                            self.current_files.append(file_path)
        self.refresh_file_listbox()

    def delete_file(self):
        selected_indices = self.file_listbox.curselection()
        for i in reversed(selected_indices):
            del self.current_files[i]
        self.refresh_file_listbox()

    def clear_files(self):
        self.current_files.clear()
        self.refresh_file_listbox()

    def refresh_file_listbox(self):
        self.file_listbox.delete(0, tk.END)
        for file_path in self.current_files:
            self.file_listbox.insert(tk.END, file_path)

    # Execution
    def execute_action(self):
        action = self.action_cb.get()
        files = list(self.current_files)
        kwargs = {}

        if not self.is_running:
            self.is_running = True
            self.execute_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.NORMAL)

            if action == "Rotate PDF":
                try:
                    kwargs["rotation_angle"] = int(self.rotation_angle_cb.get())
                except ValueError:
                    self.status_bar.config(text="Invalid rotation angle selected.")
                    self.reset_buttons()
                    return
            elif action == "Write Metadata":
                profile = self.profile_cb.get()
                kwargs["metadata"] = self.metadata.get(profile, {})

            threading.Thread(target=self.run_action, args=(action, files), kwargs=kwargs).start()

    def run_action(self, action, files, **kwargs):
        try:
            if action == "Write Metadata":
                metadata.write_metadata(files, kwargs.get("metadata"), self)
            elif action == "Split PDF":
                split.split_pdf(files, self)
            elif action == "Merge PDF":
                merge.merge_pdf(files, self)
            elif action == "Rename PDF":
                rename.rename_pdf(files, self)
            elif action == "Extract and Rename":
                extract.extract_and_rename(files, self)
            elif action == "Add Swiss Code To Name":
                swisscode.add_swiss_code_to_name(files, self)
            elif action == "Remove All Metadata":
                metadata.remove_all_metadata(files, self)
            elif action == "Remove MCARD From Name":
                mcard.remove_mcard_from_name(files, self)
            elif action == "Create Folder For Each PDF":
                folderize.create_folder_for_each_pdf(files, self)
            elif action == "Rotate PDF":
                rotate.rotate_pdf(files, kwargs.get("rotation_angle"), self)
            elif action == "Remove First Page":
                remove_page.remove_first_page_of_pdfs(files, self)
            elif action == "Split PDF by Bookmarks":
                bookmarks.split_pdf_by_bookmarks(files, self)
            elif action == "Rename PDFs by Folder Code":
                taxmap_rename.rename_pdfs_by_folder_code(files, self)
        finally:
            self.reset_buttons()
            self.root.after(100, self.update_internal_file_list)

    def cancel_action(self):
        self.is_running = False
        self.status_bar.config(text="Action Cancelled.")
        self.reset_buttons()
        self.root.after(100, self.update_internal_file_list)

    def reset_buttons(self):
        self.is_running = False
        self.execute_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.progress_bar["value"] = 0

    def update_internal_file_list(self):
        self.status_bar.config(text="Refreshing file list...")
        unique_dirs = {os.path.dirname(path) for path in self.current_files}
        new_files = []
        for directory in unique_dirs:
            if os.path.exists(directory):
                for root_dir, _, files in os.walk(directory):
                    for filename in files:
                        if filename.lower().endswith(".pdf"):
                            file_path = os.path.join(root_dir, filename)
                            if file_path not in new_files:
                                new_files.append(file_path)
        self.current_files = sorted(set(new_files))
        self.refresh_file_listbox()
        self.status_bar.config(text="Ready")
