# -*- coding: utf-8 -*-

from pegasus_cycles._pegasus import *

import os
import html

a = ADAG("pegasus-cycles", auto=True)

# input files
crops_file = File("crops.crop")
crops_file.addPFN(PFN("file://" + os.getcwd() + "/data/crops.crop", "local"))
soil_file = File("pongo.soil")
soil_file.addPFN(PFN("file://" + os.getcwd() + "/data/pongo.soil", "local"))
template_weed = File("template-weed.operation")
template_weed.addPFN(PFN("file://" + os.getcwd() + "/data/template-weed.operation", "local"))
template_ctrl = File("template.ctrl")
template_ctrl.addPFN(PFN("file://" + os.getcwd() + "/data/template.ctrl", "local"))
template_op = File("template.operation")
template_op.addPFN(PFN("file://" + os.getcwd() + "/data/template.operation", "local"))
a.addFile(crops_file)
a.addFile(soil_file)
a.addFile(template_weed)
a.addFile(template_ctrl)
a.addFile(template_op)

# Cycles' output files list
season_files = {}
params_files = {}
fi_files = {}


# @a.job()
def gldas_to_cycles(
    latitude,
    longitude,
    output_file,
    start_date="2000-01-01",
    end_date="2017-12-31",
    gldas_path="/raw-data/GLDAS",
):
    """Transform GLDAS to Cycles."""
    j = Job("gldas_to_cycles")
    j.addProfile(Profile(Namespace.CONDOR, key="+SingularityImage", value=html.unescape("&quot;/cvmfs/singularity.opensciencegrid.org/mintproject/cycles:0.9.4-alpha&quot;")))
    j.addArguments("--start-date", start_date)
    j.addArguments("--end-date", end_date)
    j.addArguments("--latitude", latitude)
    j.addArguments("--longitude", longitude)
    j.addArguments("--gldas-path", gldas_path)
    j.addArguments("--output", output_file)
    j.uses(File(output_file), link=Link.OUTPUT, transfer=True)
    return j


# @a.transformation()
# @a.resource_info(cpu=0.25)
# def baseline_transformation():
#     """Cycles Baseline Transformation."""
#     e1 = Executable("cycles-baseline")
#     return [e1]
#
#
# @a.transformation()
# @a.resource_info(cpu=0.25)
# def cycles_transformation():
#     """Cycles Transformation."""
#     e1 = Executable("cycles")
#     e1.addPFN(PFN("file://path/run", "a"))
#     e2 = Executable("io.sh")
#     e2.addPFN(PFN("file://path/io.sh", "a"))
#     return [e1, e2]


# @a.job()
def cycles(
        unique_id,
        crop,
        start_planting_date,
        end_planting_date,
        planting_date_fixed,
        fertilizer_rate,
        weed_fraction,
        forcing,
        weather_file,
        reinit_file=None,
        baseline=False,
        fertilizer_increase=False,
        weather=None
):
    """Cycles."""
    prefix = "baseline_" if baseline else "fertilizer_increase_" if fertilizer_increase else ""
    params_file = File(prefix + "cycles_params-" + unique_id + ".csv")
    season_output_file = File(prefix + "cycles_season-" + unique_id + ".dat")
    j = Job(prefix + "cycles")
    j.addProfile(Profile(Namespace.CONDOR, key="+SingularityImage", value=html.unescape("&quot;/cvmfs/singularity.opensciencegrid.org/mintproject/cycles:0.9.4-alpha&quot;")))
    j.addArguments("--baseline", str(baseline))
    j.addArguments("--fertilizer-increase", str(fertilizer_increase))
    j.addArguments("--id", unique_id)
    j.addArguments("--crop", crop)
    j.addArguments("--start-planting-date", start_planting_date)
    j.addArguments("--end-planting-date", end_planting_date)
    j.addArguments("--planting-date-fixed", planting_date_fixed)
    j.addArguments("--fertilizer-rate", fertilizer_rate)
    j.addArguments("--weed-fraction", weed_fraction)
    j.addArguments("--forcing", forcing)
    j.addArguments("--weather-file", weather_file)
    j.addArguments("--params-file", params_file)
    j.addArguments(crops_file)
    j.addArguments(soil_file)
    j.addArguments(template_weed)
    j.addArguments(template_ctrl)
    j.addArguments(template_op)
    j.uses(File(weather_file), link=Link.INPUT)
    j.uses(crops_file, link=Link.INPUT)
    j.uses(soil_file, link=Link.INPUT)
    j.uses(template_weed, link=Link.INPUT)
    j.uses(template_ctrl, link=Link.INPUT)
    j.uses(template_op, link=Link.INPUT)
    j.uses(File(prefix + "cycles_crop-" + unique_id + ".dat"), link=Link.OUTPUT, transfer=False)
    j.uses(File(prefix + "cycles_nitrogen-" + unique_id + ".dat"), link=Link.OUTPUT, transfer=False)
    j.uses(File(prefix + "cycles_soilProfile-" + unique_id + ".dat"), link=Link.OUTPUT, transfer=False)
    j.uses(File(prefix + "cycles_som-" + unique_id + ".dat"), link=Link.OUTPUT, transfer=False)
    j.uses(File(prefix + "cycles_summary-" + unique_id + ".dat"), link=Link.OUTPUT, transfer=False)
    j.uses(File(prefix + "cycles_water-" + unique_id + ".dat"), link=Link.OUTPUT, transfer=False)
    j.uses(File(prefix + "cycles_weatherOutput-" + unique_id + ".dat"), link=Link.OUTPUT, transfer=False)
    if not baseline:
        j.uses(season_output_file, link=Link.OUTPUT)
        j.uses(File(prefix + "cycles_outputs-" + unique_id + ".zip"), link=Link.OUTPUT)
        j.uses(params_file, link=Link.OUTPUT)
        j.addArguments("--reinit-file", reinit_file)
        j.uses(File(reinit_file), Link.INPUT)
        if not fertilizer_increase:
            if weather not in season_files:
                season_files[weather] = {}
                params_files[weather] = {}
            if crop not in season_files[weather]:
                season_files[weather][crop] = []
                params_files[weather][crop] = []
            season_files[weather][crop].append(season_output_file)
            params_files[weather][crop].append(params_file)
    else:
        j.uses(season_output_file, link=Link.OUTPUT, transfer=False)
        j.uses(File(prefix + "cycles_outputs-" + unique_id + ".zip"), link=Link.OUTPUT, transfer=False)
        j.uses(params_file, link=Link.OUTPUT, transfer=False)
        j.uses(File(prefix + "cycles_reinit-" + unique_id + ".dat"), link=Link.OUTPUT, transfer=False)
    return j


