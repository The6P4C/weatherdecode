from scipy.io import wavfile
from pwm import PWMDecoder
from bitstream import BitstreamDecoder
from packet import decode_packet

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
