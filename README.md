Features of the Script:
File Operations:

Add File(s): Allows adding individual PDFs from the system.

Add Folder: Allows adding all PDFs from a folder (including subdirectories).

Delete Files: Deletes selected files from the list.

Clear Files: Clears the entire file list.

Actions:

Split PDF: Splits each PDF in the list into individual pages.

Merge PDF: Merges multiple PDFs into one.

Rename PDF: Renames a PDF based on user input.

Organize Files: Creates a folder for each PDF and moves it there.

Extract and Rename: Extracts text from the first page of a PDF and uses it to rename the PDF.

Add Swiss Code to Name: Adds a fixed Swiss Code (you can modify it) to the name of each PDF.

Remove All Metadata: Removes metadata from each PDF in the list and overwrites the original files.

Progress and Status:

Progress Bar: Tracks the progress of splitting, merging, and other tasks.

Status Bar: Displays the status of the ongoing action and any errors.

Key Functions:
remove_metadata(): Removes metadata from PDFs, overwriting the original file.

split_pdf(): Splits each PDF into individual pages.

merge_pdf(): Merges multiple PDFs into a single PDF.

rename_pdf(): Renames PDFs based on user input.

organize_files(): Creates a folder for each PDF and moves the PDFs into their respective folders.

extract_and_rename(): Extracts the first few lines of the first page to use as a new name for the PDF.

add_swiss_code_to_name(): Adds a fixed "Swiss Code" to the name of each PDF.

How to Use:
Running the Script: This is a Tkinter GUI script, so it requires Python with the Tkinter library installed. It will pop up a window where you can interact with the buttons and choose actions.

Selecting PDFs and Folders: You can load PDFs into the list by selecting them directly or by choosing a folder that contains PDFs.

Executing Actions: After selecting the PDFs, choose an action from the dropdown menu and click "Execute Action" to apply the chosen operation.

Progress: The progress bar and status bar will help track the progress of the ongoing action.

Additional Notes:
The script uses PyPDF2 for PDF manipulation (splitting, merging, and removing metadata).

File Renaming is done based on user input, with specific functions like extracting text for renaming.

The Swiss Code is hardcoded as "CH12345678", but this can be customized as needed.