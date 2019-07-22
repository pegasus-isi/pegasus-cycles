#!/usr/bin/env python3
"""Cycles Executor."""

import argparse
import logging
import os
import shutil
import subprocess
import sys
from string import Template

log = logging.getLogger()


def _generate_inputs(prefix, start_year, end_year, baseline, fertilizer_increase, unique_id, crop, start_planting_date, end_planting_date, planting_date_fixed, fertilizer_rate, weed_fraction, forcing, weather_file, reinit_file, crop_file, soil_file, template_weed, template_ctrl, template_op, **kwargs):
    os.mkdir("input")
    ctrl_file = prefix + "cycles_" + unique_id + ".ctrl"
    op_file = prefix + "cycles_" + unique_id + ".operation"
    shutil.copyfile(weather_file, "./input/" + weather_file)
    shutil.copyfile(crop_file, "./input/" + crop_file)
    shutil.copyfile(soil_file, "./input/" + soil_file)
    if reinit_file:
        shutil.copyfile(reinit_file, "./input/cycles.reinit")

    # process CTRL file
    with open(template_ctrl) as t_ctrl_file:
        src = Template(t_ctrl_file.read())
        ctrl_data = {
            "start_year": start_year,
            "end_year": end_year,
            "rotation_size": 1,
            "crop_file": crop_file,
            "operation_file": op_file,
            "soil_file": soil_file,
            "weather_file": weather_file,
            "reinit": 0 if baseline == "True" else 1,
        }
        result = src.substitute(ctrl_data)
        with open("./input/" + ctrl_file, "w") as f:
            f.write(result)

    # process Operation file
    operation_contents = ""
    with open(template_op) as t_op_file:
        src = Template(t_op_file.read())
        op_data = {
            "year_count": 1,
            "crop_name": crop,
            "fertilization_date": int(start_planting_date) - 10,
            "fertilization_rate": fertilizer_rate,
            "start_planting_date": start_planting_date,
            "end_planting_date": end_planting_date,
            "tillage_date": int(start_planting_date) + 20,
        }
        if fertilizer_increase == "True":
            op_data["fertilization_rate"] = float(op_data["fertilization_rate"]) * 1.1
        result = src.substitute(op_data)
        operation_contents += result + "\n"

        # handling weeds
        if float(weed_fraction) > 0:
            with open(template_weed) as t_wd_file:
                wd_src = Template(t_wd_file.read())
                wd_data = {
                    "year_count": 1,
                    "weed_planting_date": int(start_planting_date) + 7,
                    "weed_fraction": weed_fraction
                }
                wd_result = wd_src.substitute(wd_data)
                operation_contents += wd_result + "\n"

    # writing operations file
    with open("./input/" + op_file, "w") as f:
        f.write(operation_contents)


