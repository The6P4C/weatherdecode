class PWMDecoder:
	def __init__(self, print_on_times=False, on_trigger_level=0.05, lengths0=(61, 68), lengths1=(19, 24)):
		self.is_on = False
		self.on_time = 0

		self.print_on_times = print_on_times
		self.on_trigger_level = on_trigger_level
		self.lengths0 = lengths0
		self.lengths1 = lengths1

	def classify(self, on_time):
		if self.print_on_times:
			print('On Time: %d' % (on_time), flush=True)
		if on_time >= self.lengths0[0] and on_time <= self.lengths0[1]:
			return 0
		elif on_time >= self.lengths1[0] and on_time <= self.lengths1[1]:
			return 1
		else:
			return None;

	def add_samples(self, samples):
		bitstream = []
		for sample in samples:
			if sample > self.on_trigger_level:
				if self.is_on:
					self.on_time += 1
				else:
					self.is_on = True
					self.on_time = 1
			elif self.is_on:
				self.is_on = False
				
				bit_value = self.classify(self.on_time)
				if bit_value != None:
					bitstream.append(bit_value)
		return bitstream
