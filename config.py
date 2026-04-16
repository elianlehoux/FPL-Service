import os

# Path to the PDF template
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "FPL_TEMPLATE.pdf")

# --- FIELD MAP ---
FIELD_MAP = {
    "aircraft_id":          "Aircraft identification",
    "flight_rules":         "Flight rules",
    "type_of_flight":       "Textbox3",
    "number":               "Number",
    "type_of_aircraft":     "Type of aircraft",
    "wake_turbulence_cat":  "Wake turbulence",
    "equipment":            "Textbox7",
    "surveillance":         "Textbox8",
    "departure_aerodrome":  "Textbox9",
    "departure_time":       "Textbox10",
    "cruising_speed":       "Textbox11",
    "level":                "Textbox12",
    "route":                ["Textbox13", "Textbox14", "Textbox15", "Textbox16", "Textbox17"],
    "destination_aerodrome": "Textbox18",
    "total_eet":            "Textbox19",
    "altn_aerodrome":       "Textbox20",
    "altn_aerodrome_2":     "Textbox21",
    "other_info":           ["Textbox22", "Textbox23", "Textbox24", "Textbox25"],
    "endurance":            "Textbox26",
    "persons_on_board":     "Textbox28",
    "dinghies_number":      "Textbox29",
    "dinghies_capacity":    "Textbox30",
    "dinghies_colour":      "Textbox31",
    "aircraft_colour":      "Textbox32",
    "remarks":              "Textbox33",
    "pilot_in_command":     "Textbox34",
    "filed_by":             "Textbox35",
    "date":                 "Textbox1",
}

# --- LINE LIMITS ---
ROUTE_LINE_LIMITS = [50, 80, 80, 80, 73]
OTHER_INFO_LINE_LIMITS = [79, 81, 81, 74]
FONT_NAME = "Helvetica"

# --- AUTOMATIC CROSSOUT GROUPS ---
# "master_key": ["sub_key1", "sub_key2", ...]
# If ALL sub_keys are False, the master_key is also crossed out.
CROSSOUT_GROUPS = {
    "survival_all": ["survival_polar", "survival_desert", "survival_maritime", "survival_jungle"],
    "jackets_all":  ["jackets_light", "jackets_fluor", "jackets_uhf", "jackets_vhf"],
    "dinghies_all": ["dinghies_cover"], # Dinghies master (D)
    "remarks_all":  ["remarks_indicator"] # Remarks indicator (N)
}

# --- CROSSOUT COORDINATES ---
CROSSOUT_MAP = {
    # Indicator masters (S, J, D, N)
    "survival_all": [{"x": 50, "y": 205, "w": 15, "h": 15}],  # Master S
    "jackets_all":  [{"x": 271, "y": 205, "w": 15, "h": 15}], # Master J
    "dinghies_all": [{"x": 30, "y": 167, "w": 15, "h": 15}],  # Master D
    "remarks_all":  [{"x": 30, "y": 114, "w": 15, "h": 15}],  # Master N

    # Emergency Radio (R/) - Manual calibration
    "radio_uhf": [{"x": 353, "y": 246, "w": 15, "h": 15}],
    "radio_vhf": [{"x": 393, "y": 246, "w": 15, "h": 15}],
    "radio_elt": [{"x": 433, "y": 246, "w": 15, "h": 15}],

    # Survival Items
    "survival_polar":   [{"x": 87, "y": 205, "w": 15, "h": 15}],
    "survival_desert":  [{"x": 127, "y": 205, "w": 15, "h": 15}],
    "survival_maritime":[{"x": 166, "y": 205, "w": 15, "h": 15}],
    "survival_jungle":  [{"x": 208, "y": 205, "w": 15, "h": 15}],

    # Jackets Items
    "jackets_light":    [{"x": 313, "y": 205, "w": 15, "h": 15}],
    "jackets_fluor":    [{"x": 352, "y": 205, "w": 15, "h": 15}],
    "jackets_uhf":      [{"x": 392, "y": 205, "w": 15, "h": 15}],
    "jackets_vhf":      [{"x": 432, "y": 205, "w": 15, "h": 15}],

    # Dinghies Items
    "dinghies_cover":   [{"x": 141, "y": 167, "w": 15, "h": 15}],
}
