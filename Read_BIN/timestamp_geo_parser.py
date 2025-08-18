import logging
import os
import zipfile
import shutil
import time
import ison_parser as ison
from ison_parser import global_logger

path = {
        'root_folder'      : r"C:\DimDev\DataTools\Read_BIN",
        'raw_folder'       : r"C:\DimDev\DataTools\Read_BIN\raw",
        'ison_data_folder' : r"C:\DimDev\DataTools\Read_BIN\ISON_321_20250314\data",
        'app_exe'          : os.path.join(r"C:\DimDev\DataTools\Read_BIN\ISON_321_20250314", "ISON_321.exe"),
        'ison_folder'      : r"C:\DimDev\DataTools\Read_BIN\ISON_321_20250314"
    }

raw_folder = path['raw_folder']
ison_data_folder = path['ison_data_folder']
app_exe = path['app_exe']
ison_folder = path['ison_folder']
processed_folder = os.path.join(path['root_folder'], "processed")

# Create processed folder if it doesn't exist
os.makedirs(processed_folder, exist_ok=True)
 
time_start = time.time()

for file in os.listdir(raw_folder):
    if not file.endswith('.zip'):
        continue  # Skip files that are not zip files

    zip_name = file.split(".")[0] # Extract the name without .zip
    zip_path = os.path.join(raw_folder, file)
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ison_folder)
            src = os.path.join(ison_folder, zip_name)
            dst = ison_data_folder
            if os.path.exists(dst):
                shutil.rmtree(dst, ignore_errors=True)
            # if os.path.exists(dst):
            #     try:
            #         shutil.rmtree(dst, ignore_errors=True)
            #     except Exception as e:
            #         logging.error(f"Failed to remove {dst}: {e}")
            # if os.path.exists(dst):
            #     # If still exists (e.g., file lock), log and skip
            #     logging.error(f"Destination folder still exists: {dst}")
            #     continue
            os.rename(src, dst)# rename \ISON_321_20250314\INS-BDAA6D-000000458' -> \ISON_321_20250314\data

            # Call the GUI application
            if ison.call_ison_gui(app_exe, 0.5):        
                #os.rename(src, dst)
                ins_txt_file = os.path.join(ison_data_folder, "INS_Converted.txt")
                timestamp = ison.extract_time(ins_txt_file)
                (lat, lon) = ison.extract_location(ins_txt_file)
                location  = ison.recognize_location(float(lat), float(lon), 0.17)
                #print(f"Timestampt: {timestamp}, Location: {location} (Lat: {lat}, Lon: {lon})")
                logging.info(f"New name: {timestamp}_{location}_{zip_name}")
                new_dir = os.path.join(processed_folder, f"{timestamp}_{location}_{zip_name}")
                shutil.copytree(ison_data_folder, new_dir, dirs_exist_ok=True)                  # Copy the entire data folder
                time.sleep(0.5)  
            else:
                logging.error(f"call_ison_gui failed for {file}")
    except Exception as e:
        logging.error(f"Error processing {file}: {e}")
        continue
    
    print(f"Elapsed time for all files: {time.time() - time_start:.2f} seconds")

if __name__ == "__main__":
    import sys
    # Usage: python timestamp_geo_parser.py <raw_folder> <ison_data_folder> <app_exe>
    path = {
        'root_folder'      : r"C:\DimDev\DataTools\Read_BIN",
        'raw_folder'       : r"C:\DimDev\DataTools\Read_BIN\raw",
        'ison_data_folder' : r"C:\DimDev\DataTools\Read_BIN\ISON_321_20250314\data",
        'app_exe'          : os.path.join(r"C:\DimDev\DataTools\Read_BIN\ISON_321_20250314", "ISON_321.exe"),
        'ison_folder'      : r"C:\DimDev\DataTools\Read_BIN\ISON_321_20250314"
    }
    # 
    #timestamp_geo_parser(paths)
