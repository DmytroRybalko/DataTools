import argparse
import asyncio
import os
import requests
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

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


def main():
    """
    Main function to handle command line arguments and initiate file download.
    This function sets up the argument parser, retrieves file names from the logger,
    and starts the download process.
    """
    
    parser = argparse.ArgumentParser(description="Download files from logger device.")
    parser.add_argument('--ip', type=str, required=True, help='Logger IP address, e.g. http://192.168.0.102')
    parser.add_argument('--save_dir', type=str, default='data', help='Directory to save downloaded files')
    args = parser.parse_args()

    print(f"Connecting to logger at {args.ip}...")
    files2download = get_file_names(args.ip, "files2download.txt")

    start_time = time.time()
    download_files_sync(args.ip, files2download, args.save_dir)
    elapsed = time.time() - start_time
    print(f"Total time: {elapsed:.2f} seconds")

    
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Download files from logger device.")
    parser.add_argument('--ip', type=str, required=True, help='Logger IP address, e.g. http://192.168.0.102')
    parser.add_argument('--save_dir', type=str, default='data', help='Directory to save downloaded files')
    args = parser.parse_args()

    print(f"Connecting to logger at {args.ip}...")
    
    # Get file names from the logger
    files2download = get_file_names(args.ip, "files2download.txt")

    # Start the download process
    start_time = time.time()
    download_files_sync(args.ip, files2download, args.save_dir)
    elapsed = time.time() - start_time
    print(f"Total time: {elapsed:.2f} seconds")