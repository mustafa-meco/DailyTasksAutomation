import os
from tkinter import  messagebox

# Function to rename files in bulk
def bulk_rename(folder_path, old_name_part, new_name_part, progress_bar, root):
    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", "The specified folder path does not exist.")
        return

    try:
        renamed_count = 0
        files = os.listdir(folder_path)
        total_files = len(files)
        
        if total_files == 0:
            messagebox.showinfo("Info", "The folder is empty.")
            return

        progress = 0
        progress_bar['maximum'] = total_files

        for filename in files:
            if old_name_part in filename:
                new_filename = filename.replace(old_name_part, new_name_part)
                os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
                renamed_count += 1
            progress += 1
            progress_bar['value'] = progress
            root.update_idletasks()

        if renamed_count == 0:
            messagebox.showinfo("Info", "No files matched the specified old name part.")
        else:
            messagebox.showinfo("Success", f"Renamed {renamed_count} files successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))
