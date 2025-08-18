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
                    print(f"Line {i} matches the criteria.")
                    print(f"Line {i} has {df['count'][i]} columns and type {df['type'][i]}.")
                    break
        
        return (i - 1)

def find_header_line_test():
    """
    Finds the header line by recognizing a specific data pattern.

    We read text file line by line, getting the order number of line,
    calculate number of strings in line and them check whether all string in line are numbers.
    Then we compare count of columns of current line with values of next line.
    The equality of these values says us we see numerical data and the header line is before it.
    For example:
    {'line': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    'count': [9, 9, 1, 37, 1, 79, 79, 79, 79, 79],
    'type': [False, False, False, False, False, False, True, True, True, True]}

    """
    
    # %%
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    #print(is_number("12.3"))  # True
    #print(is_number("abc"))   # False

    # %%
    path2file = "Read_BIN/ISON_321_20250314/data/INS_Converted.txt"

    # %%
    # Create a dictionary to store line number, count of columns, and type (True if all are numbers)
    df = dict()
    df['line'], df['count'], df['type'] = [], [], []
    
    with open(path2file, 'r', encoding='utf-8') as f:
        # Skip the first 212 lines to reach the header (for testing purposes)
        for _ in range(212):
            next(f)

        for i, line in enumerate(f):
            if i < 10:  # Limit to first 10 lines for testing
                df['line'].append(i)
                df['count'].append(len(re.split(r'\s+', line.strip()))) 
                #print(len(re.split(r'\s+', line.strip())))
                #print(re.split(r'\s+', line.strip()))
                df['type'].append(all([is_number(i) for i in re.split(r'\s+', line.strip())]))

 # %%
    lead_df = {key: df[key][1:] + [None] for key in df.keys()}
    print(lead_df)

    # %% Criteria of the maximum number of columns and maximum number repeated values
    from collections import Counter
    max_count = max(df['count'])
    max_repeated = Counter(df['count']).most_common(1)[0][0]
    print("Most repeated value:", max_repeated)

    # %% Criteria that all words in line are capitalized
    with open(path2file, 'r', encoding='utf-8') as f2:
        for i in range(300):
            line = next(f2)
            #print([w for w in re.split(r'\s+', line.strip())]) #re.fullmatch(r'[A-Z][a-zA-Z]*', w)
            matches = all([re.fullmatch(r'[A-Z][a-zA-Z]*', w) for w in re.split(r'\s+', line.strip())])
            if matches:
                print(f"Line {i}: {line.strip()}")
                break

    
    # %% Criteria of the maximum number of columns and maximum number repeated values
    header = lambda line: all([re.fullmatch(r'[A-Z][a-zA-Z]*', w) for w in re.split(r'\s+', line.strip())])
    max_repeated = Counter(df['count']).most_common(1)[0][0]
    with open(path2file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i > 0 and i < 300:  # Limit to first 300 lines for testing
                if (
                    lead_df['type'][i] == True                  # Check if all values are numbers 
                    and df['type'][i] == lead_df['type'][i]     # Check if types match
                    and df['count'][i] == lead_df['count'][i]   # Check if column counts match
                    and df['count'][i] == max_repeated          # Check if current count is the most common
                    and header(line)           # Check if the previous line is matching pattern (header line)
                    ):
                        print(f"Line {i} matches the criteria: {line}")
                        print(f"Line {i} has {df['count'][i]} columns and type {df['type'][i]}.")
                        
                        break
        

    # %%
    df

    # %%

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
        print("Header found:", header)
    
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
    
    #=== TEST find_header_line() ===
    # hl = find_header_line(path2file)
    # with open(path2file, 'r', encoding='utf-8') as f:
    #     for i, line in enumerate(f):
    #         if i == hl:
    #             print(f"Header line {hl}: {re.split(r'\s+', line.strip())}")
    #             break

    #=== TEST extract_location() ===
    result = extract_location(path2file)
    print(result)

