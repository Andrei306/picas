import math

"""Converts RGB (ex: (255, 0, 0)) to HEX string format (ex: '#FF0000'). Used to print the colour code in UI"""
def rgb_to_hex(rgb_tuple):
    return '#{:02x}{:02x}{:02x}'.format(rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])

"""Find colour name and closest one from a list. Calculate Euclidian distance between the real and found colour"""
def get_closest_color_name(requested_rgb):
    colors_db = {
        # --- Reds & Pinks ---
        (139, 0, 0): "Dark Red",
        (255, 0, 0): "Red",
        (255, 99, 71): "Tomato",
        (255, 192, 203): "Pink",
        (255, 105, 180): "Hot Pink",
        (199, 21, 133): "Medium Violet Red",
        (219, 112, 147): "Pale Violet Red",

        # --- Oranges ---
        (255, 69, 0): "Orange Red",
        (255, 140, 0): "Dark Orange",
        (255, 165, 0): "Orange",
        (255, 215, 0): "Gold",

        # --- Yellows ---
        (255, 255, 0): "Yellow",
        (240, 230, 140): "Khaki",
        (107, 142, 35): "Olive Drab",
        (128, 128, 0): "Olive",

        # --- Purples  ---
        (230, 230, 250): "Lavender",
        (216, 191, 216): "Thistle",
        (221, 160, 221): "Plum",
        (238, 130, 238): "Violet",
        (218, 112, 214): "Orchid",
        (255, 0, 255): "Magenta",
        (186, 85, 211): "Medium Orchid",
        (147, 112, 219): "Medium Purple",
        (170, 122, 158): "Dusty Purple",
        (138, 43, 226): "Blue Violet",
        (75, 0, 130): "Indigo",
        (128, 0, 128): "Purple",
        (102, 51, 153): "Rebecca Purple",
        (72, 61, 139): "Dark Slate Blue",

        # --- Greens ---
        (173, 255, 47): "Green Yellow",
        (50, 205, 50): "Lime Green",
        (0, 255, 0): "Lime",
        (144, 238, 144): "Light Green",
        (34, 139, 34): "Forest Green",
        (0, 128, 0): "Green",
        (0, 100, 0): "Dark Green",
        (46, 139, 87): "Sea Green",
        (25, 61, 44): "Dark Jungle Green",
        (1, 50, 32): "Dark Green (Pine)",
        (85, 107, 47): "Dark Olive Green",
        (0, 86, 59): "Deep Green",
        (60, 179, 113): "Medium Sea Green",
        (32, 178, 170): "Light Sea Green",

        # --- Blues / Cyans ---
        (0, 255, 255): "Cyan",
        (43, 96, 108): "Dark Teal",
        (0, 128, 128): "Teal",
        (0, 139, 139): "Dark Cyan",
        (54, 116, 125): "Petrol Blue",
        (0, 206, 209): "Dark Turquoise",
        (64, 224, 208): "Turquoise",
        (95, 158, 160): "Cadet Blue",
        (70, 130, 180): "Steel Blue",
        (176, 196, 222): "Light Steel Blue",
        (135, 206, 235): "Sky Blue",
        (30, 144, 255): "Dodger Blue",
        (0, 0, 255): "Blue",
        (0, 0, 205): "Medium Blue",
        (0, 0, 139): "Dark Blue",
        (25, 25, 112): "Midnight Blue",

        # --- Browns ---
        (255, 248, 220): "Cornsilk",
        (222, 184, 135): "Burlywood",
        (244, 164, 96): "Sandy Brown",
        (210, 105, 30): "Chocolate",
        (160, 82, 45): "Sienna",
        (165, 42, 42): "Brown",
        (128, 0, 0): "Maroon",

        # --- Whites / Greys / Blacks ---
        (255, 255, 255): "White",
        (245, 245, 245): "White Smoke",
        (220, 220, 220): "Gainsboro",
        (192, 192, 192): "Silver",
        (169, 169, 169): "Dark Gray",
        (128, 128, 128): "Gray",
        (105, 105, 105): "Dim Gray",
        (47, 79, 79): "Dark Slate Gray",
        (0, 0, 0): "Black"
    }

    min_distance = float('inf')
    closest_name = "Unknown"

    r_req, g_req, b_req = requested_rgb

    for rgb, name in colors_db.items():
        r_db, g_db, b_db = rgb
        distance = math.sqrt((r_req - r_db)**2 + (g_req - g_db)**2 + (b_req - b_db)**2)

        if distance < min_distance:
            min_distance = distance
            closest_name = name

    return closest_name