def _launch(prefix, baseline, unique_id, **kwargs):
    cmd = "Cycles -s -l 1 " + prefix + "cycles_" + unique_id if baseline == "True" else "Cycles " + prefix + "cycles_" + unique_id
    try:
        output = subprocess.check_output(
            cmd, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    except subprocess.CalledProcessError as exc:
        print("Status : FAIL", exc.returncode, exc.output)
        exit(1)
    else:
        print("Output: \n{}\n".format(output))



def _prepare_outputs(prefix, baseline, fertilizer_increase, unique_id, crop, **kwargs):
    shutil.copyfile("./output/" + prefix + "cycles_" + unique_id + "/annualSoilProfileC.dat", prefix + "cycles_soilProfile-" + unique_id + ".dat")
    shutil.copyfile("./output/" + prefix + "cycles_" + unique_id + "/annualSOM.dat", prefix + "cycles_som-" + unique_id + ".dat")
    shutil.copyfile("./output/" + prefix + "cycles_" + unique_id + "/N.dat", prefix + "cycles_nitrogen-" + unique_id + ".dat")
    shutil.copyfile("./output/" + prefix + "cycles_" + unique_id + "/season.dat", prefix + "cycles_season-" + unique_id + ".dat")
    shutil.copyfile("./output/" + prefix + "cycles_" + unique_id + "/summary.dat", prefix + "cycles_summary-" + unique_id + ".dat")
    shutil.copyfile("./output/" + prefix + "cycles_" + unique_id + "/weather.dat", prefix + "cycles_weatherOutput-" + unique_id + ".dat")
    shutil.copyfile("./output/" + prefix + "cycles_" + unique_id + "/water.dat", prefix + "cycles_water-" + unique_id + ".dat")
    shutil.copyfile("./output/" + prefix + "cycles_" + unique_id + "/" + crop + ".dat", prefix + "cycles_crop-" + unique_id + ".dat")
    if baseline == "True":
        shutil.copyfile("./output/" + prefix + "cycles_" + unique_id + "/reinit.dat", prefix + "cycles_reinit-" + unique_id + ".dat")

    # generate zip for input/output folder
    os.mkdir(prefix + "cycles_" + unique_id)
    shutil.move("input", prefix + "cycles_" + unique_id + "/input")
    shutil.move("output", prefix + "cycles_" + unique_id + "/output")
    shutil.make_archive(prefix + "cycles_outputs-" + unique_id, 'zip', prefix + "cycles_" + unique_id)


def _main():
    parser = argparse.ArgumentParser(
        description="Cycles executor."
    )
    parser.add_argument("--start-year", dest="start_year", default=2000, help="Simulation start year")
    parser.add_argument("--end-year", dest="end_year", default=2017, help="Simulation end year")
    parser.add_argument("-b", "--baseline", dest="baseline", default=False, help="Whether this is a baseline execution")
    parser.add_argument("-x", "--fertilizer-increase", dest="fertilizer_increase", default=False, help="Whether this is an execution with increased fertilizer")
    parser.add_argument("-i", "--id", dest="unique_id", default=None, help="Unique ID")
    parser.add_argument("-c", "--crop", dest="crop", default="Maize", help="Crop name")
    parser.add_argument("-s", "--start-planting-date", dest="start_planting_date", default=100, help="Start planting date")
    parser.add_argument("-e", "--end-planting-date", dest="end_planting_date", default=149, help="End planting date")
    parser.add_argument("-p", "--planting-date-fixed", dest="planting_date_fixed", default=True, help="Whether the planting data is fixed")
    parser.add_argument("-n", "--fertilizer-rate", dest="fertilizer_rate", default=0.00, help="Fertilizer rate")
    parser.add_argument("-w", "--weed-fraction", dest="weed_fraction", default=0.0, help="Weed fraction")
    parser.add_argument("-f", "--forcing", dest="forcing", default=False, help="Whether it uses forcing data from PIHM")
    parser.add_argument("-l", "--weather-file", dest="weather_file", default=None, help="Weather file")
    parser.add_argument("-r", "--reinit-file", dest="reinit_file", default=None, help="Cycles reinitialization file")
    parser.add_argument("crop_file", help="crops file")
    parser.add_argument("soil_file", help="Soil file")
    parser.add_argument("template_weed", help="Template weed file")
    parser.add_argument("template_ctrl", help="Template control file")
    parser.add_argument("template_op", help="Template operation file")
    args = parser.parse_args()

    if args.baseline == "True" and args.fertilizer_increase == "True":
        log.error("Error: Cannot run baseline with increased fertilizer")
        exit(1)

    # set end planting date if fixed
    if args.planting_date_fixed:
         args.end_planting_date = -999

    # setting prefix
    prefix = "baseline_" if args.baseline == "True" else "fertilizer_increase_" if args.fertilizer_increase == "True" else ""

    _generate_inputs(prefix, **vars(args))
    _launch(prefix, **vars(args))
    _prepare_outputs(prefix, **vars(args))

if __name__ == "__main__":
    _main()
