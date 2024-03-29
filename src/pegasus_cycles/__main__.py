# -*- coding: utf-8 -*-
"""
Pegasus Cycles.

:license: Apache 2.0
"""

import click
import hashlib
import logging
import pegasus_cycles
import os
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
    subwf_dir = "subwfs"
    os.mkdir(subwf_dir)
    prev_subwf_job = None

    for _lat, _lon in iterlocations(locations):
        xy = closest(_lat, _lon, elevation)
        if xy not in weather:
            _w = (_lat, _lon, xy)
            weather.add(_w)
            # GLDAS to Cycles job
            gldas_job = gldas_to_cycles(_lat, _lon, xy)
            a.addJob(gldas_job)

            # generate subworkflow per location
            logging.info("Generating subworkflows")

            subwf_id = "subwf_" + _w[2].replace("met", "").replace(".weather", "").replace(".", "_")
            subwf = ADAG(subwf_id)

            # Cycles jobs
            for _row in itercombinations([_w]):
                fertilizers = _row[7]
                coordinates = _row[2]
                id = "_".join([_row[1], _row[4], _row[5], _row[9], fertilizers[1], _row[10], _row[8], coordinates[2]])
                unique_id = hashlib.md5(id.encode('utf-8')).hexdigest()
                reinit_file = "baseline_cycles_reinit-" + unique_id + ".dat"
                # baseline job
                subwf.addJob(cycles(
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
                    weather=_row[2]
                ))
                # cycles job
                subwf.addJob(cycles(
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
                    fertilizer_increase=False,
                    weather=_row[2]
                ))
                # fertilizer increase job
                if _row[1] != "Peanut":
                    subwf.addJob(cycles(
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
                        fertilizer_increase=True,
                        weather=_row[2]
                    ))
                    subwf.addJob(cycles_fertilizer_increase_output_parser(
                        unique_id=unique_id,
                        crop=_row[1],
                        weather=_row[2]
                    ))

            # Cycles output parser job
            for crop in crops:
                subwf.addJob(cycles_output_parser(_w, crop))
                subwf.addJob(cycles_fertilizer_increase_output_summary(_w, crop))
            subwf.addJob(cycles_output_parser(_w, "Peanut"))

            # write subworkflow DAX file
            with open(subwf_dir + "/" + subwf_id + ".xml", "w") as subwf_out:
                subwf.writeXML(subwf_out)

            subwf_dax = File(subwf_id + ".xml")
            subwf_dax.addPFN(PFN("file://" + os.getcwd() + "/" + subwf_dir + "/" + subwf_id + ".xml", "local"))
            a.addFile(subwf_dax)

            subwf_job = DAX(subwf_id + ".xml", id=subwf_id)
            subwf_job.addProfile(Profile("dagman", "CATEGORY", "subwf"))
            subwf_job.uses(File(xy), Link.INPUT)
            subwf_job.uses(subwf_dax)
            subwf_job.addArguments("-Dpegasus.catalog.site.file=" + os.getcwd() + "/sites.xml",
                         "--sites", "condor_pool",
                         "--output-site", "local",
                         "--cluster", "horizontal",
                         "--cleanup", "inplace")
            a.addDAX(subwf_job)
            a.depends(parent=gldas_job, child=subwf_job)

            # add depenency for previous subworkflow
            # if prev_subwf_job:
            #     a.depends(parent=prev_subwf_job, child=subwf_job)
            prev_subwf_job = subwf_job


    # write top level DAX
    a.writeXML(out)
    click.secho(f"Success", fg="green")
