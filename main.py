import collections
import crcmod
from scipy.io import wavfile

class PWMDecoder:
	def __init__(self, lengths0 = (61, 65), lengths1 = (19, 24)):
		self.isOn = False
		self.onTime = 0

		self.lengths0 = lengths0
		self.lengths1 = lengths1

	def classify(self, onTime):
		if onTime >= self.lengths0[0] and onTime <= self.lengths0[1]:
			return 0
		elif onTime >= self.lengths1[0] and onTime <= self.lengths1[1]:
			return 1
		else:
			return None;

	def add_samples(self, samples):
		bitstream = []
		for sample in samples:
			if sample > 0.05:
				if self.isOn:
					self.onTime += 1
				else:
					self.isOn = True
					self.onTime = 1
			elif self.isOn:
				self.isOn = False
				
				bitValue = self.classify(self.onTime)
				if bitValue != None:
					bitstream.append(bitValue)
		return bitstream

def bitstream_to_bytes(l):
	if len(l) % 8 != 0:
		assert ValueError("List is not of length divisible by 8 (cannot be made into bytes)")

	output = []
	# from [... * 16] to [[... * 8], [... * 8]]
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
		self.crcFunction = crcmod.mkCrcFun(0x10F00)

	def check_packet(self, packet_bytes):
		if packet_bytes[0] != 0xFF:
			return False

		# could check CRC, but nah

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

def main():
	sampFreq, samples = wavfile.read('demo/packet.wav')

	pwmDecoder = PWMDecoder()
	bitstreamDecoder = BitstreamDecoder()
	bitstream = pwmDecoder.add_samples(samples.tolist())
	packets = bitstreamDecoder.add_bits(bitstream)
	print(packets)

if __name__ == '__main__':
	main()
