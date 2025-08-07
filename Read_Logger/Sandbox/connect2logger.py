import requests
from datetime import datetime

# Налаштування
url = "http://192.168.0.102/cgi-bin/download?M2001887-000000001"
save_path = f"c:/DimDev/DataTools/Read_Logger/data/{datetime.now():%Y%m%d_%H%M%S}.zip"
# Завантаження
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    with open(save_path, 'wb') as f:
        f.write(response.content)

    print(f"[+] File saved to: {save_path}")
except Exception as e:
    print(f"[!] Error: {e}")


import requests
from datetime import datetime
import os

# List of URLs
urls = [
    "http://192.168.0.102/cgi-bin/download?M2001887-000000001",
    "http://192.168.0.102/cgi-bin/download?M2001887-000000002",
    # Add more URLs here
]

save_dir = "c:/DimDev/DataTools/Read_Logger/data"
os.makedirs(save_dir, exist_ok=True)

for url in urls:
    file_id = url.split('=')[-1]
    save_path = f"{save_dir}/{file_id}_{datetime.now():%Y%m%d_%H%M%S}.zip"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"[+] File saved to: {save_path}")
    except Exception as e:
        print(f"[!] Error downloading {url}: {e}")