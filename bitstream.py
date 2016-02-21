import collections

def bitstream_to_bytes(l):
	if len(l) % 8 != 0:
		assert ValueError('List is not of length divisible by 8 (cannot be made into bytes)')

	output = []
	# From [... * 16] to [[... * 8], [... * 8]]
	bytes_bits = [l[i:i + 8] for i in range(0, len(l), 8)]
	for byte_bits in bytes_bits:
		val = 0
		for i in range(0, len(byte_bits)):
			if byte_bits[i]:
				val += 1 << (len(byte_bits) - 1 - i)
		output.append(val)
	return output


class BitstreamDecoder:
	def __init__(self):
		# 11 bytes of 8 bits each
		self.deque = collections.deque(maxlen=8 * 11)

	def check_packet(self, packet_bytes):
		if packet_bytes[0] != 0xFF:
			return False

		return True

	def add_bits(self, bitstream):
		packets = []
		for bit in bitstream:
			self.deque.append(bit)
			if len(self.deque) == self.deque.maxlen:
				packet_bytes = bitstream_to_bytes(list(self.deque))
				is_packet_good = self.check_packet(packet_bytes)
				if is_packet_good:
					packets.append(packet_bytes)
					self.deque.clear()
		return packets
