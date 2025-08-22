import re
from collections import Counter

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def find_header_line(path2file, max_lines=1000):
    """
    Finds the header line that starts with 'GPS_INS_Time_Round'.
    Returns the header line and its line number.
    """
    # Initialize a dictionary to store line number, count of columns, and type (True if all are numbers)
    df = dict()
    df['line'], df['count'], df['type'] = [], [], []
    
    # Read the file line by line limiting to max_lines
    with open(path2file, 'r', encoding='utf-8') as f:
        for i in range(max_lines):
            line = next(f)
            df['line'].append(i)
            df['count'].append(len(re.split(r'\s+', line.strip()))) 
            df['type'].append(all([is_number(i) for i in re.split(r'\s+', line.strip())]))

        # Create a dictionary contains lead values from df dict 
        lead_df = {key: df[key][1:] + [None] for key in df.keys()}
        max_repeated = Counter(df['count']).most_common(1)[0][0]
        # Capture the header's line 
        for i in lead_df['line']:
            if (
                df['count'][i] == lead_df['count'][i]   # Check if current line has the same number of columns as the next
                and df['type'][i] == True               # Check if all values are numbers
                and df['type'][i] == lead_df['type'][i] # Check if next line also numbers
                and df['count'][i] == max_repeated      # Check if the line contains the most common number of columns 
                and df['type'][i-1] == False            # Check if the previous line is a string - potential header
                and df['count'][i-1] == df['count'][i]  # Check if the previous line has the same number of columns
                ):  
                    break    
    
    return (i - 1)

def extract_location(path2file):
    """
    Finds the header line containing column names, finds 'Latitude' and 'Longitude' columns,
    skips 12000 lines, and extracts the corresponding values.
    Returns coordinates as tuple (<lat>, <lon>)
    """
    # Get header line
    header_line_num = find_header_line(path2file)
    header = None
    
    # Skip lines until the header line
    with open(path2file, 'r', encoding='utf-8') as f:
        for _ in range(header_line_num):
            next(f)

        line = next(f)    
        header = re.split(r'\s+', line.strip())
        #print("Header found:", header)
    
    if header is None:
        raise ValueError("Header line not found.")
    
    # Find column indices for whole words 'Latitude' and 'Longitude'
    lat_idx = next(
        i for i, col in enumerate(header)
        if re.fullmatch(r'Latitude(_HR)?', col.strip(), re.IGNORECASE)
    )
    lon_idx = next(
        i for i, col in enumerate(header)
        if re.fullmatch(r'Longitude(_HR)?', col.strip(), re.IGNORECASE)
    )
    
    # Reopen file and skip header + 12000 lines
    try:
        with open(path2file, 'r', encoding='utf-8') as f:
            for _ in range(header_line_num + 1 + 12000):
                next(f)
            data_line = next(f)
            data = re.split(r'\s+', data_line.strip())
            lat = data[lat_idx]
            lon = data[lon_idx]
    except Exception:
            lat, lon = '50.0128', '29.9794' # Default coordinates if extraction fails
        
    return (lat, lon)

if __name__ == "__main__":
    import sys
    # Usage: python extract_location.py <path2file>
    path2file = sys.argv[1] if len(sys.argv) > 1 else "Read_BIN/ISON_321_20250314/data/INS_Converted.txt"
    result = extract_location(path2file)
    print(result)