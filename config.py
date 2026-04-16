import os

# Path to the PDF template
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "FPL_TEMPLATE.pdf")

# --- FIELD MAP ---
# JSON key -> PDF AcroForm field name (or LIST of field names for multi-line)
FIELD_MAP = {
    # Casilla 7
    "aircraft_id":          "Aircraft identification",

    # Casilla 8
    "flight_rules":         "Flight rules",
    "type_of_flight":       "Textbox3",

    # Casilla 9
    "number":               "Number",
    "type_of_aircraft":     "Type of aircraft",
    "wake_turbulence_cat":  "Wake turbulence",

    # Casilla 10
    "equipment":            "Textbox7",
    "surveillance":         "Textbox8",

    # Casilla 13
    "departure_aerodrome":  "Textbox9",
    "departure_time":       "Textbox10",

    # Casilla 15
    "cruising_speed":       "Textbox11",
    "level":                "Textbox12",
    # Route (5 lines)
    "route":                ["Textbox13", "Textbox14", "Textbox15", "Textbox16", "Textbox17"],

    # Casilla 16
    "destination_aerodrome": "Textbox18",
    "total_eet":            "Textbox19",
    "altn_aerodrome":       "Textbox20",
    "altn_aerodrome_2":     "Textbox21",

    # Casilla 18
    # Other Information (4 lines)
    "other_info":           ["Textbox22", "Textbox23", "Textbox24", "Textbox25"],

    # Casilla 19
    "endurance":            "Textbox26",
    "persons_on_board":     "Textbox28",
    
    # Casilla 19 - Dinghies
    "dinghies_number":      "Textbox29",
    "dinghies_capacity":    "Textbox30",
    "dinghies_colour":      "Textbox31",

    # Casilla 19 - Bottom info
    "aircraft_colour":      "Textbox32",
    "remarks":              "Textbox33",
    "pilot_in_command":     "Textbox34",
    "filed_by":             "Textbox35",

    # Date field
    "date":                 "Textbox1", # To be confirmed
}

# --- CROSSOUT MAP ---
# Example coordinates (need to be adjusted after testing visibility)
# --- LINE LIMITS (characters per line) ---
ROUTE_LINE_LIMITS = [50, 75, 75, 75, 73]
OTHER_INFO_LINE_LIMITS = [72, 75, 75, 70]
FONT_NAME = "Helvetica"
CROSSOUT_MAP = {
    "radio_uhf": [], "radio_vhf": [], "radio_elt": [],
    "survival_polar": [], "survival_desert": [], "survival_maritime": [], "survival_jungle": [],
    "jackets_light": [], "jackets_fluor": [], "jackets_uhf": [], "jackets_vhf": [],
    "dinghies_cover": [],
}
