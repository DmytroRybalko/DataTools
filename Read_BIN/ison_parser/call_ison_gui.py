import logging
import time
from pywinauto.timings import wait_until
from pywinauto.application import Application, ProcessNotFoundError
from pywinauto.keyboard import send_keys
from pywinauto import timings
from tkinter import Tk, filedialog
from ison_parser import global_logger

def call_ison_gui(app_exe, time_sleep=1):
    """
    Launches the ISON GUI application and automates the process of converting log data to a bin file.

    Parameters:
        app_exe (str): Path to the ISON application executable.
        time_sleep (float, optional): Time to sleep between UI actions (seconds). Default is 1.
    """

    # Hide main Tk window
    root = Tk()
    root.withdraw()

    # Start the application
    app = Application(backend="uia").start(app_exe)

    dlg_select_mode = app.window(title=r"Select program type")
    dlg_select_mode.wait('visible', timeout=time_sleep)
    logging.info("Started a new instance of the application.")

    # Try to click the OK button (case-insensitive, anywhere in text)
    ok_button = dlg_select_mode.child_window(title="OK", control_type="Button")
    ok_button.click_input()
    time.sleep(time_sleep)

    # Access the main window again if needed
    main_win = app.top_window()
    logging.info(f"Captured window title: {main_win.window_text()}")
    time.sleep(time_sleep)

    # Print all MenuItem controls in the main window
    # print("Menu items after clicking Convert:")
    # logging.info("Menu items after clicking Convert:")
    # for item in main_win.descendants(control_type="MenuItem"):
    #     print(f"Menu item: {item.window_text()}")
    #     logging.info(f"Menu item: {item.window_text()}")

    # Open the "Convert" menu
    convert_menu = main_win.child_window(title="Convert", control_type="MenuItem")
    #print(f"Captured menu item: {convert_menu.window_text()}")
    #logging.info(f"Captured menu item: {convert_menu.window_text()}")
    convert_menu.click_input()
    time.sleep(time_sleep)  

    # print("Submenu items under Convert:")
    # logging.info("Submenu items under Convert:")
    # for item in convert_menu.descendants():
    #     logging.info(f"Submenu item: {item.window_text()}")

    # Select "Convert data to bin file ..."
    convert_log2bin_item = main_win.child_window(title="Convert log data to bin file...", control_type="MenuItem")
    convert_log2bin_item.click_input()
    time.sleep(time_sleep)  # Wait for dialog to appear

    # Check flash files in the dialog
    listview = main_win.child_window(control_type="List")
    for item in listview.descendants(control_type="ListItem"):
        #print(f"Flash item: {item.window_text()}")
        logging.info(f"Flash item: {item.window_text()}")

    # Select the first .flash file from the list
    flash_file = [item.window_text() for item in listview.descendants(control_type="ListItem") if item.window_text().endswith(".flash")][0]
    file_item = listview.child_window(title=flash_file, control_type="ListItem")
    file_item.click_input()
    time.sleep(time_sleep)

    # Find button to open the file
    Open_file_window = main_win.child_window(title="Open file")
    for element in Open_file_window.descendants(title="Відкрити"):
        #logging.info(f"{element.element_info.control_type}: {element.window_text()}")
        if element.window_text() == "Відкрити":
            open_btn = element
        else:
            logging.error(f"Can't find button 'Відкрити' to open {flash_file}")

    # Click the Open button (if present)
    open_btn = main_win.child_window(title="Відкрити", control_type=open_btn.element_info.control_type)
    if open_btn.is_enabled():
        open_btn.click_input()
        time.sleep(time_sleep)
    else:
        logging.error(f"Can't click on button 'Відкрити' to open {flash_file}")

    # Check log files in the dialog
    list_logs = main_win.child_window(control_type="List")
    # for item in list_logs.descendants(control_type="ListItem"):
    #     logging.info(item.window_text())

    # Choose only one file
    log_file_name = [item.window_text() for item in list_logs.descendants(control_type="ListItem", title="INS")][0]

    # Select a file by its name (replace with your actual file name)
    log_file = list_logs.child_window(title=log_file_name, control_type="ListItem")
    if log_file.exists():
        log_file.click_input()
        time.sleep(time_sleep)
    else:
        logging.error(f"Can't find {log_file_name} to open.")

    # Click the Open button (if present)
    if open_btn.is_enabled():
        open_btn.click_input()
        time.sleep(time_sleep)  # Wait for the operation to complete
    else:
        logging.error(f"Can't click on button 'Open' to open {log_file}")

    # ========================================================================
    # Wait for the Information / Error window about converting log file to bin
    # ========================================================================
    while True:
        if main_win.child_window(title="Information").exists():
            if main_win.child_window(title="Information").is_visible():
                # Capture the Information window
                Information_window = main_win.child_window(title="Information")
                # Log message from the Information window
                for elem in Information_window.descendants(control_type="Text"):
                    msg = elem.window_text()
                    print(msg)
                    logging.info(msg)
                time.sleep(time_sleep)
                
                # Find button to open the file
                ok_btn = None
                #print("All elements in child window (Information):")
                for element in Information_window.descendants():
                    #print(f"{element.element_info.control_type}: {element.window_text()}")
                    if element.window_text() == "OK":
                        ok_btn = element
                        break
                # Click the button OK if found
                if ok_btn:
                    ok_btn.click_input()
                    time.sleep(time_sleep)
                else:
                    logging.error(f"OK button not found in window: {msg}")
            break
        if main_win.child_window(title="Error").exists():
            if main_win.child_window(title="Error").is_visible():
                # Capture the error window
                error_window = main_win.child_window(title="Error")
                for elem in error_window.descendants(control_type="Text"):
                    msg = elem.window_text()
                    print(msg)
                    logging.info(msg)
                time.sleep(time_sleep)

                # Find button to open the file
                ok_btn = None
                #print("All elements in child window (Error):")
                for element in error_window.descendants():
                    #print(f"{element.element_info.control_type}: {element.window_text()}")
                    if element.window_text() == "OK":
                        ok_btn = element
                        break
                # Click the button OK if found
                if ok_btn:
                    ok_btn.click_input()
                    time.sleep(time_sleep)
                else:
                    logging.error(f"OK button not found in window: {msg}")

                # Close application
                main_win.close()
                logging.info(f"Application closed successfully after error message: {msg}")
                return False
            break

    #===========================
    # === Convert bin to txt ===
    #===========================

    # Make sure the main window is active
    main_win.set_focus()
    time.sleep(0.5)

    # Send F8 key to open the dialog window (Converter->Report of experiment...)
    send_keys('{F8}')
    time.sleep(time_sleep)  # Wait for the dialog to appear

    # Find INS_Converted.BIN file in the dialog
    list_bin_files = main_win.child_window(control_type="List")
    bin_file = None
    for element in list_bin_files.descendants(control_type="ListItem"):
        #print(element.window_text())
        if element.window_text() == "INS_Converted":
           bin_file = element
           break # Stop after finding the first INS_Converted item

    if bin_file:
        bin_file.click_input()
        time.sleep(time_sleep)
    else:
        logging.error("INS_Converted file not found in the list.")

    # Click the Open button (if present)
    if open_btn.is_enabled():
        open_btn.click_input()
        time.sleep(time_sleep)  # Wait for the operation to complete
    else:
        logging.error(f"Button to open {bin_file.window_text()} not found or not enabled.")

    # ========================================================================
    # Wait for the Information/Error window about converting bin to txt appear
    # ========================================================================
    
    while True:
        if main_win.child_window(title="Information").exists():
            if main_win.child_window(title="Information").is_visible():
                # Capture the Information window
                Information_window = main_win.child_window(title="Information")
                # Log message from the Information window
                for elem in Information_window.descendants(control_type="Text"):
                    msg = elem.window_text()
                    print(msg)
                    logging.info(msg)
                time.sleep(time_sleep)
                
                # Find button to open the file
                ok_btn = None
                #print("All elements in child window (Information):")
                for element in Information_window.descendants():
                    #print(f"{element.element_info.control_type}: {element.window_text()}")
                    if element.window_text() == "OK":
                        ok_btn = element
                        break
                # Click the button OK if found
                if ok_btn:
                    ok_btn.click_input()
                    time.sleep(time_sleep)
                else:
                    logging.error(f"OK button not found in window: {msg}")
            break
        if main_win.child_window(title="Error").exists():
            if main_win.child_window(title="Error").is_visible():
                # Capture the error window
                error_window = main_win.child_window(title="Error")
                for elem in error_window.descendants(control_type="Text"):
                    msg = elem.window_text()
                    print(msg)
                    logging.info(msg)
                time.sleep(time_sleep)

                # Find button to open the file
                ok_btn = None
                #print("All elements in child window (Error):")
                for element in error_window.descendants():
                    #print(f"{element.element_info.control_type}: {element.window_text()}")
                    if element.window_text() == "OK":
                        ok_btn = element
                        break
                # Click the button OK if found
                if ok_btn:
                    ok_btn.click_input()
                    time.sleep(time_sleep)
                else:
                    logging.error(f"OK button not found in window: {msg}")

                # Close application
                main_win.close()
                logging.info(f"Application closed successfully after error message: {msg}")
                return False
            break

    # Close application
    main_win.close()
    logging.info(f"Application closed successfully after message: {msg}")
    return True

if __name__ == "__main__":
    import sys
    # Usage: python call_ison_gui.py <app_exe> [time_sleep]
    app_exe = sys.argv[1] if len(sys.argv) > 1 else r"c:\DimDev\DataTools\Read_BIN\ISON_321_20250314\ISON_321.exe"
    time_sleep = float(sys.argv[2]) if len(sys.argv) > 2 else 1
    call_ison_gui(app_exe, time_sleep)