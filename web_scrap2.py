import asyncio
import aiohttp
import tkinter as tk
from bs4 import BeautifulSoup

# Asynchronous function to fetch a single URL
async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return await response.text(), url
    except Exception as e:
        return f"Error fetching {url}: {str(e)}", url

# Asynchronous function to scrape multiple URLs
async def scrape(urls, log_text):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)
        for html, url in results:
            if "Error fetching" in html:
                log_text.insert(tk.END, f"{html}\n")
            else:
                soup = BeautifulSoup(html, 'html.parser')
                title = soup.title.string if soup.title else "No title found"
                log_text.insert(tk.END, f"URL: {url}\nTitle: {title}\n\n")

# Wrapper to run asyncio in a separate thread
def start_scraping2(urls, log_text):
    asyncio.run(scrape(urls, log_text))
