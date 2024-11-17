import schedule
import time
import threading
from tkinter import messagebox

# Function to run the schedule in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start the scheduler thread
def start_scheduler():
    threading.Thread(target=run_scheduler, daemon=True).start()


# Function to handle adding a task to the scheduler
def add_task_to_scheduler(task_function, schedule_time):
    try:
        schedule.every().day.at(schedule_time).do(task_function)
        messagebox.showinfo("Success", f"Task scheduled at {schedule_time}!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to schedule task: {e}")