from bitstream import BitstreamDecoder
from packet import decode_packet
from pwm import PWMDecoder

class Decoder:
	def __init__(self, print_on_times=False):
		self.pwm_decoder = PWMDecoder(print_on_times)
		self.bitstream_decoder = BitstreamDecoder()

	def add_samples(self, samples):
		bitstream = self.pwm_decoder.add_samples(samples)
		packet_data = self.bitstream_decoder.add_bits(bitstream)
		packets = [decode_packet(p) for p in packet_data]
		
		return packets
