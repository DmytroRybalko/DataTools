import asyncio
import os
import requests
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright

def get_file_names(ip_address, files2save):
    """Fetches and prints file names from the logger storage page."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(ip_address)
        page.click('//*[@id="Storage"]')
        
        # Wait for the table to load (adjust selector if needed)
        page.wait_for_selector('//*[@id="contents"]/tbody/tr[1]/td[3]/a')
        
        # Get all <a> elements in the 3rd <td> of each row
        links = page.query_selector_all('//*[@id="contents"]/tbody/tr/td[3]/a')
        list_of_files = [link.inner_text() for link in links]
        browser.close()

        # Save file names to a text file
        print(f"Files from data logger {ip_address} :\n")
        with open(files2save, 'wb') as f:
            for i in list_of_files:
                f.write(i.encode('utf-8') + b'\n')
                print(i)
        
        print(f"\nList of files to download is ready: {files2save}")
        
        input(f"You can open {files2save} in editor and replace files you don't want to download. Press Enter then you're ready...\n")
    
    return files2save
    
# Synchronous file downloader
def download_files_sync(ip_address, files2download, save_dir="data"):
    """Downloads files synchronously from the logger given a list of file names."""
    
    os.makedirs(save_dir, exist_ok=True)
    base_url = f"{ip_address}/cgi-bin/download?"
    # Read file names from the provided file
    # Ensure the file exists before reading
    try:
        with open(files2download, 'r') as f:
            file_names = f.readlines()
            file_names = [name.strip() for name in file_names if name.strip()] # Clean up file names
    except Exception as e:
        print(f"[!] Error: {e}")

    # Download files 
    for name in file_names:
        url = base_url + name
        save_path = os.path.join(save_dir, name + ".zip")
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            with open(save_path, 'wb') as f:
                f.write(resp.content)
            print(f"Downloaded: {save_path}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
    
if __name__ == "__main__":
    
    # Setup
    url_name = "http://192.168.0.102"
    files2download = get_file_names(url_name, "files2download.txt")
    #print(f"List of files to download is ready: {files2download}")
    save_dir = "data"
    
    # Test file names
    #get_file_names(url_name, files2download)

    # Process files
    start_time = time.time()
    download_files_sync(url_name, files2download, save_dir)
    elapsed = time.time() - start_time
    print(f"Total time: {elapsed:.2f} seconds")
    
    
    


# Async file downloader
# import aiohttp
# import aiofiles
# import os

# async def download_file(session, url, save_path):
#     try:
#         async with session.get(url) as resp:
#             resp.raise_for_status()
#             async with aiofiles.open(save_path, 'wb') as f:
#                 async for chunk in resp.content.iter_chunked(1024):
#                     await f.write(chunk)
#         print(f"Downloaded: {save_path}")
#     except Exception as e:
#         print(f"Failed to download {url}: {e}")

# async def download_files(ip_address, file_names, save_dir="data"):
#     """Downloads files asynchronously from the logger given a list of file names."""
#     os.makedirs(save_dir, exist_ok=True)
#     base_url = f"{ip_address}/cgi-bin/download?"
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for name in file_names:
#             url = base_url + name
#             save_path = os.path.join(save_dir, name + ".zip")
#             tasks.append(download_file(session, url, save_path))
#         await asyncio.gather(*tasks)


