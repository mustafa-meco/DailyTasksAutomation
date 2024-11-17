import os
import tkinter as tk
from tkinter import  messagebox

    # Function to rename files in bulk
def bulk_rename(folder_path, old_name_part, new_name_part):
    try:
        renamed_count = 0
        for filename in os.listdir(folder_path):
            if old_name_part in filename:
                new_filename = filename.replace(old_name_part, new_name_part)
                os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
                renamed_count += 1
        messagebox.showinfo("Success", f"Renamed {renamed_count} files successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

