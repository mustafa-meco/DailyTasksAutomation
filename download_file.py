import os
import tkinter as tk
import aiohttp
import asyncio
import aiofiles

# Asynchronous function to download a file
async def download_file(url, filename, folder_path):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                file_path = os.path.join(folder_path, filename)
                async with aiofiles.open(file_path, 'wb') as file:
                    await file.write(await response.read())
        return f"Downloaded: {filename}\n"
    except Exception as e:
        return f"Failed to download {filename}: {str(e)}\n"

# Asynchronous function to download all files
async def download_all(urls, folder_path, log_text):
    tasks = [download_file(url, filename, folder_path) for url, filename in urls]
    results = await asyncio.gather(*tasks)
    log_text.insert(tk.END, ''.join(results))
    log_text.insert(tk.END, "All downloads completed!\n")

# Wrapper to run asyncio in a separate thread
def start_download(urls, folder_path, log_text):
    asyncio.run(download_all(urls, folder_path, log_text))