class PWMDecoder:
	def __init__(self, onTriggerLevel=0.05, lengths0=(61, 68), lengths1=(19, 24)):
		self.isOn = False
		self.onTime = 0

		self.onTriggerLevel = onTriggerLevel
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
			if sample > self.onTriggerLevel:
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
