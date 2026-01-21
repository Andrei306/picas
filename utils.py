import math
import csv
import os

"""
@file utils.py
@brief Helper module for mathematical conversions and color identification logic.
"""

colors_db = {}

"""
@brief Internal function to load colors from a CSV file into the global dictionary.
Format of CSV expected: R,G,B,Name
"""

def _load_color_database(filename='dict.csv'):
    global colors_db
    if colors_db:
        return

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, filename)

    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    r = int(row['R'].strip())
                    g = int(row['G'].strip())
                    b = int(row['B'].strip())
                    name = row['Name'].strip()
                    colors_db[(r, g, b)] = name
                except ValueError:
                    continue # skip lines with bad data
    except FileNotFoundError:
        print(f"Error: {filename} not found. Using fallback colors.")
        # fallback minimal database just in case
        colors_db[(0,0,0)] = "Black"
        colors_db[(255,255,255)] = "White"

_load_color_database()

"""
@brief Converts an RGB tuple to a HEX string format.
Used primarily for UI display purposes where colors must be defined as hex strings.

@param rgb_tuple - Tuple of 3 integers (Red, Green, Blue).
@return str - Hexadecimal string format (e.g., '#FF0000').
"""
def rgb_to_hex(rgb_tuple):
    return '#{:02x}{:02x}{:02x}'.format(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])

"""
@brief Identifies the closest color name from a predefined database.
Calculates the Euclidean distance between the requested RGB value and all colors 
in the database to find the best match.

@param requested_rgb - Tuple of 3 integers representing the target color.
@return str - The name of the closest matching color.
"""
def get_closest_color_name(requested_rgb):

    min_distance = float('inf')
    closest_name = "Unknown"

    r_req, g_req, b_req = requested_rgb

    for rgb, name in colors_db.items():
        r_db, g_db, b_db = rgb
        # Euclidean distance formula
        distance = math.sqrt((r_req - r_db)**2 + (g_req - g_db)**2 + (b_req - b_db)**2)

        if distance < min_distance:
            min_distance = distance
            closest_name = name

    return closest_name