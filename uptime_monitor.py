import requests
import time

# Function to check website status
def check_website(url, log_text, interval, stop_flag):
    while not stop_flag["stop"]:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                log_text.insert("end", f"Website {url} is up! Status code: 200\n")
            else:
                log_text.insert("end", f"Website {url} returned status code {response.status_code}\n")
        except requests.exceptions.RequestException as e:
            log_text.insert("end", f"Error checking website {url}: {e}\n")
        
        log_text.see("end")  # Auto-scroll to the latest log entry
        time.sleep(interval)