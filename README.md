Certainly\\! Here's comprehensive documentation for your `realAssistant.py` script, covering its purpose, features, installation, usage, and development details.



-----



\# realAssistant - PDF Utility Application



\## Table of Contents



1\.  \[Introduction](https://www.google.com/search?q=%231-introduction)

2\.  \[Features](https://www.google.com/search?q=%232-features)

3\.  \[Installation](https://www.google.com/search?q=%233-installation)

&nbsp;     \* \[Prerequisites](https://www.google.com/search?q=%23prerequisites)

&nbsp;     \* \[Setup](https://www.google.com/search?q=%23setup)

&nbsp;     \* \[Metadata Configuration (`metadata.ini`)](https://www.google.com/search?q=%23metadata-configuration-metadataini)

4\.  \[Usage](https://www.google.com/search?q=%234-usage)

&nbsp;     \* \[Adding Files/Folders](https://www.google.com/search?q=%23adding-filesfolders)

&nbsp;     \* \[Deleting/Clearing Files](https://www.google.com/search?q=%23deletingclearing-files)

&nbsp;     \* \[Selecting an Action](https://www.google.com/search?q=%23selecting-an-action)

&nbsp;     \* \[Executing an Action](https://www.google.com/search?q=%23executing-an-action)

&nbsp;     \* \[Cancelling an Action](https://www.google.com/search?q=%23cancelling-an-action)

&nbsp;     \* \[Status Bar and Progress](https://www.google.com/search?q=%23status-bar-and-progress)

5\.  \[PDF Processing Actions](https://www.google.com/search?q=%235-pdf-processing-actions)

&nbsp;     \* \[Remove MCARD From Name](https://www.google.com/search?q=%23remove-mcard-from-name)

&nbsp;     \* \[Create Folder For Each PDF](https://www.google.com/search?q=%23create-folder-for-each-pdf)

&nbsp;     \* \[Split PDF](https://www.google.com/search?q=%23split-pdf)

&nbsp;     \* \[Extract and Rename](https://www.google.com/search?q=%23extract-and-rename)

&nbsp;     \* \[Add Swiss Code To Name](https://www.google.com/search?q=%23add-swiss-code-to-name)

&nbsp;     \* \[Remove All Metadata](https://www.google.com/search?q=%23remove-all-metadata)

&nbsp;     \* \[Write Metadata](https://www.google.com/search?q=%23write-metadata)

&nbsp;     \* \[Merge PDF](https://www.google.com/search?q=%23merge-pdf)

&nbsp;     \* \[Rename PDF](https://www.google.com/search?q=%23rename-pdf)

&nbsp;     \* \[Rotate PDF](https://www.google.com/search?q=%23rotate-pdf)

&nbsp;     \* \[Remove First Page](https://www.google.com/search?q=%23remove-first-page)

6\.  \[Building an Executable](https://www.google.com/search?q=%236-building-an-executable)

&nbsp;     \* \[PyInstaller Installation](https://www.google.com/search?q=%23pyinstaller-installation)

&nbsp;     \* \[Building the `.exe`](https://www.google.com/search?q=%23building-the-exe)

&nbsp;     \* \[Including `metadata.ini`](https://www.google.com/search?q=%23including-metadataini)

&nbsp;     \* \[Changing the Executable Icon](https://www.google.com/search?q=%23changing-the-executable-icon)

&nbsp;     \* \[Troubleshooting Builds](https://www.google.com/search?q=%23troubleshooting-builds)

7\.  \[Code Structure](https://www.google.com/search?q=%237-code-structure)

&nbsp;     \* \[`get\_resource\_path` Function](https://www.google.com/search?q=%23get\_resource-path-function)

&nbsp;     \* \[`PDFCreateGUI` Class](https://www.google.com/search?q=%23pdfcreategui-class)

8\.  \[Troubleshooting Common Issues](https://www.google.com/search?q=%238-troubleshooting-common-issues)

9\.  \[Future Enhancements](https://www.google.com/search?q=%239-future-enhancements)

10\. \[License](https://www.google.com/search?q=%2310-license)



-----



\## 1\\. Introduction



`realAssistant` is a Python-based desktop application built with Tkinter, designed to provide a user-friendly interface for performing various operations on PDF documents. It simplifies common PDF manipulation tasks such as renaming, splitting, merging, and managing metadata, making it a valuable tool for anyone frequently working with PDF files.



\## 2\\. Features



&nbsp; \* \*\*File Management:\*\* Add individual PDF files or entire folders of PDFs to a processing list.

&nbsp; \* \*\*List Manipulation:\*\* Delete selected files or clear the entire list.

&nbsp; \* \*\*Multiple PDF Actions:\*\*

&nbsp;     \* Remove "MCARD" from filenames.

&nbsp;     \* Create separate folders for each PDF and move them.

&nbsp;     \* Split multi-page PDFs into individual page files.

&nbsp;     \* Extract and rename (placeholder for content-based renaming).

&nbsp;     \* Add a "SWISSCODE" prefix to filenames.

&nbsp;     \* Remove all existing metadata from PDFs.

&nbsp;     \* Write custom metadata (Title, Author, Subject, Keywords) using configurable profiles.

&nbsp;     \* Merge multiple PDFs into a single document.

&nbsp;     \* Rename individual PDF files via a prompt.

&nbsp;     \* Rotate PDF pages by 90, 180, or 270 degrees.

&nbsp;     \* Remove the first page from PDFs.

&nbsp; \* \*\*Configurable Metadata:\*\* Load and apply custom metadata profiles from an external `metadata.ini` file.

&nbsp; \* \*\*Background Processing:\*\* Executes PDF operations in a separate thread to keep the GUI responsive.

&nbsp; \* \*\*Progress Tracking:\*\* Displays current status and a progress bar for ongoing tasks.

&nbsp; \* \*\*Cancellation:\*\* Allows users to cancel ongoing operations.



\## 3\\. Installation



\### Prerequisites



&nbsp; \* Python 3.7+

&nbsp; \* `pip` (Python package installer)



\### Setup



1\.  \*\*Download the script:\*\* Save the provided `realAssistant.py` script to your desired location.

2\.  \*\*Install required Python libraries:\*\*

&nbsp;   Open your terminal or command prompt and run:

&nbsp;   ```bash

&nbsp;   pip install PyPDF2 reportlab

&nbsp;   ```

&nbsp;     \* `PyPDF2`: Used for most PDF manipulation tasks.

&nbsp;     \* `reportlab`: Used for creating PDFs (currently not actively used for output, but imported).



\### Metadata Configuration (`metadata.ini`)



The application uses an INI file named `metadata.ini` to store predefined metadata profiles. This allows you to quickly apply common sets of metadata to your PDFs.



1\.  \*\*Create the `metadata.ini` file:\*\* In the \*\*same directory\*\* as your `realAssistant.py` script, create a file named `metadata.ini`.



2\.  \*\*Add metadata profiles:\*\* Populate the `metadata.ini` file with sections, where each section represents a metadata profile. Each key-value pair within a section corresponds to a metadata field.



&nbsp;   \*\*Example `metadata.ini` content:\*\*



&nbsp;   ```ini

&nbsp;   \[Default]

&nbsp;   Title = Default Document Title

&nbsp;   Author = Your Name

&nbsp;   Subject = General Document

&nbsp;   Keywords = default, pdf, utility



&nbsp;   \[Project Report]

&nbsp;   Title = Annual Project Report

&nbsp;   Author = John Doe

&nbsp;   Subject = 2025 Project Overview

&nbsp;   Keywords = project, report, annual, confidential



&nbsp;   \[Invoice]

&nbsp;   Title = Customer Invoice

&nbsp;   Author = Billing Department

&nbsp;   Subject = Payment Details

&nbsp;   Keywords = invoice, payment, bill

&nbsp;   ```



&nbsp;     \* Each `\[Section Name]` will appear as an option in the "Select Metadata Profile" dropdown.

&nbsp;     \* Keys (e.g., `Title`, `Author`, `Subject`, `Keywords`) are case-insensitive when read by `configparser` but are typically capitalized when written to PDF by `PyPDF2`.



\## 4\\. Usage



To run the application, open your terminal or command prompt, navigate to the directory where you saved `realAssistant.py`, and run:



```bash

python realAssistant.py

```



\### Adding Files/Folders



&nbsp; \* \*\*Add File(s):\*\* Click this button to open a file dialog and select one or more PDF files.

&nbsp; \* \*\*Add Folder:\*\* Click this button to select a folder. All `.pdf` files within that folder will be added to the list.

&nbsp; \* Files will appear in the listbox. Duplicate files are prevented.



\### Deleting/Clearing Files



&nbsp; \* \*\*Delete:\*\* Select one or more files in the listbox (Ctrl+Click or Shift+Click for multiple selections) and click "Delete" to remove them from the list.

&nbsp; \* \*\*Clear:\*\* Click "Clear" to remove all files from the list. A confirmation dialog will appear.



\### Selecting an Action



&nbsp; \* Use the "Choose Action:" dropdown (Combobox) to select the desired PDF operation.

&nbsp; \* Some actions will reveal additional options:

&nbsp;     \* "Write Metadata": Reveals a "Select Metadata Profile" dropdown, populated from your `metadata.ini`.

&nbsp;     \* "Rotate PDF": Reveals a "Rotation Angle" dropdown (90, 180, 270 degrees).



\### Executing an Action



1\.  Ensure you have files in the listbox.

2\.  Select the desired action from the dropdown.

3\.  Click the "Execute Action" button.

4\.  You will be prompted to select an \*\*output folder\*\* where the processed PDFs will be saved.

5\.  The application will start processing files in a background thread, updating the status bar and progress bar.



\### Cancelling an Action



&nbsp; \* Once an action starts, the "Execute Action" button becomes disabled, and the "Cancel" button becomes enabled.

&nbsp; \* Click "Cancel" to stop the ongoing process. The application will attempt to stop gracefully after completing the current file, or as soon as possible for long operations.



\### Status Bar and Progress



&nbsp; \* The status bar at the bottom will display messages about the current operation (e.g., "Ready", "Processing...", "Action completed\\!").

&nbsp; \* The progress bar will show the overall progress of the batch processing.



\## 5\\. PDF Processing Actions



Here's a detailed description of each available action:



\### Remove MCARD From Name



&nbsp; \* \*\*Description:\*\* Removes the string " MCARD" (with leading space) or "MCARD " (with trailing space) from the filename of the PDF.

&nbsp; \* \*\*Example:\*\* `document MCARD.pdf` becomes `document.pdf`; `MCARD report.pdf` becomes `report.pdf`.



\### Create Folder For Each PDF



&nbsp; \* \*\*Description:\*\* For each selected PDF, a new folder is created in the output directory with the same name as the PDF (without the `.pdf` extension). The original PDF is then copied into this new folder.

&nbsp; \* \*\*Example:\*\* `report.pdf` results in `output\_dir/report/report.pdf`.



\### Split PDF



&nbsp; \* \*\*Description:\*\* Splits a multi-page PDF into individual PDF files, each containing a single page.

&nbsp; \* \*\*Output Naming:\*\* `original\_name\_pageX.pdf` (e.g., `document\_page1.pdf`, `document\_page2.pdf`).



\### Extract and Rename



&nbsp; \* \*\*Description:\*\* Currently a placeholder. In a full implementation, this action would involve extracting specific information from the PDF content (e.g., an invoice number, client name) and using that information to rename the file.

&nbsp; \* \*\*Current Behavior:\*\* Simply copies the file and prepends "Extracted\\\_" to the filename.



\### Add Swiss Code To Name



&nbsp; \* \*\*Description:\*\* Prepends "SWISSCODE\\\_" to the filename of the PDF.

&nbsp; \* \*\*Example:\*\* `invoice.pdf` becomes `SWISSCODE\_invoice.pdf`.



\### Remove All Metadata



&nbsp; \* \*\*Description:\*\* Clears all standard metadata fields (Title, Author, Subject, Keywords) from the selected PDF. The content of the PDF remains unchanged.



\### Write Metadata



&nbsp; \* \*\*Description:\*\* Allows you to apply predefined metadata (Title, Author, Subject, Keywords) to a PDF using a profile selected from `metadata.ini`.

&nbsp; \* \*\*Requirement:\*\* Requires a `metadata.ini` file with defined profiles.



\### Merge PDF



&nbsp; \* \*\*Description:\*\* Merges all currently selected PDF files in the listbox into a single new PDF document.

&nbsp; \* \*\*Output Naming:\*\* `merged\_document.pdf`.

&nbsp; \* \*\*Important:\*\* This action processes all selected files as a group. If you select multiple files and choose "Merge PDF", it will only perform the merge once using \*all\* the files you added to the list.



\### Rename PDF



&nbsp; \* \*\*Description:\*\* Opens a small dialog box prompting you to enter a new filename for the selected PDF.

&nbsp; \* \*\*Behavior:\*\* If you add the extension, it will use it; otherwise, it ensures the `.pdf` extension is added.



\### Rotate PDF



&nbsp; \* \*\*Description:\*\* Rotates all pages of the selected PDF by a specified angle (90, 180, or 270 degrees clockwise).

&nbsp; \* \*\*Output Naming:\*\* `rotated\_original\_name.pdf`.



\### Remove First Page



&nbsp; \* \*\*Description:\*\* Creates a new PDF that contains all pages of the original PDF \*except\* the first page.

&nbsp; \* \*\*Output Naming:\*\* `no\_first\_page\_original\_name.pdf`.

&nbsp; \* \*\*Caution:\*\* If a PDF has only one page, a warning will be issued, and no action will be performed for that file.



\## 6\\. Building an Executable



You can package your `realAssistant` application into a standalone executable (`.exe` for Windows) using `PyInstaller`. This allows users to run your application without needing to install Python or any libraries.



\### PyInstaller Installation



```bash

pip install pyinstaller

```



\### Building the `.exe`



\*\*Preferred Method (One-Folder Distribution with Editable INI):\*\*



This method creates a `dist` folder containing your `.exe` and the `metadata.ini` file alongside it, making `metadata.ini` easily editable by the user.



1\.  Open your terminal in the directory containing `realAssistant.py` and `metadata.ini`.

2\.  Run the command:

&nbsp;   ```bash

&nbsp;   pyinstaller --name "realAssistant" --windowed --add-data "metadata.ini;." --icon "app\_icon.ico" realAssistant.py

&nbsp;   ```

&nbsp;     \* `--name "realAssistant"`: Sets the name of the executable and the output folder.

&nbsp;     \* `--windowed`: Prevents a console window from appearing with the GUI.

&nbsp;     \* `--add-data "metadata.ini;."`: Tells PyInstaller to copy `metadata.ini` to the \*root of the output bundle\*.

&nbsp;     \* `--icon "app\_icon.ico"`: Specifies the icon file for the executable (replace `app\_icon.ico` with your `.ico` file path).

&nbsp;     \* `realAssistant.py`: Your main script.



\*\*Alternative Method (Single Executable with Manual INI Copy):\*\*



If a single `.exe` file is absolutely required, you'll need to manually copy `metadata.ini` to the `dist` folder \*after\* the build process.



1\.  Build the `.exe` \*without\* embedding `metadata.ini`:

&nbsp;   ```bash

&nbsp;   pyinstaller --name "realAssistant" --onefile --windowed --icon "app\_icon.ico" realAssistant.py

&nbsp;   ```

2\.  \*\*After the build completes\*\*, navigate to your project's root directory and manually copy `metadata.ini` to the `dist` folder:

&nbsp;     \* \*\*Windows:\*\* `copy metadata.ini dist\\`

&nbsp;     \* \*\*macOS/Linux:\*\* `cp metadata.ini dist/`



\### Including `metadata.ini`



The `--add-data` flag (`--add-data <source\_path>;<destination\_in\_bundle>`) is crucial for including external files.



&nbsp; \* \\\*\\\*`metadata.ini;.`: \\\*\\\* This tells PyInstaller to take `metadata.ini` from your source directory and place it in the \*root directory\* of the bundled application.



\### Changing the Executable Icon



To change the icon of the generated `.exe`:



1\.  \*\*Prepare an `.ico` file:\*\* Create or obtain an icon file in `.ico` format (e.g., `app\_icon.ico`). For best results on Windows, this `.ico` should contain multiple resolutions.

2\.  \*\*Place the icon file:\*\* Put `app\_icon.ico` in the same directory as your `realAssistant.py` script.

3\.  \*\*Use `--icon` flag:\*\* Include `--icon "app\_icon.ico"` in your PyInstaller command (as shown in the build commands above).



\### Troubleshooting Builds



&nbsp; \* \*\*`\_tkinter.TclError: Index 0 out of range`:\*\* Ensure your `metadata.ini` file exists and contains at least one section (e.g., `\[Default]`). Also, ensure the `action\_options` list is not empty.

&nbsp; \* \*\*"File not found" errors for `metadata.ini` after building:\*\*

&nbsp;     \* Verify `metadata.ini` is in the correct location during the build.

&nbsp;     \* Double-check the `--add-data` syntax.

&nbsp;     \* Ensure the `get\_resource\_path` function is correctly implemented at the top of your script and handles both development and bundled environments.

&nbsp;     \* If using `--onefile` and the manual copy method, ensure you \*actually\* copied the `metadata.ini` to the `dist` folder after building.

&nbsp; \* \*\*Antivirus flags the `.exe`:\*\* This can sometimes happen with PyInstaller-generated executables as they are new and unfamiliar to antivirus software. It's usually a false positive.

&nbsp; \* \*\*Icon not showing/updating:\*\* Windows sometimes caches icons. Try refreshing the folder, moving the `.exe` to a new location, or restarting your computer.



\## 7\\. Code Structure



\### `get\_resource\_path` Function



```python

def get\_resource\_path(relative\_path):

&nbsp;   """Get the absolute path to a resource, checking various locations."""

&nbsp;   if getattr(sys, 'frozen', False):

&nbsp;       # Running in a PyInstaller bundle

&nbsp;       exe\_dir = os.path.dirname(sys.executable)

&nbsp;       potential\_path = os.path.join(exe\_dir, relative\_path)

&nbsp;       if os.path.exists(potential\_path):

&nbsp;           return potential\_path

&nbsp;       # Fallback to \_MEIPASS if it's an embedded file (e.g., in one-file mode before extraction)

&nbsp;       try:

&nbsp;           base\_path = sys.\_MEIPASS

&nbsp;           return os.path.join(base\_path, relative\_path)

&nbsp;       except AttributeError:

&nbsp;           return os.path.join(exe\_dir, relative\_path) # Fallback to exe\_dir if \_MEIPASS not present

&nbsp;   else:

&nbsp;       # Running in a normal Python environment (development)

&nbsp;       return os.path.join(os.path.abspath("."), relative\_path)

```



This helper function is crucial for ensuring that `metadata.ini` (or any other external resource) can be found whether the script is run directly via Python or as a PyInstaller-bundled executable. It checks:



1\.  If the script is frozen (bundled by PyInstaller).

2\.  If so, it first looks for the resource directly next to the executable.

3\.  If not found there, it tries the `\_MEIPASS` temporary directory (where embedded files are extracted in `--onefile` mode).

4\.  If not frozen, it assumes a standard development environment and looks in the current working directory.



\### `PDFCreateGUI` Class



The main application logic is encapsulated within the `PDFCreateGUI` class.



&nbsp; \* \*\*`\_\_init\_\_(self, root)`:\*\* Initializes the Tkinter window, loads metadata, sets up UI elements (listbox, buttons, comboboxes), and initializes internal state variables.

&nbsp; \* \*\*`load\_metadata(self, filename)`:\*\* Reads and parses the `metadata.ini` file using `configparser`. It handles errors if the file is missing or malformed.

&nbsp; \* \*\*`add\_files(self)` / `add\_folder(self)`:\*\* Handlers for adding PDFs to the processing list via file/folder dialogs.

&nbsp; \* \*\*`delete\_file(self)` / `clear\_files(self)`:\*\* Manages removing files from the listbox and `self.current\_files`.

&nbsp; \* \*\*`update\_status(self, message, progress=0)`:\*\* Updates the GUI's status bar and progress bar.

&nbsp; \* \*\*`on\_action\_select(self, event)`:\*\* Dynamically shows/hides UI elements (metadata profile, rotation angle) based on the selected action.

&nbsp; \* \*\*`start\_execute\_thread(self)`:\*\* Initiates the PDF processing in a separate `threading.Thread` to prevent the GUI from freezing. It also manages button states.

&nbsp; \* \*\*`execute\_action(self)`:\*\* The core method where the selected PDF operation is performed. It iterates through `self.current\_files`, calls the appropriate helper function, and updates progress. It includes checks for the `self.is\_running` flag to allow cancellation.

&nbsp; \* \*\*`cancel\_action(self)`:\*\* Sets the `self.is\_running` flag to `False` to signal the background thread to stop.

&nbsp; \* \*\*`reset\_buttons(self)`:\*\* Resets the state of the "Execute" and "Cancel" buttons after an action completes or is cancelled.

&nbsp; \* \*\*`\_remove\_mcard\_from\_name(...)`, `\_create\_folder\_for\_each\_pdf(...)`, etc.:\*\* Private helper methods (prefixed with `\_`) that encapsulate the specific logic for each PDF operation. These methods handle file copying, `PyPDF2` operations, and path manipulations.



\## 8\\. Troubleshooting Common Issues



&nbsp; \* \*\*GUI Freezing:\*\* If the application's GUI becomes unresponsive during PDF processing, ensure `start\_execute\_thread` is correctly implemented to run `execute\_action` in a `threading.Thread`.

&nbsp; \* \*\*PDF Read/Write Errors:\*\* Check if the PDF files are corrupted or password-protected. `PyPDF2` might raise errors in such cases.

&nbsp; \* \*\*Permissions:\*\* Ensure the application has read/write permissions for the input PDF files and the chosen output directory.

&nbsp; \* \*\*Missing Dependencies:\*\* If you get `ModuleNotFoundError`, double-check that all required libraries (`PyPDF2`, `reportlab`, `pyinstaller`) are installed.

&nbsp; \* \*\*`metadata.ini` Issues:\*\* If profiles aren't loading, check the console for error messages from `load\_metadata`. Verify the INI file format and path.



\## 9\\. Future Enhancements



&nbsp; \* \*\*Error Reporting:\*\* More detailed error messages for specific PDF-related failures.

&nbsp; \* \*\*User Feedback:\*\* More dynamic status updates, perhaps showing the current file being processed more prominently.

&nbsp; \* \*\*Advanced Features:\*\*

&nbsp;     \* PDF encryption/decryption.

&nbsp;     \* Adding watermarks (using ReportLab).

&nbsp;     \* PDF compression.

&nbsp;     \* Batch renaming with more complex patterns (regex, CSV input).

&nbsp;     \* Support for other file types (e.g., convert image to PDF).

&nbsp;     \* A "Settings" dialog to manage `metadata.ini` profiles directly within the GUI.

&nbsp; \* \*\*Input Validation:\*\* Check if input files are actually PDFs before attempting to process them.

&nbsp; \* \*\*Logging:\*\* Implement a proper logging system for debugging and tracking operations.



\## 10\\. License



This project is open-source. (Add your chosen license here, e.g., MIT, GPL, etc.)



-----

