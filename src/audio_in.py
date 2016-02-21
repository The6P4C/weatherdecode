import pyaudio
import struct

class AudioIn:
	def __init__(self, callback):
		def pa_callback(in_data, frame_count, time_info, status):
			floats = []
			for float_bytes in [in_data[i:i + 4] for i in range(0, len(in_data), 4)]:
		 		floats.append(struct.unpack('f', float_bytes)[0])

			callback(floats)

			return (in_data, pyaudio.paContinue)

		FORMAT = pyaudio.paFloat32
		CHANNELS = 1
		RATE = 44100

		self.p = pyaudio.PyAudio()

		self.stream = self.p.open(
			format=FORMAT,
			channels=CHANNELS,
			rate=RATE,
			input=True,
			stream_callback=pa_callback
		)

		self.stream.start_stream()

	def stop(self):
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()
