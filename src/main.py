import argparse
from audio_in import AudioIn
import datetime
from decoder import Decoder
from scipy.io import wavfile
import warnings
import time

def print_packet(packet):	
	now = datetime.datetime.now()
	print('Recieved: %s' % (now.strftime('%Y-%m-%d %H:%M:%S')))

	if packet['crc_fail']:
		print('CRC Fail', flush=True)
	else:
		temperature = packet['temperature']
		humidity = packet['humidity']
		wind_direction = packet['wind_direction']

		print(u'\tTemperature: %d deg C' % (temperature))
		print('\tHumidity: %d%%' % (humidity))
		print('\tWind Direction: %s' % (wind_direction))
		print('', flush=True)

def main():
	parser = argparse.ArgumentParser(description='Decode packets from the Maxkon 433MHz weather station.')
	parser.add_argument('--file')
	args = parser.parse_args()

	decoder = Decoder()

	if (args.file):
		# Suppress WAV file warnings
		warnings.filterwarnings('ignore')
		sampFreq, samples = wavfile.read(args.file)
		warnings.filterwarnings('default')

		packets = decoder.add_samples(samples.tolist())
		for packet in packets:
			print_packet(packet)
	else:
		def audio_samples_ready(samples):
			packets = decoder.add_samples(samples)

			for packet in packets:
				print_packet(packet)

		audioIn = AudioIn(audio_samples_ready)

		while True:
			time.sleep(0.1)

if __name__ == '__main__':
	main()
