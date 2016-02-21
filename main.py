import argparse
from bitstream import BitstreamDecoder
from packet import decode_packet
from pwm import PWMDecoder
import pyaudio
from scipy.io import wavfile
import struct
import warnings

def main():
	parser = argparse.ArgumentParser(description='Decode packets from the Maxkon 433MHz weather station.')
	parser.add_argument('--file')
	args = parser.parse_args()

	if (args.file):
		# Suppress WAV file warnings
		warnings.filterwarnings('ignore')
		sampFreq, samples = wavfile.read(args.file)
		warnings.filterwarnings('default')

		pwmDecoder = PWMDecoder()
		bitstreamDecoder = BitstreamDecoder()
		bitstream = pwmDecoder.add_samples(samples.tolist())
		packets = bitstreamDecoder.add_bits(bitstream)
		
		for packet in packets:
			print(decode_packet(packet))
	else:
		CHUNK = 1024
		FORMAT = pyaudio.paFloat32
		CHANNELS = 1
		RATE = 44100
		RECORD_SECONDS = 0.05

		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

		print('rec start')

		frames = []
		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
			data = stream.read(CHUNK)
			frames.append(data)

		print('rec end')

		stream.stop_stream()
		stream.close()
		p.terminate()

		for frame in frames:
			for float_bytes in [frame[i:i + 4] for i in range(0, len(frame), 4)]:
				print(struct.unpack('f', float_bytes)[0])

if __name__ == '__main__':
	main()
