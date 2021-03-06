class config():
	# default official: the official to display when openning the page
	DEFAULT_OFFICIAL = "习近平"

	# use geocode of 中南海 to encode `中央`
	CENTRAL_LAT = 39.9113
	CENTRAL_LON = 116.3805

	# arbitary chosen geocode for missing location
	UNKNOWN_LAT = 0
	UNKNOWN_LON = 0

	DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"

	# dictionary for rank
	RANK_MAP = {
		"正国级": 12,
		"副国级": 11,
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
		"": 0,
		"其他": 0
	}

	RANK_TICKS = [
		"-",			#  0
		"副科/营级",		#  1
		"正科/营级",		#  2
		"副处/团级",		#  3
		"正处/团级",		#  4
		"副厅/师级",		#  5
		"正厅/师级",		#  6
		"副部/军级",		#  7
		"正部/军级",		#  8
		"副大军区级",		#  9
		"正大军区级",		# 10
		"副国级",		# 11
		"正国级"			# 12
	]

	RANK_COLOR = {
		"-": '#ffffcc',
		"副科/营级": '#ffeda0',
		"正科/营级": '#fed976',
		"副处/团级": '#feb24c',
		"正处/团级": '#fd8d3c',
		"副厅/师级": '#fc4e2a',
		"正厅/师级": '#e31a1c',
		"副部/军级": '#bd0026',
		"正部/军级": '#800026',
		"副大军区级": '#520115',
		"正大军区级": '#2b000b',
		"副国级":	'#520115',
		"正国级":	'#2b000b'
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

	DEGREE_TICKS = [
		"培训",			# -5
		"博士",			# -4
		"硕士",			# -3
		"本科",			# -2
		"专科",			# -1
		"NA"			#  0
	]

	MIN_AGE = 15
	MAX_AGE = 80
	MIN_TICK = min(DEGREE_MAP.values())
	MAX_TICK = max(RANK_MAP.values())
	AXIS_TICKS = DEGREE_TICKS[:-1] + RANK_TICKS

	NATIONAL_CONGRESS = {
		12: "1982-09-01T00:00:00",
		13: "1987-10-25T00:00:00",
		14: "1992-10-12T00:00:00",
		15: "1997-09-12T00:00:00",
		16: "2002-11-08T00:00:00",
		17: "2007-10-15T00:00:00",
		18: "2012-11-08T00:00:00",
		19: "2017-10-18T00:00:00"
	}

	MAJOR_COLOR = {
	    "哲学": 	'darkred',
	    "经济学":'darkred',
	    "法学": 	'darkred',
	    "教育学":'darkred',
	    "文学": 	'darkred',
	    "历史学":'darkred',
	    "理学": 	'darkred',
	    "工学": 	'darkred',
	    "农学": 	'darkred',
	    "医学": 	'darkred',
	    "军事学":'darkred',
	    "管理学":'darkred',
	    "艺术学":'darkred',
	    "其他": 	'darkred'
	}

	TYPE_COLOR = {
		"一线领导职务": "#1f77b4",
		"二线领导职务": "#aec7e8",
		"党口办公厅":	  "#ff7f0e",
		"政府办公厅":	  "#ffbb78",
		"国安":		  "#f7b6d2",
		"纪委监察":	  "#e377c2",
		"组织人事口":	  "#c49c94",
		"宣传文教口":	  "#c5b0d5",
		"军队口":	  "#2ca02c",
		"外事统战口":	  "#8c564b",
		"财政经济口":	  "#d62728",
		"政治法律口":	  "#ff9896",
		"群团组织口":	  "#9467bd",
		"知识分子口":	  "#98df8a",
		"其他":		  "#7f7f7f"
	}

	TYPE_MAP = {
		"一线领导职务": 1,
		"二线领导职务": 2,
		"党口办公厅":	  3,
		"政府办公厅":	  4,
		"国安":		  5,
		"纪委监察":	  6,
		"组织人事口":	  7,
		"宣传文教口":	  8,
		"军队口":	  9,
		"外事统战口":	  10,
		"财政经济口":	  11,
		"政治法律口":	  12,
		"群团组织口":	  13,
		"知识分子口":	  14,
		"其他":		  15

	}

	TYPE_DETAIL = {
		"一线领导职务": ["一线领导职务"],
		"二线领导职务": ["二线领导职务"],
		"党口办公厅":	  ["党口办公厅"],		
		"政府办公厅":	  ["政府办公厅"],
		"国安":		  ["国安"],
		"纪委监察":	  ["纪委监察"],
		"组织人事口":	  ["组织人事"],
		"宣传文教口":	  ["宣传", "教文卫"],
		"军队口":	  ["军事"],
		"外事统战口":	  ["外事统战口", "民主党派"],
		"财政经济口":	  ["基础设施交通建设", "机械工业口", "能源工业口", "计委", "经委", "农口国土口"],
		"政治法律口":	  ["政法口"],
		"群团组织口":	  ["团口", "社会团体"],
		"知识分子口":	  ["文", "理"],
		"其他":		  ["其他"]
	}


