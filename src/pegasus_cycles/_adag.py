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

# Cycles' season output files list
season_files = {}
params_files = {}


@a.job()
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
    j.uses(File(output_file), Link.OUTPUT)
    return j


@a.transformation()
@a.resource_info(cpu=0.25)
def baseline_transformation():
    """Cycles Baseline Transformation."""
    e1 = Executable("cycles-baseline")
    return [e1]


@a.transformation()
@a.resource_info(cpu=0.25)
def cycles_transformation():
    """Cycles Transformation."""
    e1 = Executable("cycles")
    e1.addPFN(PFN("file://path/run", "a"))
    e2 = Executable("io.sh")
    e2.addPFN(PFN("file://path/io.sh", "a"))
    return [e1, e2]


@a.job()
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
        fertilizer_increase=False
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
    j.uses(File(weather_file), Link.INPUT)
    j.uses(crops_file, Link.INPUT)
    j.uses(soil_file, Link.INPUT)
    j.uses(template_weed, Link.INPUT)
    j.uses(template_ctrl, Link.INPUT)
    j.uses(template_op, Link.INPUT)
    j.uses(File(prefix + "cycles_crop-" + unique_id + ".dat"), Link.OUTPUT)
    j.uses(File(prefix + "cycles_nitrogen-" + unique_id + ".dat"), Link.OUTPUT)
    j.uses(season_output_file, Link.OUTPUT)
    j.uses(File(prefix + "cycles_soilProfile-" + unique_id + ".dat"), Link.OUTPUT)
    j.uses(File(prefix + "cycles_som-" + unique_id + ".dat"), Link.OUTPUT)
    j.uses(File(prefix + "cycles_summary-" + unique_id + ".dat"), Link.OUTPUT)
    j.uses(File(prefix + "cycles_water-" + unique_id + ".dat"), Link.OUTPUT)
    j.uses(File(prefix + "cycles_weatherOutput-" + unique_id + ".dat"), Link.OUTPUT)
    j.uses(File(prefix + "cycles_outputs-" + unique_id + ".zip"), Link.OUTPUT)
    j.uses(params_file, Link.OUTPUT)
    if not baseline:
        j.addArguments("--reinit-file", reinit_file)
        j.uses(File(reinit_file), Link.INPUT)
        if not fertilizer_increase:
            if crop not in season_files:
                season_files[crop] = []
                params_files[crop] = []
            season_files[crop].append(season_output_file)
            params_files[crop].append(params_file)
    else:
        j.uses(File(prefix + "cycles_reinit-" + unique_id + ".dat"), Link.OUTPUT)
    return j


@a.job()
def cycles_output_parser(crop):
    """Cycles Output Parser."""
    j = Job("cycles_output_parser")
    j.addProfile(Profile(Namespace.CONDOR, key="+SingularityImage", value=html.unescape("&quot;/cvmfs/singularity.opensciencegrid.org/mintproject/cycles:0.9.4-alpha&quot;")))
    output_file = File("cycles_output_summary_" + crop.lower() + ".csv")
    if crop not in season_files: # temp
        return
    for f in season_files[crop]:
        j.uses(f, Link.INPUT)
    for f in params_files[crop]:
        j.addArguments("-p", f)
        j.uses(f, Link.INPUT)
    j.uses(output_file, Link.OUTPUT)
    j.addArguments("--output-file", output_file)
    return j


@a.transformation()
@a.resource_info(cpu=0.25)
def merge_transformation():
    """Cycles Baseline Transformation."""
    e1 = Executable("merge")
    e1.addPFN(PFN("file://path/run", "a"))
    return e1


@a.job()
def merge():
    """Merge."""
    return Job("merge")


@a.transformation()
@a.resource_info(cpu=0.25)
def visualize_transformation():
    """Cycles Baseline Transformation."""
    e1 = Executable("visualize")
    e1.addPFN(PFN("file://path/run", "a"))
    return e1


@a.job()
def visualize():
    """Cycles Visualize."""
    return Job("visualize")
