from tkinter import filedialog, messagebox
import os
import shutil
import tkinter as tk


# Function to back up files
def backup_files(src_dir, dest_dir):
    try:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        backed_up_count = 0
        for file in os.listdir(src_dir):
            full_file_name = os.path.join(src_dir, file)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, dest_dir)
                backed_up_count += 1
        messagebox.showinfo("Success", f"Backed up {backed_up_count} files to {dest_dir}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

