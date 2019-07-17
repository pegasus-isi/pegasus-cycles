# -*- coding: utf-8 -*-
"""
Pegasus Cycles.

:license: Apache 2.0
"""

import logging
import sys
from pathlib import Path

import click

import pegasus_cycles
from pegasus_cycles._adag import *
from pegasus_cycles._combinations import itercombinations
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
    logging.info("Create transformation catalog")
    baseline_transformation()
    cycles_transformation()
    merge_transformation()
    visualize_transformation()

    logging.info("Generate weather grids")
    weather = set()
    for _lat, _lon in iterlocations(locations):
        xy = closest(_lat, _lon, elevation)
        if xy not in weather:
            gldas_to_cycles(_lat, _lon, xy)
            weather.add((_lat, _lon, xy))

    logging.info("Run Cycles")
    baseline()
    cycles()
    cycles_plus_10pct_nitrogen()
    merge()
    visualize()

    a.writeXML(out)
    click.secho(f"Success", fg="green")
