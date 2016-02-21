from scipy.io import wavfile

class PWMDecoder:
	def __init__(self, lengths0 = (61, 65), lengths1 = (19, 24)):
		self.isOn = False
		self.onTime = 0
		self.bitstream = []

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
					self.bitstream.append(bitValue)

def main():
	sampFreq, samples = wavfile.read('demo/packet.wav')

	decoder = PWMDecoder()
	decoder.add_samples(samples.tolist())
	print(decoder.bitstream)

if __name__ == '__main__':
	main()
