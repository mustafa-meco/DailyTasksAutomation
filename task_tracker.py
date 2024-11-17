import asyncio
from datetime import datetime

# Async function to send reminders
async def task_reminder(task_name, interval, log_text):
    while True:
        log_text.insert("end", f"Reminder: {task_name} - {datetime.now()}\n")
        log_text.see("end")  # Auto-scroll to the latest reminder
        await asyncio.sleep(interval)

# Async manager for multiple reminders
async def manage_reminders(reminders, log_text):
    tasks = [
        task_reminder(task["name"], task["interval"], log_text) for task in reminders
    ]
    await asyncio.gather(*tasks)