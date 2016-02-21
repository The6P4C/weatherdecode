from scipy.io import wavfile
from pwm import PWMDecoder
from bitstream import BitstreamDecoder

def decode_packet(packet):
	COMPASS_DIRECTIONS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

	return {
		'temperature': 0.1 * packet[3] + 11.2,
		'humidity': packet[4],
		'wind_direction': COMPASS_DIRECTIONS[packet[9]]
	}

def main():
	sampFreq, samples = wavfile.read('demo/packet.wav')

	pwmDecoder = PWMDecoder()
	bitstreamDecoder = BitstreamDecoder()
	bitstream = pwmDecoder.add_samples(samples.tolist())
	packets = bitstreamDecoder.add_bits(bitstream)
	
	for packet in packets:
		print(decode_packet(packet))

if __name__ == '__main__':
	main()
