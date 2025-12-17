import math

"""Converts RGB (ex: (255, 0, 0)) to HEX string format (ex: '#FF0000'). Used to print the colour code in UI"""
def rgb_to_hex(rgb_tuple):
    return '#{:02x}{:02x}{:02x}'.format(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])

"""Find colour name and closest one from a list. Calculate Euclidian distance between the real and found colour"""
def get_closest_color_name(requested_rgb):
    colors_db = {
        (0, 0, 0): "Black",
        (255, 255, 255): "White",
        (255, 0, 0): "Red",
        (0, 255, 0): "Green",
        (0, 0, 255): "Blue",
        (255, 255, 0): "Yellow",
        (0, 255, 255): "Cyan",
        (255, 0, 255): "Magenta",
        (192, 192, 192): "Silver",
        (128, 128, 128): "Gray",
        (128, 0, 0): "Maroon",
        (128, 128, 0): "Olive",
        (0, 128, 0): "Dark Green",
        (128, 0, 128): "Purple",
        (0, 128, 128): "Teal",
        (0, 0, 128): "Navy",
        (255, 165, 0): "Orange",
        (245, 245, 220): "Beige",
        (165, 42, 42): "Brown"
    }
    min_distance = float('inf')
    cloest_name = "Unknown"

    r_req, g_req, b_req = requested_rgb

    for rgb, name in colors_db.items():
        r_db, g_db, b_db = rgb
        distance = math.sqrt((r_req - r_db)**2 + (g_req - g_db)**2 + (b_req - b_db)**2)

        if distance < min_distance:
            min_distance = distance
            cloest_name = name

    return cloest_name