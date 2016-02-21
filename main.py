import argparse
from scipy.io import wavfile
from pwm import PWMDecoder
from bitstream import BitstreamDecoder
from packet import decode_packet
import warnings

def main():
	parser = argparse.ArgumentParser(description='Decode packets from the Maxkon 433MHz weather station.')
	parser.add_argument('--file')
	args = parser.parse_args()

	if (args.file):
		# Suppress WAV file warnings
		warnings.filterwarnings("ignore")
		sampFreq, samples = wavfile.read(args.file)
		warnings.filterwarnings("default")

		pwmDecoder = PWMDecoder()
		bitstreamDecoder = BitstreamDecoder()
		bitstream = pwmDecoder.add_samples(samples.tolist())
		packets = bitstreamDecoder.add_bits(bitstream)
		
		for packet in packets:
			print(decode_packet(packet))
	else:
		print("Not implemented; must load file")

if __name__ == '__main__':
	main()
