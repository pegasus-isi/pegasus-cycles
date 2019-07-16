# -*- coding: utf-8 -*-

import csv
import io
from pathlib import Path

import numpy as np
from netCDF4 import Dataset


def iterlocations(location_file):
    # X is Longitude, Y is Latitude.
    with Path(location_file).open("r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            yield row["LATITUDE"], row["LONGITUDE"]


def closest(lat, lon, elevation):
    nc = Dataset(elevation, "r")

    best_y = (np.abs(nc.variables["lat"][:] - float(lat))).argmin()
    best_x = (np.abs(nc.variables["lon"][:] - float(lon))).argmin()
    grid_lat = nc["lat"][best_y]
    grid_lon = nc["lon"][best_x]
    elevation = nc["GLDAS_elevation"][0, best_y, best_x]

    if grid_lat < 0.0:
        lat_str = "%.2fS" % (abs(grid_lat))
    else:
        lat_str = "%.2fN" % (abs(grid_lat))

    if grid_lon < 0.0:
        lon_str = "%.2fW" % (abs(grid_lon))
    else:
        lon_str = "%.2fE" % (abs(grid_lon))

    fname = "met" + lat_str + "x" + lon_str + ".weather"

    return lat, lon, fname
