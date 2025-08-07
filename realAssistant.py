import tkinter as tk
from tkinter import filedialog, ttk
import os
import threading
import configparser
from PyPDF2 import PdfReader, PdfWriter
import shutil
import re
import sys

class PDFCreateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("realAssistant")
        self.root.geometry("500x475")

        # Load metadata from ini file
        # self.metadata = self.load_metadata("metadata.ini")
        if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        ini_path = os.path.join(application_path, 'metadata.ini')

        self.metadata = self.load_metadata(ini_path)

        # Task running flag
        self.is_running = False

        # Store file paths internally
        self.current_files = [] 

        # File List
        self.file_listbox = tk.Listbox(root, height=10, width=60, selectmode=tk.MULTIPLE)
        self.file_listbox.pack(pady=10)

        # Buttons Frame (for Add, Delete, Clear)
        button_frame = tk.Frame(root)
        button_frame.pack()

        tk.Button(button_frame, text="Add File(s)", command=self.add_files).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Add Folder", command=self.add_folder).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Delete", command=self.delete_file).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Clear", command=self.clear_files).grid(row=0, column=3, padx=5)

        # Action Selection
        ttk.Label(root, text="Choose Action:").pack(pady=5)
        self.action_cb = ttk.Combobox(root, values=[
            "Remove MCARD From Name",
            "Create Folder For Each PDF",
            "Split PDF",
            "Extract and Rename",
            "Add Swiss Code To Name",
            "Remove All Metadata",
            "Write Metadata",
            "Merge PDF",
            "Rename PDF",
            "Rotate PDF",
            "Remove First Page" # NEW Action
        ])
        self.action_cb.current(0)
        self.action_cb.pack()
        self.action_cb.bind("<<ComboboxSelected>>", self.on_action_select)

        # Metadata Profile Selection Frame
        self.metadata_profile_frame = tk.Frame(root)
        ttk.Label(self.metadata_profile_frame, text="Select Metadata Profile:").pack(pady=2)
        self.profile_cb = ttk.Combobox(self.metadata_profile_frame, values=list(self.metadata.keys()))
        self.profile_cb.current(0)
        self.profile_cb.pack(pady=2)
        self.metadata_profile_frame.pack_forget() # Initially hidden

        # Rotation Options Frame
        self.rotation_options_frame = tk.Frame(root)
        ttk.Label(self.rotation_options_frame, text="Rotation Angle:").pack(pady=2)
        self.rotation_angle_cb = ttk.Combobox(self.rotation_options_frame, values=[90, 180, 270])
        self.rotation_angle_cb.current(0)
        self.rotation_angle_cb.pack(pady=2)
        self.rotation_options_frame.pack_forget() # Initially hidden

        # Define the Execute/Cancel buttons frame
        self.button_frame2 = tk.Frame(root)
        self.button_frame2.pack(pady=10)
        self.execute_button = tk.Button(self.button_frame2, text="Execute Action", command=self.execute_action)
        self.execute_button.grid(row=0, column=0, padx=5)
        self.cancel_button = tk.Button(self.button_frame2, text="Cancel", command=self.cancel_action)
        self.cancel_button.grid(row=0, column=1, padx=5)

        # Status bar
        self.status_bar = tk.Label(root, text="Ready", relief=tk.SUNKEN, anchor="w")
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Progress Bar
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(side=tk.BOTTOM, pady=5)

    def load_metadata(self, ini_file):
        config = configparser.ConfigParser()
        config.read(ini_file)
        metadata_dict = {}
        for section in config.sections():
            metadata_dict[section] = {
                'Title': config.get(section, 'Title', fallback=''),
                'Author': config.get(section, 'Author', fallback=''),
                'Subject': config.get(section, 'Subject', fallback=''),
                'Keywords': config.get(section, 'Keywords', fallback=''),
            }
        return metadata_dict

    def add_files(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        for file in files:
            if file not in self.current_files:
                self.current_files.append(file)
        self.refresh_file_listbox()

    def add_folder(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            new_files_added = []
            for root_dir, _, files in os.walk(folder):
                for filename in files:
                    if filename.lower().endswith(".pdf"):
                        file_path = os.path.join(root_dir, filename)
                        if file_path not in self.current_files:
                            new_files_added.append(file_path)
            self.current_files.extend(new_files_added)
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

    def on_action_select(self, event):
        """Handles the selection change in the action combobox to show/hide options."""
        selected_action = self.action_cb.get()

        # Hide all option frames first
        self.rotation_options_frame.pack_forget()
        self.metadata_profile_frame.pack_forget()

        # Show specific option frames based on selection
        if selected_action == "Rotate PDF":
            self.rotation_options_frame.pack(pady=5, before=self.button_frame2)
        elif selected_action == "Write Metadata":
            self.metadata_profile_frame.pack(pady=5, before=self.button_frame2)


    def execute_action(self):
        action = self.action_cb.get()
        if not self.is_running:
            self.is_running = True
            self.execute_button.config(state=tk.DISABLED)
            self.cancel_button.config(state=tk.NORMAL)
            
            thread_args = (action, list(self.current_files))
            
            if action == "Rotate PDF":
                try:
                    rotation_angle = int(self.rotation_angle_cb.get())
                    thread_args = (action, list(self.current_files), rotation_angle)
                except ValueError:
                    self.status_bar.config(text="Invalid rotation angle selected.")
                    self.is_running = False
                    self.execute_button.config(state=tk.NORMAL)
                    self.cancel_button.config(state=tk.DISABLED)
                    return
            elif action == "Write Metadata":
                selected_profile = self.profile_cb.get()
                if selected_profile in self.metadata:
                    self.selected_metadata = self.metadata[selected_profile]
                else:
                    self.selected_metadata = {}
                thread_args = (action, list(self.current_files), None, self.selected_metadata) # Pass selected_metadata
            # No special UI for "Remove First Page", so no extra elif here for its UI elements

            threading.Thread(target=self.run_action, args=thread_args).start()

    def run_action(self, action, files_to_process, rotation_angle=None, metadata_to_write=None):
        try:
            if action == "Write Metadata":
                self.write_metadata(files_to_process, metadata_to_write)
            elif action == "Split PDF":
                self.split_pdf(files_to_process)
            elif action == "Merge PDF":
                self.merge_pdf(files_to_process)
            elif action == "Rename PDF":
                self.rename_pdf(files_to_process)
            elif action == "Extract and Rename":
                self.extract_and_rename(files_to_process)
            elif action == "Add Swiss Code To Name":
                self.add_swiss_code_to_name(files_to_process)
            elif action == "Remove All Metadata":
                self.remove_all_metadata(files_to_process)
            elif action == "Remove MCARD From Name":
                self.remove_mcard_from_name(files_to_process)
            elif action == "Create Folder For Each PDF":
                self.create_folder_for_each_pdf(files_to_process)
            elif action == "Rotate PDF":
                if rotation_angle is not None:
                    self.rotate_pdf(files_to_process, rotation_angle)
                else:
                    self.status_bar.config(text="Error: Rotation angle not provided.")
                    print("Error: Rotation angle not provided for Rotate PDF action.")
            elif action == "Remove First Page": # NEW: Call the new action method
                self.remove_first_page_of_pdfs(files_to_process)

        finally:
            self.is_running = False
            self.execute_button.config(state=tk.NORMAL)
            self.cancel_button.config(state=tk.DISABLED)
            self.progress_bar["value"] = 0
            self.root.after(100, self.update_internal_file_list) 

    def update_internal_file_list(self):
        """
        Scans the directories of the previously added files to find their new locations
        and updates self.current_files, then refreshes the Listbox.
        This is crucial for renamed/moved files.
        """
        self.status_bar.config(text="Refreshing file list...")
        
        unique_directories = set()
        for old_path in self.current_files:
            unique_directories.add(os.path.dirname(old_path))

        temp_new_files = []
        for directory in unique_directories:
            if os.path.exists(directory):
                for root_dir, _, files in os.walk(directory):
                    for filename in files:
                        if filename.lower().endswith(".pdf"):
                            file_path = os.path.join(root_dir, filename)
                            if file_path not in temp_new_files:
                                temp_new_files.append(file_path)
        
        self.current_files = sorted(list(set(temp_new_files)))
        self.refresh_file_listbox()
        self.status_bar.config(text="Ready")
        print("File list refreshed.")

    def cancel_action(self):
        self.is_running = False
        self.status_bar.config(text="Action Cancelled.")
        print("Action cancelled.")
        self.execute_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.progress_bar["value"] = 0
        self.root.after(100, self.update_internal_file_list)

    def write_metadata(self, files_to_process, metadata_to_write):
        """Write metadata to PDFs."""
        print("Writing metadata...")
        total_files = len(files_to_process)
        processed_files = 0
        self.progress_bar.config(maximum=total_files)
        self.progress_bar["value"] = 0
        for file_path in files_to_process:
            if not self.is_running:
                self.status_bar.config(text="Metadata write cancelled.")
                return
            self.apply_metadata(file_path, metadata_to_write)
            processed_files += 1
            self.progress_bar["value"] = processed_files
            self.status_bar.config(text=f"Processing file {processed_files}/{total_files}...")
            self.root.update_idletasks()
        print("Finished writing metadata.")
        self.status_bar.config(text="Metadata writing complete.")

    def apply_metadata(self, file_path, metadata_to_apply):
        """Apply metadata changes to a single PDF."""
        try:
            base_filename = os.path.splitext(os.path.basename(file_path))[0]
            title_from_ini = metadata_to_apply.get('Title', '').strip()
            title = title_from_ini if title_from_ini else base_filename
            author = metadata_to_apply.get('Author', ' ')
            subject = metadata_to_apply.get('Subject', ' ')
            keywords = metadata_to_apply.get('Keywords', ' ')

            with open(file_path, 'rb') as input_file:
                reader = PdfReader(input_file)
                writer = PdfWriter()
                for page_num in range(len(reader.pages)):
                    writer.add_page(reader.pages[page_num])
                new_metadata = {
                    '/Title': title,
                    '/Author': author,
                    '/Subject': subject,
                    '/Keywords': keywords,
                }
                writer.add_metadata(new_metadata)
                with open(file_path, 'wb') as output_file:
                    writer.write(output_file)
            print(f"Metadata successfully applied to {file_path}")
            self.status_bar.config(text=f"Metadata successfully applied to {file_path}")
        except Exception as e:
            print(f"Error writing metadata to {file_path}: {e}")
            self.status_bar.config(text=f"Error writing metadata to {file_path}")

    def split_pdf(self, files_to_process):
        """Split PDFs into individual pages."""
        print("Splitting PDFs...")
        total_pages_overall = sum([self.count_pages(file) for file in files_to_process])
        self.progress_bar.config(maximum=total_pages_overall)
        self.progress_bar["value"] = 0
        current_processed_pages = 0
        
        for file_path in files_to_process:
            if not self.is_running:
                self.status_bar.config(text="Split PDF Cancelled.")
                return
            num_pages_in_file = self.count_pages(file_path)
            self.perform_split(file_path, current_processed_pages, total_pages_overall)
            current_processed_pages += num_pages_in_file
        print("Finished splitting PDFs.")
        self.status_bar.config(text="Finished splitting PDFs.")

    def perform_split(self, file_path, current_processed_pages, total_pages_overall):
        """Perform the actual split."""
        try:
            with open(file_path, "rb") as file:
                reader = PdfReader(file)
                total_pages_in_file = len(reader.pages)
                base_filename = os.path.splitext(os.path.basename(file_path))[0]
                directory = os.path.dirname(file_path)

                for page_num in range(total_pages_in_file):
                    if not self.is_running:
                        return
                    writer = PdfWriter()
                    writer.add_page(reader.pages[page_num])
                    output_filename = f"{base_filename}-{page_num + 1}.pdf"
                    output_file_path = os.path.join(directory, output_filename)
                    with open(output_file_path, "wb") as output_file:
                        writer.write(output_file)
                    self.progress_bar["value"] = current_processed_pages + (page_num + 1)
                    self.status_bar.config(text=f"Splitting '{base_filename}': Page {page_num + 1}/{total_pages_in_file} (Overall: {current_processed_pages + (page_num + 1)}/{total_pages_overall})")
                    self.root.update_idletasks()
            print(f"Successfully split {file_path}")
        except Exception as e:
            print(f"Error splitting {file_path}: {e}")
            self.status_bar.config(text=f"Error splitting {file_path}: {e}")

    def count_pages(self, file_path):
        """Count the number of pages in a PDF."""
        try:
            with open(file_path, 'rb') as f:
                reader = PdfReader(f)
                return len(reader.pages)
        except Exception as e:
            print(f"Error counting pages for {file_path}: {e}")
            return 0

    def merge_pdf(self, files_to_process):
        """Merge multiple PDFs into one."""
        print("Merging PDFs...")
        if not files_to_process:
            self.status_bar.config(text="No PDF files selected for merging.")
            print("No PDF files selected for merging.")
            self.is_running = False
            return
        output_file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if output_file_path:
            self.perform_merge(files_to_process, output_file_path)
        else:
            self.status_bar.config(text="Merge operation cancelled by user.")
            print("Merge operation cancelled by user.")
            self.is_running = False

    def perform_merge(self, files, output_file_path):
        """Perform the actual merge."""
        try:
            writer = PdfWriter()
            total_files = len(files)
            processed_files = 0
            self.progress_bar.config(maximum=total_files)
            self.progress_bar["value"] = 0
            for file_path in files:
                if not self.is_running:
                    self.status_bar.config(text="Merge cancelled.")
                    return
                with open(file_path, 'rb') as f:
                    reader = PdfReader(f)
                    for page_num in range(len(reader.pages)):
                        writer.add_page(reader.pages[page_num])
                processed_files += 1
                self.progress_bar["value"] = processed_files
                self.status_bar.config(text=f"Merging file {processed_files}/{total_files}...")
                self.root.update_idletasks()
            with open(output_file_path, 'wb') as output_file:
                writer.write(output_file)
            print(f"PDFs merged successfully into {output_file_path}")
            self.status_bar.config(text=f"PDFs merged successfully into {output_file_path}")
        except Exception as e:
            print(f"Error merging PDFs: {e}")
            self.status_bar.config(text=f"Error merging PDFs: {e}")
        finally:
            pass

    def rename_pdf(self, files_to_process):
        print("Renaming PDFs...")
        total_files = len(files_to_process)
        processed_files = 0
        self.progress_bar.config(maximum=total_files)
        self.progress_bar["value"] = 0
        updated_paths = []
        for file_path in files_to_process:
            if not self.is_running:
                self.status_bar.config(text="Renaming cancelled.")
                break
            new_path = self.rename_file(file_path)
            if new_path and os.path.exists(new_path):
                updated_paths.append(new_path)
            else:
                if os.path.exists(file_path):
                    updated_paths.append(file_path)
            processed_files += 1
            self.progress_bar["value"] = processed_files
            self.status_bar.config(text=f"Renaming file {processed_files}/{total_files}...")
            self.root.update_idletasks()
        self.current_files = updated_paths
        print("Renaming completed.")
        self.status_bar.config(text="Renaming completed.")

    def rename_file(self, file_path):
        """Remove the first 5 characters from the filename, returns new path or None."""
        try:
            dir_name = os.path.dirname(file_path)
            base_filename = os.path.basename(file_path)
            
            if len(base_filename) < 5:
                print(f"Skipping renaming for '{base_filename}': filename is too short to remove first 5 characters.")
                self.status_bar.config(text=f"Skipped: '{base_filename}' too short for rename.")
                return None

            new_name = base_filename[5:]
            new_file_path = os.path.join(dir_name, new_name)

            if os.path.exists(new_file_path):
                print(f"Error: A file with the new name '{new_file_path}' already exists. Skipping.")
                self.status_bar.config(text=f"Error: '{new_name}' already exists.")
                return None

            os.rename(file_path, new_file_path)
            print(f"Renamed {file_path} to {new_file_path}")
            return new_file_path
        except Exception as e:
            print(f"Error renaming {file_path}: {e}")
            self.status_bar.config(text=f"Error renaming {file_path}: {e}")
            return None

    def extract_and_rename(self, files_to_process):
        print("Extracting and Renaming PDFs...")
        total_files = len(files_to_process)
        processed_files = 0
        self.progress_bar.config(maximum=total_files)
        self.progress_bar["value"] = 0
        updated_paths = []
        for file_path in files_to_process:
            if not self.is_running:
                self.status_bar.config(text="Extract and Rename cancelled.")
                break
            new_path = self.rename_pdf_from_text(file_path)
            if new_path and os.path.exists(new_path):
                updated_paths.append(new_path)
            else:
                if os.path.exists(file_path):
                    updated_paths.append(file_path)
            processed_files += 1
            self.progress_bar["value"] = processed_files
            self.status_bar.config(text=f"Renaming file {processed_files}/{total_files}...")
            self.root.update_idletasks()
        self.current_files = updated_paths
        print("Extracting and renaming completed.")
        self.status_bar.config(text="Extracting and renaming completed.")

    def rename_pdf_from_text(self, file_path):
        try:
            pdf_reader = PdfReader(file_path)
            if not pdf_reader.pages:
                print(f"Skipping {file_path}: PDF has no pages.")
                self.status_bar.config(text=f"Skipped {file_path}: No pages.")
                return None
            page = pdf_reader.pages[0]
            text = page.extract_text()
            if not text:
                print(f"Skipping {file_path}: No text found on the first page.")
                self.status_bar.config(text=f"Skipped {file_path}: No text.")
                return None
            match = re.search(r'(.*?)\s*east', text, re.IGNORECASE)
            if match:
                extracted_name = match.group(1).strip().replace(" ", "_")
                extracted_name = re.sub(r'[^\w_.-]', '', extracted_name)
                if not extracted_name:
                    print(f"Skipping {file_path}: Extracted name is empty after cleaning.")
                    self.status_bar.config(text=f"Skipped {file_path}: Empty name.")
                    return None
                original_folder = os.path.dirname(file_path)
                new_name = os.path.join(original_folder, extracted_name + '.pdf')
                if os.path.exists(new_name) and os.path.abspath(file_path) != os.path.abspath(new_name):
                    print(f"Error: A file with the new name '{new_name}' already exists. Skipping renaming for {file_path}.")
                    self.status_bar.config(text=f"Error: '{extracted_name}.pdf' exists.")
                    return None
                shutil.move(file_path, new_name)
                print(f"Renamed {file_path} to {new_name}")
                return new_name
            else:
                print(f"No valid pattern '... east' found in {file_path}")
                self.status_bar.config(text=f"No pattern found in {file_path}")
                return None
        except Exception as e:
            print(f"Error renaming from text in {file_path}: {e}")
            self.status_bar.config(text=f"Error renaming {file_path}: {e}")
            return None

    def add_swiss_code_to_name(self, files_to_process):
        """Add Swiss code (parent directory name) to PDF name."""
        print("Adding Swiss code to name...")
        total_files = len(files_to_process)
        processed_files = 0
        self.progress_bar.config(maximum=total_files)
        self.progress_bar["value"] = 0
        updated_paths = []
        for file_path in files_to_process:
            if not self.is_running:
                self.status_bar.config(text="Adding Swiss code cancelled.")
                break
            new_path = self.perform_add_swiss_code(file_path)
            if new_path and os.path.exists(new_path):
                updated_paths.append(new_path)
            else:
                if os.path.exists(file_path):
                    updated_paths.append(file_path)
            processed_files += 1
            self.progress_bar["value"] = processed_files
            self.status_bar.config(text=f"Processing file {processed_files}/{total_files}...")
            self.root.update_idletasks()
        self.current_files = updated_paths
        print("Finished adding Swiss code.")
        self.status_bar.config(text="Swiss code addition complete.")

    def perform_add_swiss_code(self, file_path):
        """Add Swiss code (parent directory name) to a file name, returns new path or None."""
        try:
            dir_name = os.path.dirname(file_path)
            base_filename = os.path.basename(file_path)
            parent_dir_name = os.path.basename(dir_name)
            
            if not parent_dir_name:
                print(f"Skipping '{base_filename}': Cannot determine parent directory name for Swiss code (file might be in a root directory or directly added).")
                self.status_bar.config(text=f"Skipped '{base_filename}': No parent dir name.")
                return None

            new_filename = f"{parent_dir_name}_{base_filename}"
            new_file_path = os.path.join(dir_name, new_filename)

            if base_filename.startswith(f"{parent_dir_name}_"):
                print(f"Skipping '{base_filename}': Already has Swiss code '{parent_dir_name}'.")
                self.status_bar.config(text=f"Skipped '{base_filename}': Already coded.")
                return file_path

            if os.path.exists(new_file_path):
                print(f"Error: A file with the new name '{new_file_path}' already exists. Skipping.")
                self.status_bar.config(text=f"Error: '{new_filename}' already exists.")
                return None

            os.rename(file_path, new_file_path)
            print(f"Renamed {file_path} to {new_file_path}")
            self.status_bar.config(text=f"Renamed {file_path} to {new_file_path}")
            return new_file_path
        except Exception as e:
            print(f"Error adding Swiss code to {file_path}: {e}")
            self.status_bar.config(text=f"Error adding Swiss code to {file_path}: {e}")
            return None

    def remove_all_metadata(self, files_to_process):
        """Remove metadata from PDFs."""
        print("Removing all metadata from PDFs...")
        total_files = len(files_to_process)
        processed_files = 0
        self.progress_bar.config(maximum=total_files)
        self.progress_bar["value"] = 0
        for file_path in files_to_process:
            if not self.is_running:
                self.status_bar.config(text="Remove metadata cancelled.")
                return
            self.perform_remove_metadata(file_path)
            processed_files += 1
            self.progress_bar["value"] = processed_files
            self.status_bar.config(text=f"Processing file {processed_files}/{total_files}...")
            self.root.update_idletasks()
        print("Finished removing metadata.")
        self.status_bar.config(text="Metadata removal complete.")

    def perform_remove_metadata(self, file_path):
        """Remove metadata from a PDF."""
        try:
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                writer = PdfWriter()
                for page_num in range(len(reader.pages)):
                    writer.add_page(reader.pages[page_num])
                writer.add_metadata({})
                with open(file_path, 'wb') as output_file:
                    writer.write(output_file)
            print(f"Metadata removed from {file_path}")
            self.status_bar.config(text=f"Metadata removed from {file_path}")
        except Exception as e:
            print(f"Error removing metadata from {file_path}: {e}")
            self.status_bar.config(text=f"Error removing metadata from {file_path}: {e}")

    def remove_mcard_from_name(self, files_to_process):
        """Remove 'MCARD' from the filename."""
        print("Removing MCARD from file names...")
        total_files = len(files_to_process)
        processed_files = 0
        self.progress_bar.config(maximum=total_files)
        self.progress_bar["value"] = 0
        updated_paths = []
        for file_path in files_to_process:
            if not self.is_running:
                self.status_bar.config(text="Remove MCARD operation cancelled.")
                break
            new_path = self.perform_remove_mcard(file_path)
            if new_path and os.path.exists(new_path):
                updated_paths.append(new_path)
            else:
                if os.path.exists(file_path):
                    updated_paths.append(file_path)
            processed_files += 1
            self.progress_bar["value"] = processed_files
            self.status_bar.config(text=f"Processing file {processed_files}/{total_files}...")
            self.root.update_idletasks()
        self.current_files = updated_paths
        print("Finished removing MCARD from names.")
        self.status_bar.config(text="MCARD removal complete.")

    def perform_remove_mcard(self, file_path):
        """Removes 'MCARD' (case-insensitive) from the filename, returns new path or None."""
        try:
            dir_name = os.path.dirname(file_path)
            base_filename = os.path.basename(file_path)
            name_without_ext, file_ext = os.path.splitext(base_filename)
            new_name_without_mcard = re.sub(r'MCARD', '', name_without_ext, flags=re.IGNORECASE)
            new_name_without_mcard = new_name_without_mcard.strip(' _-')

            if not new_name_without_mcard or new_name_without_mcard == name_without_ext:
                print(f"Skipping '{base_filename}': No 'MCARD' found or new name would be empty/unchanged.")
                self.status_bar.config(text=f"Skipped '{base_filename}': No MCARD or empty name.")
                return None

            new_filename = new_name_without_mcard + file_ext
            new_file_path = os.path.join(dir_name, new_filename)

            if os.path.exists(new_file_path) and os.path.abspath(file_path) != os.path.abspath(new_file_path):
                print(f"Error: A file with the new name '{new_file_path}' already exists. Skipping.")
                self.status_bar.config(text=f"Error: '{new_filename}' already exists.")
                return None

            os.rename(file_path, new_file_path)
            print(f"Renamed {file_path} to {new_file_path}")
            self.status_bar.config(text=f"Renamed {file_path} to {new_file_path}")
            return new_file_path
        except Exception as e:
            print(f"Error removing 'MCARD' from {file_path}: {e}")
            self.status_bar.config(text=f"Error removing 'MCARD' from {file_path}: {e}")
            return None
    
    def create_folder_for_each_pdf(self, files_to_process):
        """Creates a new folder for each PDF and moves the PDF into it."""
        print("Creating folders for each PDF...")
        total_files = len(files_to_process)
        processed_files = 0
        self.progress_bar.config(maximum=total_files)
        self.progress_bar["value"] = 0
        updated_paths = []
        for file_path in files_to_process:
            if not self.is_running:
                self.status_bar.config(text="Create folder operation cancelled.")
                break
            new_path = self.perform_create_folder_for_each_pdf(file_path)
            if new_path and os.path.exists(new_path):
                updated_paths.append(new_path)
            else:
                if os.path.exists(file_path):
                    updated_paths.append(file_path)
            processed_files += 1
            self.progress_bar["value"] = processed_files
            self.status_bar.config(text=f"Processing file {processed_files}/{total_files}...")
            self.root.update_idletasks()
        self.current_files = updated_paths
        print("Finished creating folders for PDFs.")
        self.status_bar.config(text="Folder creation complete.")

    def perform_create_folder_for_each_pdf(self, file_path):
        """Creates a new folder for the PDF and moves the PDF into it, returns new path or None."""
        try:
            dir_name = os.path.dirname(file_path)
            base_filename_with_ext = os.path.basename(file_path)
            base_filename_without_ext = os.path.splitext(base_filename_with_ext)[0]
            new_folder_path = os.path.join(dir_name, base_filename_without_ext)
            
            if os.path.exists(new_folder_path):
                print(f"Skipping '{base_filename_with_ext}': Folder '{new_folder_path}' already exists.")
                self.status_bar.config(text=f"Skipped '{base_filename_with_ext}': Folder exists.")
                return None

            os.makedirs(new_folder_path)
            new_file_path = os.path.join(new_folder_path, base_filename_with_ext)
            shutil.move(file_path, new_file_path)
            
            print(f"Moved '{file_path}' to '{new_file_path}' inside new folder.")
            self.status_bar.config(text=f"Moved '{base_filename_with_ext}' to its new folder.")
            return new_file_path
        except Exception as e:
            print(f"Error creating folder and moving PDF for {file_path}: {e}")
            self.status_bar.config(text=f"Error creating folder for {file_path}: {e}")
            return None

    def rotate_pdf(self, files_to_process, rotation_angle):
        """Rotates PDFs by the specified angle."""
        print(f"Rotating PDFs by {rotation_angle} degrees...")
        total_files = len(files_to_process)
        processed_files = 0
        self.progress_bar.config(maximum=total_files)
        self.progress_bar["value"] = 0
        for file_path in files_to_process:
            if not self.is_running:
                self.status_bar.config(text="Rotate PDF cancelled.")
                return
            self.perform_rotation(file_path, rotation_angle)
            processed_files += 1
            self.progress_bar["value"] = processed_files
            self.status_bar.config(text=f"Rotating file {processed_files}/{total_files}...")
            self.root.update_idletasks()
        print("Finished rotating PDFs.")
        self.status_bar.config(text="PDF rotation complete.")

    def perform_rotation(self, file_path, rotation_angle):
        """Rotates a single PDF by the given angle."""
        try:
            with open(file_path, 'rb') as input_file:
                reader = PdfReader(input_file)
                writer = PdfWriter()
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    page.rotate(rotation_angle)
                    writer.add_page(page)
                with open(file_path, 'wb') as output_file:
                    writer.write(output_file)
            print(f"Successfully rotated {file_path} by {rotation_angle} degrees.")
            self.status_bar.config(text=f"Rotated {file_path} by {rotation_angle} degrees.")
        except Exception as e:
            print(f"Error rotating {file_path}: {e}")
            self.status_bar.config(text=f"Error rotating {file_path}: {e}")

    # NEW: Method to remove the first page of PDFs
    def remove_first_page_of_pdfs(self, files_to_process):
        """Removes the first page from each selected PDF."""
        print("Removing first page from PDFs...")
        total_files = len(files_to_process)
        processed_files = 0
        self.progress_bar.config(maximum=total_files)
        self.progress_bar["value"] = 0

        for file_path in files_to_process:
            if not self.is_running:
                self.status_bar.config(text="Remove First Page cancelled.")
                return

            try:
                with open(file_path, 'rb') as infile:
                    reader = PdfReader(infile)
                    writer = PdfWriter()

                    if len(reader.pages) <= 1:
                        print(f"Skipping '{file_path}': PDF has only one page or fewer, cannot remove first page.")
                        self.status_bar.config(text=f"Skipped '{file_path}': One page or less.")
                        continue # Skip to the next file

                    # Add all pages except the first one
                    for page_num in range(1, len(reader.pages)):
                        writer.add_page(reader.pages[page_num])

                    # Overwrite the original file with the modified content
                    with open(file_path, 'wb') as outfile:
                        writer.write(outfile)
                    
                    print(f"Successfully removed first page from {file_path}")
                    self.status_bar.config(text=f"Removed first page from {file_path}")

            except Exception as e:
                print(f"Error removing first page from {file_path}: {e}")
                self.status_bar.config(text=f"Error removing first page from {file_path}: {e}")
            finally:
                processed_files += 1
                self.progress_bar["value"] = processed_files
                self.root.update_idletasks() # Update GUI for each file

        print("Finished removing first page from PDFs.")
        self.status_bar.config(text="Remove First Page complete.")


if __name__ == "__main__":
    import sys
    import os
    import configparser

    if getattr(sys, 'frozen', False):
        # PyInstaller EXE: read from the bundled path
        application_path = sys._MEIPASS
    else:
        # Normal Python script: use script directory
        application_path = os.path.dirname(os.path.abspath(__file__))

        # Create metadata.ini only during development/testing
        ini_path = os.path.join(application_path, 'metadata.ini')
        if not os.path.exists(ini_path):
            config = configparser.ConfigParser()
            config['Default'] = {
                'Title': '',
                'Author': 'Default Author',
                'Subject': 'Default Subject',
                'Keywords': 'default, test'
            }
            config['ProjectA'] = {
                'Title': 'Project A Document',
                'Author': 'Team A',
                'Subject': 'Project Alpha',
                'Keywords': 'projecta, alpha, engineering'
            }
            with open(ini_path, 'w') as configfile:
                config.write(configfile)
            print("Created a dummy 'metadata.ini' for testing purposes.")

    # This path is used for reading the config
    ini_path = os.path.join(application_path, 'metadata.ini')

    root = tk.Tk()
    app = PDFCreateGUI(root)
    root.mainloop()
