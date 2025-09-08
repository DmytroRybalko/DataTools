
# DataTools: Read_Logger Project

This project provides a set of tools and scripts for automating the download, processing, and management of data from logger devices. It is designed for data engineers and analysts who need to collect, parse, and analyze log files from various sources.

## Project Structure

- **Read_Logger/**: Main application folder containing scripts and resources for interacting with logger devices.
    - **build_exe.bat**: Batch script to install dependencies, build the executable, and set up Playwright browsers.
    - **data_from_logger.py**: Main script for extracting and processing data from logger files.
    - **files2download.txt**: List of files available or required for download from loggers.
    - **requirements.txt**: Python dependencies required for running the project.
    - **data/**: Contains raw data files (typically zipped) collected from logging devices. Each file is named according to the device and session.
    - **logger/**: Contains scripts and resources for interacting with loggers, including:
        - **aux_functions.py**: Utility functions used across logger scripts.
        - **connect2logger.py**: Handles connection logic to logger devices.
        - **data_from_logger_main.py**: Main entry point for logger data extraction workflows.
        - **data_from_logger.py**: Core logic for reading and parsing logger data files.
        - **get_logger_url.py**: Retrieves URLs or endpoints for logger devices.
        - **test_example.py**, **test_launch_browser.py**: Example and test scripts for validating logger interactions.
        - **data_logger_get_method.png**, **example.png**: Example images and diagrams related to logger data extraction.
        - **files2download.txt**: Logger-specific file list.
- **Sandbox/**: Folder for experimental, prototype, or development scripts not part of the main workflow.
- **copilot_chat_data_logger.md**: Documentation and notes related to Copilot Chat and data logger usage.
- **ipconfig_pc.txt**: Example output of PC network configuration, useful for troubleshooting logger connectivity.
- **login2datalogger.txt**: Instructions or logs related to logging into the data logger web interface.
- **tp-link_as_router_config.html**: Example configuration for using a TP-Link device as a router for logger connectivity.
- **use_anaconda.txt**: Notes or instructions for using Anaconda Python environment with the project.
- **files2download.txt**: General list of files to download, used across the project.

## Key Functions
- **Data Extraction**: Scripts in `Read_Logger/logger/` and the main `data_from_logger.py` handle reading, parsing, and converting logger data into usable formats.
- **Device Connection**: `connect2logger.py` manages connections to physical logger devices or endpoints.
- **Automation**: Batch scripts and utility functions streamline repetitive tasks such as building executables and downloading files.
- **Testing**: Example and test scripts ensure reliability and correctness of logger interactions.

## Usage Overview
1. Place raw logger data files in the appropriate `data/` folder.
2. Use the scripts in `Read_Logger/logger/` to connect to devices, download data, and process files.
3. Run `data_from_logger.py` to extract and analyze data as needed.
4. Refer to `requirements.txt` for necessary Python packages.

## License
See repository for license details.