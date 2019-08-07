# -*- coding: utf-8 -*-

from itertools import product

country = ["South Sudan"]

# "Cassava"
# crops = ["Maize", "Sorghum", "Peanut", "Sesame", "Cassava"]
crops = ["Maize", "Sorghum"]

soil = ["pongo.soil"]

start_planting_date = ["100", "107", "114", "121", "128", "135", "142"]

end_planting_date = ["149"]

planting_date_fixed = ["True", "False"]

fertilizer = ["urea"]

nitrogen_rate = ["0", "25", "50", "100", "200", "400"]

fertilizer_rate = ["0.00", "78.13", "156.25", "312.50", "625.00", "1250.00"]

# forcing = ["True", "False"]
forcing = ["False"]

weed_fraction = ["0.0", "0.05", "0.1", "0.2", "0.4", "1.5", "2.0"]


def itercombinations(distinct_locations):
    # dot product for fertilizers
    fertilizers = zip(nitrogen_rate, fertilizer_rate)
    
    for row in list(
        product(
            country,
            crops,
            distinct_locations,
            soil,
            start_planting_date,
            end_planting_date,
            fertilizer,
            fertilizers,
            forcing,
            planting_date_fixed,
            weed_fraction,
        )
    ):
        yield row
