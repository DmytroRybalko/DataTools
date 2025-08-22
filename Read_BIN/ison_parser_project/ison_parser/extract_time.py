import re

def extract_time(path2file):
    """
    Extracts date and time from the first line of INS_Converted.txt and returns it as 'YYYY-MM-DD_HH-MM-SS'.
    """
    with open(path2file, 'r', encoding='utf-8') as f:
        first_line = f.readline()
    # Regex to find date and time in format DD.MM.YYYY HH:MM:SS
    match = re.search(r'(\d{2})\.(\d{2})\.(\d{4}) (\d{2}):(\d{2}):(\d{2})', first_line)
    if match:
        day, month, year, hour, minute, second = match.groups()
        return f"{year}-{month}-{day}_{hour}-{minute}-{second}"
    else:
        return f"year-month-day_time"

if __name__ == "__main__":
    import sys
    # Usage: python extract_time.py <path2file>
    path2file = sys.argv[1] if len(sys.argv) > 1 else "Read_BIN/ISON_321_20250314/data/INS_Converted.txt"
    result = extract_time(path2file)
    print(result)
