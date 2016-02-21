import argparse
from audio_in import AudioIn
from bitstream import BitstreamDecoder
from packet import decode_packet
from pwm import PWMDecoder
from scipy.io import wavfile
import warnings
import time

def main():
	parser = argparse.ArgumentParser(description='Decode packets from the Maxkon 433MHz weather station.')
	parser.add_argument('--file')
	args = parser.parse_args()

	pwmDecoder = PWMDecoder()
	bitstreamDecoder = BitstreamDecoder()

	if (args.file):
		# Suppress WAV file warnings
		warnings.filterwarnings('ignore')
		sampFreq, samples = wavfile.read(args.file)
		warnings.filterwarnings('default')
		
		bitstream = pwmDecoder.add_samples(samples.tolist())
		packets = bitstreamDecoder.add_bits(bitstream)
		
		for packet in packets:
			print(decode_packet(packet))
	else:
		def audio_samples_ready(samples):
			bitstream = pwmDecoder.add_samples(samples)
			packets = bitstreamDecoder.add_bits(bitstream)

			for packet in packets:
				print(decode_packet(packet), flush=True)

		audioIn = AudioIn(audio_samples_ready)

		while True:
			time.sleep(0.1)

if __name__ == '__main__':
	main()
