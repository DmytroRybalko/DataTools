# Read_BIN Project

## Overview
The `Read_BIN` project is a Python-based automation tool designed to process, extract, and analyze data from binary files and interact with GUI applications. It includes robust error handling, logging, and modularized scripts for ease of use and maintenance.

## Features
- **File Processing**: Extract, rename, and move files from various directories.
- **GUI Automation**: Automate interactions with the ISON application using `pywinauto`.
- **Data Extraction**: Extract location and time data from binary files.
- **Logging**: Comprehensive logging for debugging and monitoring.
- **Environment Setup**: Automated setup using `ison_parser.bat`.

## Directory Structure
```
Read_BIN/
├── ISON_321_20250314/      # ISON application and related resources
├── ison_parser/            # Python package for data extraction and GUI automation
├── raw/                    # Raw binary files
├── requirements.txt        # Python dependencies
├── ison_parser.bat         # Batch file for environment setup
└── timestamp_geo_parser.py # Main script for automation
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/DmytroRybalko/DataTools.git
   cd DataTools/Read_BIN
   ```

2. Run the batch file to set up the environment (only once):
   ```bash
   .\ison_parser.bat
   ```

## Usage
1. Activate the virtual environment:
   ```bash
   .\env\Scripts\activate
   ```

2. Run the main script with parameters:
   ```bash
   python timestamp_geo_parser.py <root folder> <ISON folder> <ison exe file>
   example: python timestamp_geo_parser.py C:\DimDev\DataTools\Read_BIN\ison_parser_project ISON_321_20250314 ISON_321.exe
   ```

## Dependencies
- `pywinauto`
- `pandas`
- `numpy`

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For any inquiries, please contact [Dmytro Rybalko](mailto:dmytro.rybalko@example.com).
