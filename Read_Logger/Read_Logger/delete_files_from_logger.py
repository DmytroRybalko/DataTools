import argparse
import os
import requests
import time
from playwright.sync_api import sync_playwright


# Set up dialog handler before clicking the delete button
def handle_dialog(dialog):
    file_name = dialog.message.split(' ')[9].split('\n')[0]
    print(f"Deleting file: {file_name}")
    dialog.accept()

def delete_file(ip_address):
    """Delete all files from the logger storage ."""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(ip_address)
        page.click('//*[@id="Storage"]')
        
        # Wait for the table to load (adjust selector if needed)
        page.wait_for_selector('//*[@id="contents"]/tbody/tr[2]/td[5]/a')

        # Get total number of files
        links = page.query_selector_all('//*[@id="contents"]/tbody/tr/td[5]/a')
        counter = len(links)
        if counter > 0:
            print(f"There is {counter} files in data logger {ip_address}\n")
        else:
            print("No files to delete")
            return
        
        input(f"It will be deleted {counter} files. Please, be shure your've copied files before!!! Press Enter to delete or Ctrl+c to exit\n")
        # Accept dialog window to delete file
        page.on("dialog", handle_dialog)

        # Number of files to delete, adjust as needed    
        #stop_number = counter - 5  # For Test only: number of files to delete, starting from the second one in the list
        stop_number = 1  # standard, leave one file
        
        try:
            while counter > stop_number:
                page.click(f'//*[@id="contents"]/tbody/tr[2]/td[5]/a')
                time.sleep(0.5)  # Wait a bit for the deletion to process
                counter -= 1
            print(f"All files have been deleted!")
        except Exception as e:
            print(f"[!] Error during deletion: {e}")
        
        browser.close()

def main():
    """
    Main function to handle command line arguments and initiate files to delete.
    This function sets up the argument parser, retrieves file names from the logger,
    and starts the deletion process.
    """

    parser = argparse.ArgumentParser(description="Delete files from logger device.")
    parser.add_argument('--ip', type=str, required=True, help='Logger IP address, e.g. http://192.168.0.102')
    args = parser.parse_args()

    print(f"Connecting to logger at {args.ip}...")
    
    delete_file(args.ip)

if __name__ == "__main__":
    # Setup
    #url_name = "http://192.168.1.147"
        
    parser = argparse.ArgumentParser(description="Delete files from logger device.")
    parser.add_argument('--ip', type=str, required=True, help='Logger IP address, e.g. http://192.168.0.102')
    args = parser.parse_args()

    print(f"Connecting to logger at {args.ip}...\n")
    
    delete_file(args.ip)
    