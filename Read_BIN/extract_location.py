import re

def extract_location(path2file):
    """
    Finds the header line containing column names, finds 'Latitude' and 'Longitude' columns,
    skips 12000 lines, and extracts the corresponding values.
    Returns coordinates as tuple (<lat>, <lon>)
    """
    # Find header line that starts with 'GPS_INS_Time_Round'
    header_line_num = None
    header = None
    with open(path2file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if line.strip().startswith('GPS_INS_Time_Round'):
                header = re.split(r'\s+', line.strip())
                header_line_num = i
                #print("Header found:", line.strip())
                break
    if header is None:
        raise ValueError("Header line not found.")
    # Find column indices for whole words 'Latitude' and 'Longitude'
    lat_idx = next(
        i for i, col in enumerate(header)
        if re.fullmatch(r'Latitude', col.strip(), re.IGNORECASE)
    )
    lon_idx = next(
        i for i, col in enumerate(header)
        if re.fullmatch(r'Longitude', col.strip(), re.IGNORECASE)
    )
    # Reopen file and skip header + 12000 lines
    with open(path2file, 'r', encoding='utf-8') as f:
        for _ in range(header_line_num + 1 + 12000):
            next(f)
        data_line = next(f)
        data = re.split(r'\s+', data_line.strip())
        lat = data[lat_idx]
        lon = data[lon_idx]
        return (lat, lon)

if __name__ == "__main__":
    import sys
    # Usage: python extract_location.py <path2file>
    path2file = sys.argv[1] if len(sys.argv) > 1 else "Read_BIN/ISON_321_20250314/data/INS_Converted.txt"
    result = extract_location(path2file)
    print(result)