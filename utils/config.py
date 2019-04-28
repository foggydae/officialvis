class config():
	# default official: the official shown when open page

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
