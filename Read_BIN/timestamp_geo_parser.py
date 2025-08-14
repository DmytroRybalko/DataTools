#
import os
import zipfile
import shutil
import time
import ison_parser as ison

path = {
        'root_folder'      : r"C:\DimDev\DataTools\Read_BIN",
        'raw_folder'       : r"C:\DimDev\DataTools\Read_BIN\raw",
        'ison_data_folder' : r"C:\DimDev\DataTools\Read_BIN\ISON_321_20250314\data",
        'app_exe'          : os.path.join(r"C:\DimDev\DataTools\Read_BIN\ISON_321_20250314", "ISON_321.exe"),
        'ison_folder'      : r"C:\DimDev\DataTools\Read_BIN\ISON_321_20250314"
    }

#def timestamp_geo_parser(path):
    # Loop through all zip files in the given folder
# 
raw_folder = path['raw_folder']
ison_data_folder = path['ison_data_folder']
app_exe = path['app_exe']
ison_folder = path['ison_folder']
processed_folder = os.path.join(path['root_folder'], "processed")

# Create processed folder if it doesn't exist
os.makedirs(processed_folder, exist_ok=True)
# 
for file in os.listdir(raw_folder):
    if file.endswith('.zip'):
        zip_name = file.split(".")[0] # Extract the name without .zip
        zip_path = os.path.join(raw_folder, file)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(ison_folder)
            if os.path.exists(ison_data_folder):
                shutil.rmtree(ison_data_folder, ignore_errors=True)
            os.rename(os.path.join(ison_folder, zip_name), ison_data_folder) # rename \ISON_321_20250314\INS-BDAA6D-000000458' -> \ISON_321_20250314\data
    
    # Call call_ison_gui.py to convert INS_Converted.BIN to INS_Converted.txt
    #ison.call_ison_gui(app_exe, 0.5)    

    try: 
        if ison.call_ison_gui(app_exe, 0.5):
            # Extract timestamp and geo coordinates
            ins_txt_file = os.path.join(ison_data_folder, "INS_Converted.txt")
            timestamp = ison.extract_time(ins_txt_file)
            (lat, lon) = ison.extract_location(ins_txt_file)
            location  = ison.recognize_location(float(lat), float(lon), 0.17)
            print(f"Timestampt: {timestamp}, Location: {location} (Lat: {lat}, Lon: {lon})")
            print(f"New name: {timestamp}_{location}_{zip_name}")
            new_dir = os.path.join(processed_folder, f"{timestamp}_{location}_{zip_name}")
            #os.makedirs(new_dir, exist_ok=True)
            shutil.copytree(ison_data_folder, new_dir, dirs_exist_ok=True)  # Copy the entire data folder
        time.sleep(0.5)  # Wait for the copy to complete
    except Exception as e:
        print(f"Error processing {file}: {e}")
        continue

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
