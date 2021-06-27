#!/usr/bin/python3

import fastf1 as ff1
import pudb
import os

import argparse

# Parser logic
parser = argparse.ArgumentParser()
parser.add_argument("-y",
                    "--year",
                    default="2021",
                    type=int,
                    help="Session year")
parser.add_argument("-n",
                    "--number",
                    default="1",
                    type=int,
                    help="Session number")
parser.add_argument("-o",
                    "--output",
                    default='/tmp/F1/',
                    type=str,
                    help="Output directory for CSV files and Fast-F1 cache")
parser.add_argument("-r",
                    "--reload",
                    default=False,
                    type=bool,
                    help="Invalidate the current Fast-F1 cache data")
args = parser.parse_args()

output_dir = args.output
# Add trailing slash if missing
if output_dir[-1] != '/':
	output_dir += '/'
force_renew = args.reload
year = args.year
session_number = args.number

print(f'Loading data for session {session_number} of the {year} season...')
if force_renew:
	print('Ignoring previously cached data due to -r flag.')

if not os.path.isdir(output_dir):
    print(f'Output directory at {output_dir} does not exist, creating...')
    os.mkdir(output_dir)
else:
    print(f'Using existing output directory at {output_dir}.')

try:
    ff1.Cache.enable_cache(output_dir, force_renew=force_renew)

    output = ff1.get_session(year, session_number)
    race = output.get_race()
    telemetry = race.load_laps(with_telemetry=True)

    timing_data = ff1.api.timing_data(ff1.api.make_path(output.name, output.date, 'Race', race.date))
    laps_data = timing_data[0]
    stream_data = timing_data[1]

    print(f'Saving data to {output_dir}...')
    laps_data.to_csv(output_dir + f'export_laps_{output.name}_{output.date}_{race.date}_race.csv')
    stream_data.to_csv(output_dir + f'export_stream_{output.name}_{output.date}_{race.date}_race.csv')
    print("Done")
except Exception as ex:
    print(f'An error occurred: {ex}.')
    exit(1)
