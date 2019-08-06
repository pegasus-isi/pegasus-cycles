#!/usr/bin/env python3
"""Cycles Output Parser."""

import argparse
import csv
import os

def parse_outputs(output_file, params_files, **kwargs):
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
            'weed_fraction',
            'forcing'
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
            'n_concn_forage'
        ])

        for f in params_files:
            params = []
            with open(f) as params:
                reader = csv.reader(params, skipinitialspace=True, quotechar="'")
                for row in reader:
                    params = row.copy()

            with open(params[9]) as season_file:
                csvreader = csv.reader(season_file, delimiter='\t')
                next(csvreader)
                next(csvreader)
                for row in csvreader:
                    csvwriter.writerow([
                        params[0],
                        params[1],
                        params[2],
                        params[3],
                        params[4],
                        params[5],
                        params[6],
                        params[7],
                        params[8],
                        row[0][:4].strip(),
                        row[2].strip(),
                        row[3].strip(),
                        row[4].strip(),
                        row[5].strip(),
                        row[6].strip(),
                        row[7].strip(),
                        row[8].strip(),
                        row[9].strip(),
                        row[10].strip(),
                        ])


def _main():
    parser = argparse.ArgumentParser(
        description="Generate CSV file from Cycles Outputs."
    )
    parser.add_argument("-o", "--output-file", dest="output_file", default="output-summary.csv", help="Summary CSV file")
    parser.add_argument("-p", "--params-file", action="append", dest="params_files", help="Summary CSV file")
    args = parser.parse_args()
    parse_outputs(**vars(args))


if __name__ == "__main__":
    _main()
