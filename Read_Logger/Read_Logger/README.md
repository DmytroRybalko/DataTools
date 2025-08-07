# Read_Logger

A python console application to download files from a data logger web interface.

## Features
- Automatically fetches the list of available files from the logger
- Downloads all files to a specified directory
- Can be run as a Python script 

## Requirements
- Windows 10/11
- Python 3.8+
- Internet/network access to the logger device

## Setup and Usage

### 1. Clone or Copy the Repository
Copy the entire `Read_Logger` folder to your PC.

### 2. Setup python if needed (optionally)

### 3. Setup python if needed (optionally)
Copy the entire `Read_Logger` folder to your PC.

### 4. Setup libraries (at first using)
1. Open a command prompt in the `Read_Logger` folder.
2. Run:
    ```
    build_exe.bat
    ```
   This will install dependencies, build the executable, and install Playwright browsers.

### 3. Run the Application 

1. Open a command prompt (not PowerShell) in the `Read_Logger` folder.
2. Activate python virtual environment where all libraries are:
    ```
    logger\Scripts\activate.bat   
    ```
3. Run script with actual parameters:
    ```
    python data_from_logger.py --ip http://192.168.0.102 --save_dir data
    ```

- Replace `http://192.168.0.102` with your logger's IP address if different.
- The `--save_dir` argument is optional (default is `data`).

## Notes
- The first run may take longer as Playwright downloads browser binaries.
- Make sure your logger device is accessible from your PC.
- All downloaded files will be saved as `.zip` in the specified directory.

## Troubleshooting
- If you see errors about missing dependencies, rerun `build_exe.bat` or install them manually.
- If Playwright browsers are missing, run `playwright install`.
- For network errors, check your logger's IP and network connection.

---

**Author:** Dmytro Rybalko
