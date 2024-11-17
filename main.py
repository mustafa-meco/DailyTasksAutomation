import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Toplevel, Label, Entry, Button, Tk, ttk, scrolledtext, Frame
from threading import Thread
from bulk_rename import bulk_rename
from backup_files import backup_files
from download_file import start_download
from send_email import send_email
from task_scheduler import start_scheduler, add_task_to_scheduler
from web_scrap1 import start_scraping1
from web_scrap2 import start_scraping2
from social_media_post import post_tweet
from invoice_generation import create_invoice
from uptime_monitor import check_website
from auto_reply import auto_reply
from file_cleanup import clean_up
import asyncio
from password_generator import generate_multiple_passwords
from task_tracker import manage_reminders

# Function to handle the renaming task
def open_rename_window():
    def execute_rename():
        folder_path = folder_entry.get()
        old_name_part = old_name_entry.get()
        new_name_part = new_name_entry.get()
        if not folder_path or not old_name_part or not new_name_part:
            messagebox.showwarning("Input Error", "All fields are required!")
        else:
            bulk_rename(folder_path, old_name_part, new_name_part, progress_bar, rename_window)
            status_label.config(text="Renaming completed!")

    def browse_folder():
        folder_selected = filedialog.askdirectory()
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, folder_selected)

    rename_window = tk.Toplevel(root)
    rename_window.title("Bulk Rename Files")
    rename_window.geometry("450x250")

    ttk.Label(rename_window, text="Folder Path:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    folder_entry = ttk.Entry(rename_window, width=40)
    folder_entry.grid(row=0, column=1, padx=10, pady=5)
    ttk.Button(rename_window, text="Browse", command=browse_folder).grid(row=0, column=2, padx=10, pady=5)

    ttk.Label(rename_window, text="Old Name Part:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    old_name_entry = ttk.Entry(rename_window, width=40)
    old_name_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(rename_window, text="New Name Part:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    new_name_entry = ttk.Entry(rename_window, width=40)
    new_name_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Button(rename_window, text="Rename Files", command=execute_rename).grid(row=3, column=1, padx=10, pady=20)
    ttk.Button(rename_window, text="Cancel", command=rename_window.destroy).grid(row=3, column=2, padx=10, pady=20)

    progress_bar = ttk.Progressbar(rename_window, orient="horizontal", length=400, mode="determinate")
    progress_bar.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    status_label = ttk.Label(rename_window, text="")
    status_label.grid(row=5, column=0, columnspan=3, padx=10, pady=5)


# Function to handle the backup task
def open_backup_window():
    def execute_backup():
        src_dir = src_entry.get()
        dest_dir = dest_entry.get()
        if not src_dir or not dest_dir:
            messagebox.showwarning("Input Error", "Both fields are required!")
        else:
            backup_files(src_dir, dest_dir)

    backup_window = tk.Toplevel(root)
    backup_window.title("Backup Files")
    backup_window.geometry("400x300")

    tk.Label(backup_window, text="Source Folder:").pack(pady=5)
    src_entry = tk.Entry(backup_window, width=40)
    src_entry.pack(pady=5)

    def browse_src():
        src_selected = filedialog.askdirectory()
        src_entry.insert(0, src_selected)

    tk.Button(backup_window, text="Browse", command=browse_src).pack(pady=5)

    tk.Label(backup_window, text="Destination Folder:").pack(pady=5)
    dest_entry = tk.Entry(backup_window, width=40)
    dest_entry.pack(pady=5)

    def browse_dest():
        dest_selected = filedialog.askdirectory()
        dest_entry.insert(0, dest_selected)

    tk.Button(backup_window, text="Browse", command=browse_dest).pack(pady=5)

    tk.Button(backup_window, text="Backup Files", command=execute_backup).pack(pady=20)

# Function to handle the download task
def open_download_window():
    def add_url():
        url = url_entry.get()
        filename = filename_entry.get()
        if not url or not filename:
            messagebox.showwarning("Input Error", "Both URL and Filename are required!")
        else:
            urls_list.append((url, filename))
            url_list_box.insert(tk.END, f"{url} -> {filename}")
            url_entry.delete(0, tk.END)
            filename_entry.delete(0, tk.END)

    def execute_download():
        if not urls_list:
            messagebox.showwarning("Input Error", "No URLs added!")
            return
        folder_path = folder_entry.get()
        if not folder_path:
            messagebox.showwarning("Input Error", "Destination folder is required!")
            return
        log_text.delete(1.0, tk.END)
        log_text.insert(tk.END, "Starting downloads...\n")
        # Run downloads in a separate thread to keep GUI responsive
        Thread(target=start_download, args=(urls_list, folder_path, log_text)).start()

    download_window = tk.Toplevel(root)
    download_window.title("Download Files")
    download_window.geometry("500x500")

    urls_list = []

    tk.Label(download_window, text="Add URL and Filename").pack(pady=5)
    url_entry = tk.Entry(download_window, width=50)
    url_entry.pack(pady=5)
    filename_entry = tk.Entry(download_window, width=50)
    filename_entry.pack(pady=5)

    tk.Button(download_window, text="Add URL", command=add_url).pack(pady=5)

    url_list_box = tk.Listbox(download_window, height=10, width=70)
    url_list_box.pack(pady=5)

    tk.Label(download_window, text="Destination Folder:").pack(pady=5)
    folder_entry = tk.Entry(download_window, width=50)
    folder_entry.pack(pady=5)

    def browse_folder():
        folder_selected = filedialog.askdirectory()
        folder_entry.insert(0, folder_selected)

    tk.Button(download_window, text="Browse", command=browse_folder).pack(pady=5)

    tk.Button(download_window, text="Start Download", command=execute_download).pack(pady=5)

    tk.Label(download_window, text="Download Log:").pack(pady=5)
    log_text = scrolledtext.ScrolledText(download_window, height=10, width=70)
    log_text.pack(pady=5)

# Function to open the email automation window
def open_email_window():
    def execute_email():
        subject = subject_entry.get()
        body = body_text.get("1.0", tk.END).strip()
        to_email = recipient_entry.get()

        if not subject or not body or not to_email:
            messagebox.showwarning("Input Error", "All fields are required!")
        else:
            send_email(subject, body, to_email)

    email_window = tk.Toplevel(root)
    email_window.title("Automate Email Reports")
    email_window.geometry("400x400")

    tk.Label(email_window, text="Recipient Email:").pack(pady=5)
    recipient_entry = tk.Entry(email_window, width=50)
    recipient_entry.pack(pady=5)

    tk.Label(email_window, text="Email Subject:").pack(pady=5)
    subject_entry = tk.Entry(email_window, width=50)
    subject_entry.pack(pady=5)

    tk.Label(email_window, text="Email Body:").pack(pady=5)
    body_text = tk.Text(email_window, height=10, width=50)
    body_text.pack(pady=5)

    tk.Button(email_window, text="Send Email", command=execute_email).pack(pady=20)

# Open scheduler window
def open_scheduler_window():
    global task_mapping
    # Map task names to functions
    task_mapping = {
        "Bulk Rename Files": open_rename_window,
        "Backup Files": open_backup_window,
        "Download Files": open_download_window,
        "Automate Email Reports": open_email_window,
        "Task Scheduler": open_scheduler_window,
        "Web Scraping1": open_scraping_window1,
            "Web Scraping2": open_scraping_window2,
            "Automate Social Media Posts": open_social_media_window,
            "Automate Invoice Generation": open_invoice_window,
            "Monitor Website Uptime": open_uptime_monitor_window,
            "Automate Email Replies": open_auto_reply_window,
            "File Cleanup": open_file_cleanup_window,
            "Password Generator": open_password_generator_window
        }
    def schedule_task():
        global task_mapping
        task_name = task_selection.get()
        schedule_time = time_entry.get()
        if not task_name or not schedule_time:
            messagebox.showwarning("Input Error", "All fields are required!")
            return
        
        
        
        
        task_function = task_mapping.get(task_name)
        if task_function:
            add_task_to_scheduler(task_function, schedule_time)
        else:
            messagebox.showerror("Error", "Invalid task selected!")

    scheduler_window = tk.Toplevel(root)
    scheduler_window.title("Task Scheduler")
    scheduler_window.geometry("400x250")

    tk.Label(scheduler_window, text="Select Task to Schedule:").pack(pady=5)
    task_selection = tk.StringVar()
    task_selection.set("Bulk Rename Files")
    tk.OptionMenu(scheduler_window, task_selection, *[task for task in task_mapping.keys()]).pack(pady=5)
    


    tk.Label(scheduler_window, text="Time (HH:MM 24-hour format):").pack(pady=5)
    time_entry = tk.Entry(scheduler_window, width=20)
    time_entry.pack(pady=5)

    tk.Button(scheduler_window, text="Schedule Task", command=schedule_task).pack(pady=20)

# Function to open the scraping window
def open_scraping_window1():
    def add_url():
        url = url_entry.get()
        if url:
            urls.append(url)
            url_list.insert("end", url)
            url_entry.delete(0, "end")
        else:
            messagebox.showwarning("Input Error", "Please enter a URL!")

    def execute_scraping():
        if not urls:
            messagebox.showwarning("Input Error", "No URLs added!")
            return
        log_text.delete(1.0, "end")
        log_text.insert("end", "Starting web scraping...\n")
        # Run scraping in a separate thread to keep GUI responsive
        Thread(target=start_scraping1, args=(urls, log_text), daemon=True).start()

    scraping_window = Toplevel(root)
    scraping_window.title("Web Scraping")
    scraping_window.geometry("500x500")

    urls = []

    Label(scraping_window, text="Enter URL:").pack(pady=5)
    url_entry = Entry(scraping_window, width=50)
    url_entry.pack(pady=5)

    Button(scraping_window, text="Add URL", command=add_url).pack(pady=5)

    Label(scraping_window, text="URL List:").pack(pady=5)
    url_list = scrolledtext.ScrolledText(scraping_window, height=10, width=60)
    url_list.pack(pady=5)

    Button(scraping_window, text="Start Scraping", command=execute_scraping).pack(pady=10)

    Label(scraping_window, text="Scraping Log:").pack(pady=5)
    log_text = scrolledtext.ScrolledText(scraping_window, height=10, width=60)
    log_text.pack(pady=5)

# Function to open the scraping window
def open_scraping_window2():
    def execute_scraping():
        urls = url_text.get("1.0", tk.END).strip().split("\n")
        urls = [url.strip() for url in urls if url.strip()]
        if not urls:
            messagebox.showwarning("Input Error", "Please provide at least one URL!")
            return
        log_text.delete(1.0, tk.END)
        log_text.insert(tk.END, "Starting web scraping...\n")
        # Run scraping in a separate thread to keep GUI responsive
        Thread(target=start_scraping2, args=(urls, log_text)).start()

    scraping_window = tk.Toplevel(root)
    scraping_window.title("Web Scraping")
    scraping_window.geometry("500x500")

    tk.Label(scraping_window, text="Enter URLs (one per line):").pack(pady=5)
    url_text = scrolledtext.ScrolledText(scraping_window, height=10, width=60)
    url_text.pack(pady=5)

    tk.Button(scraping_window, text="Start Scraping", command=execute_scraping).pack(pady=10)

    tk.Label(scraping_window, text="Scraping Results:").pack(pady=5)
    log_text = scrolledtext.ScrolledText(scraping_window, height=15, width=60)
    log_text.pack(pady=5)

# Function to open the social media posting window
def open_social_media_window():
    def execute_tweet():
        message = tweet_text.get("1.0", "end").strip()
        if not message:
            messagebox.showwarning("Input Error", "Tweet content cannot be empty!")
        else:
            post_tweet(message)

    social_media_window = Toplevel(root)
    social_media_window.title("Automate Social Media Posts")
    social_media_window.geometry("400x300")

    Label(social_media_window, text="Enter your tweet:").pack(pady=10)
    tweet_text = scrolledtext.ScrolledText(social_media_window, height=5, width=40)
    tweet_text.pack(pady=10)

    Button(social_media_window, text="Post Tweet", command=execute_tweet).pack(pady=20)

# Function to open the invoice generation window
def open_invoice_window():
    def generate_invoice():
        client_name = client_name_entry.get().strip()
        amount = amount_entry.get().strip()
        
        if not client_name or not amount:
            messagebox.showwarning("Input Error", "All fields are required!")
            return
        
        try:
            amount = float(amount)
            create_invoice(client_name, amount)
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a valid number!")

    invoice_window = Toplevel(root)
    invoice_window.title("Automate Invoice Generation")
    invoice_window.geometry("400x300")

    Label(invoice_window, text="Client Name:").pack(pady=5)
    client_name_entry = Entry(invoice_window, width=30)
    client_name_entry.pack(pady=5)

    Label(invoice_window, text="Amount ($):").pack(pady=5)
    amount_entry = Entry(invoice_window, width=30)
    amount_entry.pack(pady=5)

    Button(invoice_window, text="Generate Invoice", command=generate_invoice).pack(pady=20)

# Function to open the uptime monitoring window
def open_uptime_monitor_window():
    def start_monitoring():
        url = url_entry.get().strip()
        interval = interval_entry.get().strip()

        if not url:
            messagebox.showwarning("Input Error", "Website URL cannot be empty!")
            return
        if not interval.isdigit() or int(interval) <= 0:
            messagebox.showwarning("Input Error", "Interval must be a positive number!")
            return
        
        interval = int(interval)
        stop_flag["stop"] = False
        log_text.delete(1.0, "end")
        log_text.insert("end", f"Starting uptime monitoring for {url} every {interval} seconds...\n")
        Thread(target=check_website, args=(url, log_text, interval, stop_flag), daemon=True).start()

    def stop_monitoring():
        stop_flag["stop"] = True
        log_text.insert("end", "Stopped monitoring.\n")

    uptime_window = Toplevel(root)
    uptime_window.title("Monitor Website Uptime")
    uptime_window.geometry("500x400")

    stop_flag = {"stop": False}  # Shared flag to stop monitoring

    Label(uptime_window, text="Website URL:").pack(pady=5)
    url_entry = Entry(uptime_window, width=50)
    url_entry.pack(pady=5)

    Label(uptime_window, text="Check Interval (seconds):").pack(pady=5)
    interval_entry = Entry(uptime_window, width=10)
    interval_entry.pack(pady=5)

    Button(uptime_window, text="Start Monitoring", command=start_monitoring).pack(pady=10)
    Button(uptime_window, text="Stop Monitoring", command=stop_monitoring).pack(pady=10)

    Label(uptime_window, text="Uptime Log:").pack(pady=5)
    log_text = scrolledtext.ScrolledText(uptime_window, height=15, width=60)
    log_text.pack(pady=5)

# Function to open auto-reply window
def open_auto_reply_window():
    def start_auto_reply():
        email = email_entry.get().strip()
        password = password_entry.get().strip()
        reply_message = reply_message_text.get(1.0, "end").strip()

        if not email or not password or not reply_message:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        stop_flag["stop"] = False
        log_text.delete(1.0, "end")
        log_text.insert("end", "Starting auto-reply service...\n")
        Thread(target=auto_reply, args=(email, password, reply_message, log_text, stop_flag), daemon=True).start()

    def stop_auto_reply():
        stop_flag["stop"] = True
        log_text.insert("end", "Stopped auto-reply service.\n")

    auto_reply_window = Toplevel(root)
    auto_reply_window.title("Auto-Reply to Emails")
    auto_reply_window.geometry("500x500")

    stop_flag = {"stop": False}  # Shared flag to stop the service

    Label(auto_reply_window, text="Email Address:").pack(pady=5)
    email_entry = Entry(auto_reply_window, width=50)
    email_entry.pack(pady=5)

    Label(auto_reply_window, text="Password:").pack(pady=5)
    password_entry = Entry(auto_reply_window, show='*', width=50)
    password_entry.pack(pady=5)

    Label(auto_reply_window, text="Reply Message:").pack(pady=5)
    reply_message_text = scrolledtext.ScrolledText(auto_reply_window, height=5, width=60)
    reply_message_text.pack(pady=5)

    Button(auto_reply_window, text="Start Auto-Reply", command=start_auto_reply).pack(pady=10)
    Button(auto_reply_window, text="Stop Auto-Reply", command=stop_auto_reply).pack(pady=10)

    Label(auto_reply_window, text="Log:").pack(pady=5)
    log_text = scrolledtext.ScrolledText(auto_reply_window, height=15, width=60)
    log_text.pack(pady=5)

# Function to open file cleanup window
def open_file_cleanup_window():
    def start_cleanup():
        folder_path = folder_path_entry.get().strip()
        days_old = days_old_entry.get().strip()

        if not folder_path or not days_old.isdigit():
            messagebox.showwarning("Input Error", "Please specify a valid folder path and number of days!")
            return

        days_old = int(days_old)
        log_text.delete(1.0, "end")
        log_text.insert("end", f"Starting cleanup in {folder_path} for files older than {days_old} days...\n")
        Thread(target=asyncio.run, args=(clean_up(folder_path, days_old, log_text),), daemon=True).start()

    def browse_folder():
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            folder_path_entry.delete(0, "end")
            folder_path_entry.insert(0, folder_selected)

    file_cleanup_window = Toplevel(root)
    file_cleanup_window.title("File Cleanup")
    file_cleanup_window.geometry("500x400")

    Label(file_cleanup_window, text="Folder Path:").pack(pady=5)
    folder_path_entry = Entry(file_cleanup_window, width=50)
    folder_path_entry.pack(pady=5)
    Button(file_cleanup_window, text="Browse", command=browse_folder).pack(pady=5)

    Label(file_cleanup_window, text="Delete files older than (days):").pack(pady=5)
    days_old_entry = Entry(file_cleanup_window, width=20)
    days_old_entry.pack(pady=5)

    Button(file_cleanup_window, text="Start Cleanup", command=start_cleanup).pack(pady=10)

    Label(file_cleanup_window, text="Log:").pack(pady=5)
    log_text = scrolledtext.ScrolledText(file_cleanup_window, height=15, width=60)
    log_text.pack(pady=5)

# Function to open password generation window
def open_password_generator_window():
    def start_password_generation():
        num_passwords = num_passwords_entry.get().strip()
        password_length = password_length_entry.get().strip()

        if not num_passwords.isdigit() or not password_length.isdigit():
            messagebox.showwarning("Input Error", "Please enter valid numbers for length and count!")
            return

        num_passwords = int(num_passwords)
        password_length = int(password_length)
        log_text.delete(1.0, "end")
        log_text.insert("end", f"Generating {num_passwords} passwords of length {password_length}...\n")
        Thread(target=asyncio.run, args=(generate_multiple_passwords(num_passwords, password_length, log_text),), daemon=True).start()

    password_generator_window = Toplevel(root)
    password_generator_window.title("Password Generator")
    password_generator_window.geometry("500x400")

    Label(password_generator_window, text="Number of Passwords:").pack(pady=5)
    num_passwords_entry = Entry(password_generator_window, width=20)
    num_passwords_entry.pack(pady=5)

    Label(password_generator_window, text="Length of Each Password:").pack(pady=5)
    password_length_entry = Entry(password_generator_window, width=20)
    password_length_entry.pack(pady=5)

    Button(password_generator_window, text="Generate Passwords", command=start_password_generation).pack(pady=10)

    Label(password_generator_window, text="Generated Passwords:").pack(pady=5)
    log_text = scrolledtext.ScrolledText(password_generator_window, height=15, width=60)
    log_text.pack(pady=5)

# Function to open the task tracker window
def open_task_tracker_window():
    reminders = []

    def add_reminder():
        task_name = task_name_entry.get().strip()
        interval = interval_entry.get().strip()

        if not task_name:
            messagebox.showwarning("Input Error", "Task name cannot be empty!")
            return
        if not interval.isdigit():
            messagebox.showwarning("Input Error", "Interval must be a number (seconds)!")
            return

        interval = int(interval)
        reminders.append({"name": task_name, "interval": interval})
        log_text.insert("end", f"Added reminder: {task_name} every {interval} seconds.\n")

    def start_reminders():
        log_text.insert("end", "Starting reminders...\n")
        Thread(
            target=asyncio.run,
            args=(manage_reminders(reminders, log_text),),
            daemon=True
        ).start()

    task_tracker_window = Toplevel(root)
    task_tracker_window.title("Task Tracker / Reminder")
    task_tracker_window.geometry("500x400")

    Label(task_tracker_window, text="Task Name:").pack(pady=5)
    task_name_entry = Entry(task_tracker_window, width=30)
    task_name_entry.pack(pady=5)

    Label(task_tracker_window, text="Interval (seconds):").pack(pady=5)
    interval_entry = Entry(task_tracker_window, width=30)
    interval_entry.pack(pady=5)

    Button(task_tracker_window, text="Add Reminder", command=add_reminder).pack(pady=10)
    Button(task_tracker_window, text="Start Reminders", command=start_reminders).pack(pady=10)

    Label(task_tracker_window, text="Logs:").pack(pady=5)
    log_text = scrolledtext.ScrolledText(task_tracker_window, height=15, width=60)
    log_text.pack(pady=5)

# Main GUI
root = tk.Tk()
root.title("Automation Tasks")
root.geometry("400x800")
root.configure(bg="#f0f0f0")

ttk.Label(root, text="Select a Task", font=("Arial", 16, "bold"), background="#f0f0f0").pack(pady=20)

# Create frames for better organization with different background colors
frame1 = ttk.Frame(root, style="Frame1.TFrame")
frame1.pack(pady=10, fill='x')
frame2 = ttk.Frame(root, style="Frame2.TFrame")
frame2.pack(pady=10, fill='x')
frame3 = ttk.Frame(root, style="Frame3.TFrame")
frame3.pack(pady=10, fill='x')

# Define styles
style = ttk.Style()
style.configure("Frame1.TFrame", background="#e0f7fa")
style.configure("Frame2.TFrame", background="#ffe0b2")
style.configure("Frame3.TFrame", background="#dcedc8")
style.configure("TButton", padding=6, relief="flat", background="#ccc")

# Buttons for tasks
ttk.Button(frame1, text="Bulk Rename Files", command=open_rename_window).pack(pady=5)
ttk.Button(frame1, text="Backup Files", command=open_backup_window).pack(pady=5)
ttk.Button(frame1, text="Download Files", command=open_download_window).pack(pady=5)
ttk.Button(frame1, text="Automate Email Reports", command=open_email_window).pack(pady=5)

ttk.Button(frame2, text="Task Scheduler", command=open_scheduler_window).pack(pady=5)
ttk.Button(frame2, text="Web Scraping1", command=open_scraping_window1).pack(pady=5)
ttk.Button(frame2, text="Web Scraping2", command=open_scraping_window2).pack(pady=5)
ttk.Button(frame2, text="Automate Social Media Posts", command=open_social_media_window).pack(pady=5)

ttk.Button(frame3, text="Automate Invoice Generation", command=open_invoice_window).pack(pady=5)
ttk.Button(frame3, text="Monitor Website Uptime", command=open_uptime_monitor_window).pack(pady=5)
ttk.Button(frame3, text="Automate Email Replies", command=open_auto_reply_window).pack(pady=5)
ttk.Button(frame3, text="File Cleanup", command=open_file_cleanup_window).pack(pady=5)
ttk.Button(frame3, text="Password Generator", command=open_password_generator_window).pack(pady=5)
ttk.Button(frame3, text="Task Tracker / Reminder", command=open_task_tracker_window).pack(pady=5)

# Start the scheduler
start_scheduler()

root.mainloop()