# -*- coding: utf-8 -*-
"""
Pegasus Cycles.

:license: Apache 2.0
"""
import sys

import click

import pegasus_cycles
from pegasus_cycles._adag import *
from pegasus_cycles._combinations import latitude, longitude


def _closest(lat, lon):
    pass


@click.group()
def cli():
    click.echo(f"pegasus-cycles v{pegasus_cycles.__version__}")


@cli.command()
@click.argument("out", type=click.File("w"), default=sys.stdout)
def dax(out=sys.stdout):
    click.secho(f"Generate DAX", fg="green")
    weather = set()
    for _lat, _lon in zip(latitude, longitude):
        xy = _closest(_lat, _lon)
        if xy not in weather:
            gldas_to_cycles(_lat, _lon)
            weather.add((_lat, _lon, xy))

    baseline()
    cycles()
    cycles_plus_10pct_nitrogen()
    merge()
    visualize()

    a.writeXML(out)
