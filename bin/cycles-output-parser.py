#!/usr/bin/env python3
"""Cycles Output Parser."""

import argparse
import csv
import os

def parse_outputs(output_file, params_files, **kwargs):
    with open('output-summary.csv', 'w', newline='') as csvfile:
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
            'year',
            'yield',
            'forcing'
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
                        row[0][:4],
                        row[4],
                        params[8]
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
