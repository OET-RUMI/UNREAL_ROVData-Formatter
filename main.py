import pandas as pd
import os

INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

# Timestamp,Longitude,Latitude,Depth,Conductivity,PressurePSI,SalinityPSU,SoundVelocityMS,TemperatureC,Heading,Pitch,Roll,OxygenUncompensatedConcentrationMicromolar,OxygenUncompensatedSaturationPercent,SealogEventText,SealogEventValue

HEADER_ALIASES = {
	'Timestamp': ['timestamp', 'time', 'date'],
	'Longitude': ['longitude', 'long', 'dvl_lon'],
	'Latitude': ['latitude', 'lat', 'dvl_lat'],
	'Depth': ['depth', 'paro_depth_m'],
	'Conductivity': ['conductivity', 'ctd_conductivity'],
	'PressurePSI': ['pressure', 'ctd_pressure_psi'],
	'SalinityPSU': ['salinity', 'ctd_salinity_psu'],
	'SoundVelocityMS': ['sound_velocity', 'ctd_sound_velocity_ms'],
	'TemperatureC': ['temperature', 'ctd_temp_c'],
	'Heading': ['heading', 'octans_heading'],
	'Pitch': ['pitch', 'octans_pitch'],
	'Roll': ['roll', 'octans_roll'],
	'OxygenUncompensatedConcentrationMicromolar': ['oxygenuncompensatedconcentrationmicromolar', 'oxygen_uncompensated_concentration_micromolar'],
	'OxygenUncompensatedSaturationPercent': ['oxygenuncompensatedsaturationpercent', 'oxygen_uncompensated_saturation_percent'],
	'SealogEventText': ['sealogeventtext', 'sealog_event_free_text'],
	'SealogEventValue': ['sealogeventvalue', 'sealog_event_value']
}

def read_data(file_path, delimiter):
	data = pd.read_csv(file_path, delimiter=delimiter)

	return data

# returns header used in headers that matches with key in HEADER_ALIASES
def get_header_alias(header, headers):
	for alias in HEADER_ALIASES[header]:
		if alias in headers:
			return alias

	return None

# converts from generic headers to headers matching HEADER_ALIASES keys
def process_data(input_data):
	headers = input_data.columns

	output_headers = [key for key in HEADER_ALIASES.keys()]
	output_data = pd.DataFrame(columns=output_headers)

	for header in output_headers:
		alias = get_header_alias(header, headers)
		if alias is not None:
			output_data[header] = input_data[alias]

	return output_data

def write_data(file_path, data, delimiter):
	data.to_csv(file_path, sep=delimiter, index=False)

def main():
	if not os.path.exists(OUTPUT_FOLDER):
		os.makedirs(OUTPUT_FOLDER)

	for file_name in os.listdir(INPUT_FOLDER):
		name, ext = os.path.splitext(file_name)

		delimiter = None
		if ext == '.csv':
			delimiter = ','
		elif ext == '.tsv':
			delimiter = '\t'

		if delimiter is None:
			continue

		input_data = read_data(os.path.join(INPUT_FOLDER, file_name), delimiter)
		output_data = process_data(input_data)

		write_data(os.path.join(OUTPUT_FOLDER, name + '_processed' + ext), output_data, ',')


if __name__ == '__main__':
	main()
