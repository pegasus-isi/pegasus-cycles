# -*- coding: utf-8 -*-

from itertools import *

column_names = [
    "unique_id",
    "country",
    "crop",
    "lat",
    "long",
    "weather",
    "soil",
    "start_planting_date",
    "end_planting_date",
    "fertilizer",
    "nitrogen_rate",
    "fertilizer_rate",
    "forcing",
    "planting_date_fixed",
    "weed_fraction",
    "disabled",
    "notes",
]
crop_name = []
country = ["South Sudan"]
soil = ["pongo.soil"]
weather = [
    "met8.88Nx27.12E.weather",
    "met8.88Nx27.38E.weather",
    "met8.88Nx27.62E.weather",
    "met9.12Nx26.62E.weather",
    "met9.12Nx26.88E.weather",
    "met9.12Nx27.12E.weather",
    "met9.12Nx27.38E.weather",
    "met9.12Nx27.62E.weather",
]
latitude = [
    "8.829099519",
    "8.923781802 8.984132814 8.755570551 8.820167532 8.883219298 8.908088282 8.998744933 8.93792366",
    "8.972398591 8.86024595 8.952655146 8.936357173 8.928924507",
    "9.121384874 9.119378463 9.129366152",
    "9.166162062 9.199570663 9.141141242 9.107271307",
    "9.191139714 9.094510053 9.115790067 9.130481542 9.16096445",
    "9.005184032 9.000342937 9.043091884 9.024157237 9.076631574 9.039018931 9.017684703",
    "9.001108886 9.014155302 9.020785507",
]
longitude = [
    "27.19601693",
    "27.31273652 27.31493641 27.37516169 27.45148756 27.43278379 27.40732517 27.48843616 27.41070765",
    "27.61273326 27.5548614 27.64580119 27.55398462 27.50769452",
    "26.74770849 26.62730866 26.56943995",
    "26.89553587 26.89694621 26.92771393 26.84613418",
    "27.02025261 27.08002874 27.02323762 27.16684993 27.04477233",
    "27.40063124 27.43337662 27.3915511 27.46177109 27.29878071 27.29859773 27.32907505",
    "27.62810838 27.5159694 27.59201436",
]
start_planting_date = ["100", "107", "114", "121", "128", "135", "142"]
end_planting_date = ["149"]
planting_date_fixed = ["True", "False"]
fertilizer = ["urea"]
nitrogen_rate = ["0", "25", "50", "100", "200", "400"]
fertilizer_rate = ["0.00", "78.13", "156.25", "312.50", "625.00", "1250.00"]
forcing = ["True", "False"]
weed_fraction = ["0.0", "0.05", "0.1", "0.2", "0.4"]
disabled = ["False"]
notes = [" "]

# dot product for coordinates
coordinates = zip(latitude, longitude, weather)

# dot product for fertilizers
fertilizers = zip(nitrogen_rate, fertilizer_rate)

rows = list(
    product(
        country,
        [crop_name],
        coordinates,
        soil,
        start_planting_date,
        end_planting_date,
        fertilizer,
        fertilizers,
        forcing,
        planting_date_fixed,
        weed_fraction,
        disabled,
        notes,
    )
)