def cycles_fertilizer_increase_output_parser(
    unique_id,
    crop,
    weather=None
):
    """Cycles Fertilizer Increase Output Parser."""
    j = Job("cycles_fertilizer_increase_output_parser")
    j.addProfile(Profile(Namespace.CONDOR, key="+SingularityImage", value=html.unescape("&quot;/cvmfs/singularity.opensciencegrid.org/mintproject/cycles:0.9.4-alpha&quot;")))

    # input files
    params_file = File("cycles_params-" + unique_id + ".csv")
    params_file_fi = File("fertilizer_increase_cycles_params-" + unique_id + ".csv")
    season_file = File("cycles_season-" + unique_id + ".dat")
    season_file_fi = File("fertilizer_increase_cycles_season-" + unique_id + ".dat")
    j.addArguments("--params-file", params_file)
    j.addArguments("--params-file-fi", params_file_fi)
    j.addArguments("--season-file", season_file)
    j.addArguments("--season-file-fi", season_file_fi)
    j.uses(params_file, link=Link.INPUT)
    j.uses(params_file_fi, link=Link.INPUT)
    j.uses(season_file, link=Link.INPUT)
    j.uses(season_file_fi, link=Link.INPUT)

    # output file
    output_file = File("cycles_fertilizer_increase_output_parsed-" + unique_id + ".csv")
    j.addArguments("--output-file", output_file)
    j.uses(output_file, link=Link.OUTPUT, transfer=False)
    if weather not in fi_files:
        fi_files[weather] = {}
    if crop not in fi_files[weather]:
        fi_files[weather][crop] = []
    fi_files[weather][crop].append(output_file)

    return j


def cycles_fertilizer_increase_output_summary(weather, crop):
    """Cycles Output Summary."""
    if weather not in fi_files or crop not in fi_files[weather]: #temp
        return
    j = Job("cycles_fertilizer_increase_output_summary")
    j.addProfile(Profile(Namespace.CONDOR, key="+SingularityImage", value=html.unescape("&quot;/cvmfs/singularity.opensciencegrid.org/mintproject/cycles:0.9.4-alpha&quot;")))

    # inputs
    for f in fi_files[weather][crop]:
        j.addArguments("-p", f)
        j.uses(f, Link.INPUT)

    # output
    output_file = File("cycles_fi_output_summary_" + crop.lower() + "_" + weather[2].replace("met", "").replace(".weather", "") + ".csv")
    j.uses(output_file, link=Link.OUTPUT, transfer=True)
    j.addArguments("--output-file", output_file)
    return j


# @a.job()
def cycles_output_parser(weather, crop):
    """Cycles Output Parser."""
    if weather not in season_files or crop not in season_files[weather]: #temp
        return
    j = Job("cycles_output_parser")
    j.addProfile(Profile(Namespace.CONDOR, key="+SingularityImage", value=html.unescape("&quot;/cvmfs/singularity.opensciencegrid.org/mintproject/cycles:0.9.4-alpha&quot;")))
    output_file = File("cycles_output_summary_" + crop.lower() + "_" + weather[2].replace("met", "").replace(".weather", "") + ".csv")
    for f in season_files[weather][crop]:
        j.uses(f, Link.INPUT)
    for f in params_files[weather][crop]:
        j.addArguments("-p", f)
        j.uses(f, Link.INPUT)
    j.uses(output_file, link=Link.OUTPUT, transfer=True)
    j.addArguments("--output-file", output_file)
    return j


# @a.transformation()
# @a.resource_info(cpu=0.25)
# def merge_transformation():
#     """Cycles Baseline Transformation."""
#     e1 = Executable("merge")
#     e1.addPFN(PFN("file://path/run", "a"))
#     return e1
#
#
# @a.job()
# def merge():
#     """Merge."""
#     return Job("merge")
#
#
# @a.transformation()
# @a.resource_info(cpu=0.25)
# def visualize_transformation():
#     """Cycles Baseline Transformation."""
#     e1 = Executable("visualize")
#     e1.addPFN(PFN("file://path/run", "a"))
#     return e1
#
#
# @a.job()
# def visualize():
#     """Cycles Visualize."""
#     return Job("visualize")
