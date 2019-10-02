#!/usr/bin/env python3
"""Cycles Fertilizer Increase Output Summary."""

import argparse
import csv
import os

def parse_outputs(output_file, parsed_files, **kwargs):
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([
            'unique_id',
            'crop',
            'location',
            'planting_date',
            'end_planting_date',
            'planting_date_fixed',
            'nitrogen_rate',
            'increased_nitrogen_rate',
            'weed_fraction',
            'forcing',
            'year',
            'total_biomass',
            'root_biomass',
            'grain_yield',
            'forage_yield',
            'ag_residue',
            'harvest_index',
            'potential_tr',
            'actual_tr',
            'soil_evap',
            'total_n',
            'root_n',
            'grain_n',
            'forage_n',
            'cum_n_stress',
            'n_in_harvest',
            'n_in_residue',
            'n_concn_forage',
            'increased_total_biomass',
            'increased_root_biomass',
            'increased_grain_yield',
            'increased_forage_yield',
            'increased_ag_residue',
            'increased_harvest_index',
            'increased_potential_tr',
            'increased_actual_tr',
            'increased_soil_evap',
            'increased_total_n',
            'increased_root_n',
            'increased_grain_n',
            'increased_forage_n',
            'increased_cum_n_stress',
            'increased_n_in_harvest',
            'increased_n_in_residue',
            'increased_n_concn_forage'
        ])

        for f in parsed_files:
            params = []
            with open(f) as parsed_file:
                reader = csv.reader(parsed_file, skipinitialspace=True, quotechar="'")
                next(reader)
                for row in reader:
                    csvwriter.writerow(row)


def _main():
    parser = argparse.ArgumentParser(
        description="Generate CSV file from Cycles Fertilizer Increase Outputs."
    )
    parser.add_argument("-o", "--output-file", dest="output_file", default="output-fi-summary.csv", help="Summary CSV file")
    parser.add_argument("-p", "--parsed-file", action="append", dest="parsed_files", help="List of parsed season files")
    args = parser.parse_args()
    parse_outputs(**vars(args))


if __name__ == "__main__":
    _main()
