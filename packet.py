def decode_packet(packet):
	COMPASS_DIRECTIONS = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

	return {
		'temperature': 0.1 * packet[3] + 11.2,
		'humidity': packet[4],
		'wind_direction': COMPASS_DIRECTIONS[packet[9]]
	}
