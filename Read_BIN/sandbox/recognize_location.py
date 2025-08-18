import csv

def recognize_location(target_lat, target_lon, threshold_radius):
    """
    Finds the nearest known location to the given latitude and longitude.
    Uses a hardcoded dictionary of locations and their coordinates.
    If the minimum distance is within the threshold_radius (in degrees, ~0.17 ≈ 18.5 km),
    returns the name of the nearest location. Otherwise, returns the coordinates as a string.
    """
    # Uncomment the following lines if you want to read from a CSV file
    # locations = {}
    # with open(csv_path, 'r', encoding='utf-8') as f:
    #     reader = csv.DictReader(f, delimiter=',')
    #     for row in reader:
    #         location = row['Location']
    #         latitude = float(row['Latitude'])
    #         longitude = float(row['Longitude'])
    #         locations[location] = (latitude, longitude)

    locations = \
    {'Borodianka':      (50.6658, 29.9328),
     'Buzova':          (50.4017, 30.0536),
     'Chepelivka/Uzyn': (49.7906, 30.4414),
     'Chaika':          (50.4286, 30.2983),
     'Dymer':           (51.0070, 29.9781),
     'Hoholiv':         (50.5134, 31.0455),
     'Hostomel':        (50.6033, 30.1917),
     'Zhuliany':        (50.4017, 30.4494),
     'Sviatoshyn':      (50.4789, 30.3858),
     'Vasylkiv':        (50.2331, 30.2997),
     'Bila Tserkva':    (49.7947, 30.0300),
     'Ksaverivka':      (50.0056, 30.1978),
     'Nalyvaikivka':    (50.4792, 29.7356),
     'Palianychyntsi':  (50.0128, 29.9794),
     'Romashky':        (49.7353, 30.5536),
     'Boryspil':        (50.3450, 30.8944),
     'Kyiv South':      (50.4167, 30.5167)}
    
    # Calculate the distance from the target location to each known location
    result = {}
    for location, (latitude, longitude) in locations.items():
         result[location] = ((latitude - target_lat)**2 + (longitude - target_lon)**2)**0.5
    
    # 111 km is approximately 1 degree of latitude or longitude
    # Keep threshold radius 1/6 degree = 0.17 degree ~ 18.5 km. If where is no location within this radius,
    # return target lat/lon as string: "{target_lat}_{target_lon}"
    
    #print(threshold_radius) 

    min_location = min(result, key=result.get)
    if result[min_location] <= threshold_radius:
        return min_location
    else:
        return f"{target_lat}_{target_lon}"

if __name__ == "__main__":
    import sys
    # Usage: python recognize_location.py <lat> <lon> [csv_path]
    lat = 50.0 #float(sys.argv[1])
    lon = 30.0 #float(sys.argv[2])
    csv_path = sys.argv[3] if len(sys.argv) > 3 else "Read_BIN/data/kyiv_airfields.csv"
    locations = recognize_location(lat, lon, 0.17)
    print(locations)
