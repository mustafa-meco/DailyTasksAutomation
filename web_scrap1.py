import asyncio
import aiohttp
from bs4 import BeautifulSoup

# Asynchronous function to fetch content from a URL
async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        return f"Error fetching {url}: {e}"

# Asynchronous function to scrape data from multiple URLs
async def scrape_urls(urls, log_text):
    try:
        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, url) for url in urls]
            html_pages = await asyncio.gather(*tasks)

            for i, html in enumerate(html_pages):
                if "Error" in html:
                    log_text.insert("end", html + "\n")
                else:
                    soup = BeautifulSoup(html, 'html.parser')
                    title = soup.title.string if soup.title else "No Title Found"
                    log_text.insert("end", f"URL {i + 1}: {title}\n")
    except Exception as e:
        log_text.insert("end", f"Error scraping: {e}\n")
    log_text.insert("end", "Scraping completed!\n")

# Wrapper to run asyncio in a separate thread
def start_scraping1(urls, log_text):
    asyncio.run(scrape_urls(urls, log_text))