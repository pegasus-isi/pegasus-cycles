#!/usr/bin/env python3
"""Cycles Output Parser."""

import argparse
import csv
import os

def parse_outputs(params_file, params_file_fi, season_file, season_file_fi, output_file, **kwargs):
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

        params = []
        params_fi = []

        with open(params_file) as f:
            reader = csv.reader(f, skipinitialspace=True, quotechar="'")
            for row in reader:
                params = row.copy()

        with open(params_file_fi) as fi:
            reader = csv.reader(fi, skipinitialspace=True, quotechar="'")
            for row in reader:
                params_fi = row.copy()

        values = {}

        with open(season_file) as s:
            csvreader = csv.reader(s, delimiter='\t')
            next(csvreader)
            next(csvreader)
            for row in csvreader:
                year = row[0][:4].strip()
                values[year] = []
                values[year].append(row[2].strip())
                values[year].append(row[3].strip())
                values[year].append(row[4].strip())
                values[year].append(row[5].strip())
                values[year].append(row[6].strip())
                values[year].append(row[7].strip())
                values[year].append(row[8].strip())
                values[year].append(row[9].strip())
                values[year].append(row[10].strip())
                values[year].append(row[11].strip())
                values[year].append(row[12].strip())
                values[year].append(row[13].strip())
                values[year].append(row[14].strip())
                values[year].append(row[15].strip())
                values[year].append(row[16].strip())
                values[year].append(row[17].strip())
                values[year].append(row[18].strip())

        with open(season_file_fi) as s:
            csvreader = csv.reader(s, delimiter='\t')
            next(csvreader)
            next(csvreader)
            for row in csvreader:
                year = row[0][:4].strip()
                values[year].append(row[2].strip())
                values[year].append(row[3].strip())
                values[year].append(row[4].strip())
                values[year].append(row[5].strip())
                values[year].append(row[6].strip())
                values[year].append(row[7].strip())
                values[year].append(row[8].strip())
                values[year].append(row[9].strip())
                values[year].append(row[10].strip())
                values[year].append(row[11].strip())
                values[year].append(row[12].strip())
                values[year].append(row[13].strip())
                values[year].append(row[14].strip())
                values[year].append(row[15].strip())
                values[year].append(row[16].strip())
                values[year].append(row[17].strip())
                values[year].append(row[18].strip())

        for y in values:
            csvwriter.writerow([
                params[0],
                params[1],
                params[2],
                params[3],
                params[4],
                params[5],
                params[6],
                params_fi[6],
                params[7],
                params[8],
                y,
                values[y][0],
                values[y][1],
                values[y][2],
                values[y][3],
                values[y][4],
                values[y][5],
                values[y][6],
                values[y][7],
                values[y][8],
                values[y][9],
                values[y][10],
                values[y][11],
                values[y][12],
                values[y][13],
                values[y][14],
                values[y][15],
                values[y][16],
                values[y][17],
                values[y][18],
                values[y][19],
                values[y][20],
                values[y][21],
                values[y][22],
                values[y][23],
                values[y][24],
                values[y][25],
                values[y][26],
                values[y][27],
                values[y][28],
                values[y][29],
                values[y][30],
                values[y][31],
                values[y][32],
                values[y][33]
                ])


def _main():
    parser = argparse.ArgumentParser(
        description="Generate CSV file from Cycles Outputs."
    )
    parser.add_argument("-p", "--params-file", dest="params_file", default="cycles_params.csv", help="Params file for Cycles run")
    parser.add_argument("-i", "--params-file-fi", dest="params_file_fi", default="fertilizer_increase_cycles_params.csv", help="Params file for Cycles run with increased fertilizer rate")
    parser.add_argument("-s", "--season-file", dest="season_file", default="cycles_season.dat", help="Season file for Cycles run")
    parser.add_argument("-f", "--season-file-fi", dest="season_file_fi", default="fertilizer_increase_cycles_season.csv", help="Season file for Cycles run with increased fertilizer rate")
    parser.add_argument("-o", "--output-file", dest="output_file", default="output-summary.csv", help="Summary CSV file")

    args = parser.parse_args()
    parse_outputs(**vars(args))


if __name__ == "__main__":
    _main()
