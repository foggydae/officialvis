class config():
	# default official: the official to display when openning the page
	DEFAULT_OFFICIAL = "习近平"

	# use geocode of 中南海 to encode `中央`
	CENTRAL_LAT = 39.9113
	CENTRAL_LON = 116.3805

	# arbitary chosen geocode for missing location
	UNKNOWN_LAT = 0
	UNKNOWN_LON = 0

	# dictionary for rank
	RANK_MAP = {
		"正国级": 10,
		"副国级": 9,
		"正大军区级": 10,
		"副大军区级": 9,
		"正部级、正军级": 8,
		"副部级、副军级": 7,
		"正厅级、正师级": 6,
		"副厅级、副师级": 5,
		"正处级、正团级": 4,
		"副处级、副团级": 3,
		"正科级、正营级": 2,
		"副科级、副营级": 1,
		"": 0
	}

	# dictionary for degree
	DEGREE_MAP = {
		"专科": -1,
		"本科": -2,
		"硕士": -3,
		"博士": -4,
		"培训": -5,
		"NA": 0
	}

	AXIS_TICKS = [
		"培训",			# -5
		"博士",			# -4
		"硕士",			# -3
		"本科",			# -2
		"专科",			# -1
		"-",			#  0
		"副科/营级",		#  1
		"正科/营级",		#  2
		"副处/团级",		#  3
		"正处/团级",		#  4
		"副厅/师级",		#  5
		"正厅/师级",		#  6
		"副部/军级",		#  7
		"正部/军级",		#  8
		"副国/大军区级",	#  9
		"正国/大军区级"	# 10
	]

	MIN_AGE = 15
	MAX_AGE = 80
	MIN_TICK = -5
	MAX_TICK = 10

	DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

