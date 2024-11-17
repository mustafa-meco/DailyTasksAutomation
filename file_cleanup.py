import os
import time

# Asynchronous file cleanup function
async def clean_up(folder_path, days_old, log_text):
    try:
        now = time.time()
        cutoff_time = now - (days_old * 86400)
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path) and os.path.getmtime(file_path) < cutoff_time:
                os.remove(file_path)
                log_text.insert("end", f"Deleted {filename}\n")
        log_text.insert("end", "Cleanup completed!\n")
    except Exception as e:
        log_text.insert("end", f"Error during cleanup: {e}\n")