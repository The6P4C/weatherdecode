import argparse
from audio_in import AudioIn
import datetime
from decoder import Decoder
from scipy.io import wavfile
import warnings
import time

def print_packet(packet, show_raw):	
	now = datetime.datetime.now()
	print('Recieved: %s' % (now.strftime('%Y-%m-%d %H:%M:%S')))

	if packet['crc_fail']:
		print('CRC Fail', flush=True)
	else:
		temperature = packet['temperature']
		humidity = packet['humidity']
		wind_direction = packet['wind_direction']
		raw_data = ''

		for byte in packet['raw_data']:
			hexVal = hex(byte)[2:]
			paddedHexVal = hexVal.rjust(2, '0')

			raw_data += paddedHexVal + ' '

		print(u'\tTemperature: %d deg C' % (temperature))
		print('\tHumidity: %d%%' % (humidity))
		print('\tWind Direction: %s' % (wind_direction))
		print('\tRaw Data: %s' % (raw_data))
		print('', flush=True)

def main():
	parser = argparse.ArgumentParser(description='Decode packets from the Maxkon 433MHz weather station.')
	parser.add_argument('--file', '-f', help='Decode packets from a WAV file')
	parser.add_argument('--show-raw', '-r', action='store_true', help='Show raw packet data in hexidecimal')
	args = parser.parse_args()

	decoder = Decoder()

	if (args.file):
		# Suppress WAV file warnings
		warnings.filterwarnings('ignore')
		sampFreq, samples = wavfile.read(args.file)
		warnings.filterwarnings('default')

		packets = decoder.add_samples(samples.tolist())
		for packet in packets:
			print_packet(packet, args.show_raw)
	else:
		def audio_samples_ready(samples):
			packets = decoder.add_samples(samples)

			for packet in packets:
				print_packet(packet, args.show_raw)

		audioIn = AudioIn(audio_samples_ready)

		while True:
			time.sleep(0.1)

if __name__ == '__main__':
	main()
