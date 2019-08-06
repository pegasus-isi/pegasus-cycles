# -*- coding: utf-8 -*-
"""
Pegasus Cycles.

:license: Apache 2.0
"""

import click
import hashlib
import logging
import pegasus_cycles
import sys

from pathlib import Path
from pegasus_cycles._adag import *
from pegasus_cycles._combinations import itercombinations
from pegasus_cycles._combinations import crops
from pegasus_cycles._gldas import closest, iterlocations


@click.group()
@click.option("--verbose", "-v", default=0, count=True)
def cli(verbose):
    logging.basicConfig()


@cli.command()
def version():
    click.echo(f"{Path(sys.argv[0]).name} v{pegasus_cycles.__version__}")


@cli.command()
@click.option(
    "--locations",
    "-l",
    type=click.Path(file_okay=True, dir_okay=False, readable=True),
    required=True,
)
@click.option(
    "--elevation",
    "-e",
    type=click.Path(file_okay=True, dir_okay=False, readable=True),
    required=True,
)
@click.argument("out", type=click.File("w"), default=sys.stdout)
def dax(locations, elevation, out=sys.stdout):
    logging.info("Generate weather grids")
    weather = set()
    for _lat, _lon in iterlocations(locations):
        xy = closest(_lat, _lon, elevation)
        if xy not in weather:
            gldas_to_cycles(_lat, _lon, xy)
            weather.add((_lat, _lon, xy))

    count = 0
    logging.info("Run Cycles")
    for _row in itercombinations(weather):
        fertilizers = _row[7]
        coordinates = _row[2]
        id = "_".join([_row[1], _row[4], _row[5], _row[9], fertilizers[1], _row[10], _row[8], coordinates[2]])
        unique_id = hashlib.md5(id.encode('utf-8')).hexdigest()
        reinit_file = "baseline_cycles_reinit-" + unique_id + ".dat"
        cycles(
            unique_id=unique_id,
            crop=_row[1],
            start_planting_date=_row[4],
            end_planting_date=_row[5],
            planting_date_fixed=_row[9],
            fertilizer_rate=fertilizers[1],
            weed_fraction=_row[10],
            forcing=_row[8],
            weather_file=coordinates[2],
            reinit_file=None,
            baseline=True,
            fertilizer_increase=False,
        )
        cycles(
            unique_id=unique_id,
            crop=_row[1],
            start_planting_date=_row[4],
            end_planting_date=_row[5],
            planting_date_fixed=_row[9],
            fertilizer_rate=fertilizers[1],
            weed_fraction=_row[10],
            forcing=_row[8],
            weather_file=coordinates[2],
            reinit_file=reinit_file,
            baseline=False,
            fertilizer_increase=False
        )
        cycles(
            unique_id=unique_id,
            crop=_row[1],
            start_planting_date=_row[4],
            end_planting_date=_row[5],
            planting_date_fixed=_row[9],
            fertilizer_rate=fertilizers[1],
            weed_fraction=_row[10],
            forcing=_row[8],
            weather_file=coordinates[2],
            reinit_file=reinit_file,
            baseline=False,
            fertilizer_increase=True
        )
        count += 1
        # if count == 2:
        #     break

        # merge()
        # visualize()

    for crop in crops:
        cycles_output_parser(crop)

    a.writeXML(out)
    click.secho(f"Success", fg="green")
