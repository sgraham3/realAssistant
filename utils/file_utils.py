# utils/file_utils.py
import os
import shutil

def safe_rename(src, dst):
    if os.path.exists(dst):
        return False, f"Destination file '{dst}' already exists."
    try:
        os.rename(src, dst)
        return True, dst
    except Exception as e:
        return False, str(e)

def move_file(src, dst):
    try:
        shutil.move(src, dst)
        return True, dst
    except Exception as e:
        return False, str(e)
