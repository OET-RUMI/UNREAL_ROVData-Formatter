import pandas as pd
from dateutil import parser
from datetime import datetime
import os

INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

HEADER_ALIASES = {
	'Row Name': ['row name', 'row', 'index'],
	'Timestamp': ['timestamp', 'time', 'date'],
	'Vehicle': ['vehicle'],
	'Longitude': ['longitude', 'long', 'kalman_long', 'dvl_lon'],
	'Latitude': ['latitude', 'lat', 'kalman_lat', 'dvl_lat'],
	'Depth': ['depth', 'paro_depth_m', 'kalman_depth'],
	'Conductivity': ['conductivity', 'ctd_conductivity'],
	'PressurePSI': ['pressure', 'ctd_pressure_psi'],
	'SalinityPSU': ['salinity', 'ctd_salinity_psu'],
	'SoundVelocityMS': ['sound_velocity', 'ctd_sound_velocity_ms'],
	'TemperatureC': ['temperature', 'ctd_temp_c'],
	'Heading': ['heading', 'octans_heading', 'heading_rad'],
	'Pitch': ['pitch', 'octans_pitch', 'kalman_pitch_deg'],
	'Roll': ['roll', 'octans_roll', 'kalman_roll_deg'],
	'OxygenUncompensatedConcentrationMicromolar': ['oxygenuncompensatedconcentrationmicromolar', 'oxygen_uncompensated_concentration_micromolar', 'o2_concentration'],
	'OxygenUncompensatedSaturationPercent': ['oxygenuncompensatedsaturationpercent', 'oxygen_uncompensated_saturation_percent', 'o2_saturation'],
	'SealogEventText': ['sealogeventtext', 'sealog_event_free_text', 'event_free_text'],
	'SealogEventValue': ['sealogeventvalue', 'sealog_event_value', 'event_value'],
	'SealogEventChannel': ['event_option.channel'],
	'SealogEventMilestone': ['event_option.milestone'],
	'SealogEventRating': ['event_option.rating'],
	'SealogEventVehicle': ['event_option.vehicle'],
	'Capture1': ['capture_1', 'vehicleRealtimeDualHDGrabData.camera_name_value'],
	'Capture2': ['capture_2', 'vehicleRealtimeDualHDGrabData.camera_name_2_value'],
	'Capture1ImagePath': ['capture_1_image_path', 'vehicleRealtimeDualHDGrabData.filename_value'],
	'Capture2ImagePath': ['capture_2_image_path', 'vehicleRealtimeDualHDGrabData.filename_2_value'],
}

def read_data(file_path, delimiter):
	data = pd.read_csv(file_path, delimiter=delimiter)

	return data

def get_header_alias(header, headers):
	headers_lower = [h.lower() for h in headers]

	for alias in HEADER_ALIASES[header]:
		if alias.lower() in headers_lower:
			return headers[headers_lower.index(alias.lower())]
	
	if header != 'Row Name':
		print(f'{header} not found in input data')
		
	return None

def correct_timestamp(timestamp):
	input_datetime = parser.parse(timestamp)
	output_datetime = input_datetime.strftime(TIMESTAMP_FORMAT)

	millisecond_portion = output_datetime.split('.')[1]
	millisecond_portion = millisecond_portion[3:] if len(millisecond_portion) > 3 else millisecond_portion
	output_datetime = output_datetime.split('.')[0] + '.' + millisecond_portion
	
	return output_datetime

def correct_depth(depth):
	return -abs(depth)

# converts from generic headers to headers matching HEADER_ALIASES keys
def process_data(input_data):
	headers = input_data.columns

	output_headers = [key for key in HEADER_ALIASES.keys()]
	output_data = pd.DataFrame(columns=output_headers)

	for header in output_headers:
		alias = get_header_alias(header, headers)

		if alias is not None:
			output_data[header] = input_data[alias]
		if alias is None and header == 'Row Name':
			output_data[header] = input_data.index
	
	if 'Timestamp' in output_headers:
		output_data['Timestamp'] = output_data['Timestamp'].apply(lambda x: correct_timestamp(x))

	if 'Depth' in output_headers:
		output_data['Depth'] = output_data['Depth'].apply(lambda x: correct_depth(x))

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

		print(f'Processing file: {file_name}')

		input_data = read_data(os.path.join(INPUT_FOLDER, file_name), delimiter)
		output_data = process_data(input_data)

		write_data(os.path.join(OUTPUT_FOLDER, name + '_processed' + ext), output_data, ',')


if __name__ == '__main__':
	main()
