from utils.config import config
from datetime import datetime
import json
import math
from pprint import pprint
from collections import defaultdict, Counter

class data_center(config):

	CENTRAL_LAT = 39.9113
	CENTRAL_LON = 116.3805
	UNKNOWN_LAT = 0
	UNKNOWN_LON = 0
	
	def __init__(self):
		# Establish direct connection with the raw data
		# TODO: Change this to connecting the database
		with open("./dataset/test.json", "r") as json_file:
			self.dataset = json.load(json_file)

		with open("./dataset/geo_dict.json", "r") as json_file:
			self.geo_dict = json.load(json_file)

	def get_metadata(self):
		official_list = list(self.dataset.keys())
		return official_list, self.DEFAULT_OFFICIAL

	def update_official(self, official_name = None):
		if official_name is None:
			official_name = self.DEFAULT_OFFICIAL
		self.official = self._clean_data(self.dataset[official_name])

	def get_loc_data(self):
		loc_dict = defaultdict(lambda:{
			"lat": self.UNKNOWN_LAT,
			"lon": self.UNKNOWN_LON,
			"resume": [],
			"types": [],
			"duration": 0
		})
		cur_loc = ""
		prev_geo = tuple()
		cur_geo = tuple()
		loc_path = []
		for entry in sorted(self.official["resumes"], key=lambda x:self._to_date(x["start_timestamp"])):
			loc = entry["loc_description"]
			loc_dict[loc]["lat"] = entry["latitude"]
			loc_dict[loc]["lon"] = entry["longitude"]
			loc_dict[loc]["resume"].append(entry["description"])
			loc_dict[loc]["types"].append(entry["type_head"])
			loc_dict[loc]["duration"] += entry["duration"]
			if cur_loc != loc:
				cur_loc = loc
				prev_geo = cur_geo
				cur_geo = (entry["latitude"], entry["longitude"])
				if len(prev_geo) != 0:
					loc_path.append([[prev_geo, cur_geo]])
		for loc in loc_dict.keys():
			loc_dict[loc]["type"] = self._prioritize_type(loc_dict[loc]["types"])
			loc_dict[loc]["color"] = self.TYPE_COLOR[loc_dict[loc]["type"]]
		return loc_dict, loc_path

	def get_summary_data(self):
		type_dict = defaultdict(int)
		rank_dict = defaultdict(int)
		total_duration = 0
		for entry in self.official["resumes"]:
			type_dict[entry["type_head"]] += entry["duration"]
			rank_dict[entry["rank_num"]] += entry["duration"]
			total_duration += entry["duration"]

		yet_duration = 0
		type_summary = []
		for title, duration in type_dict.items():
			type_summary.append({
				"title": title,
				"color": self.TYPE_COLOR[title],
				"duration": duration,
				"percentage": duration / total_duration,
				"start":yet_duration / total_duration
			})
			yet_duration += duration

		yet_duration = 0
		rank_summary = []
		for rank_num, duration in rank_dict.items():

			rank_summary.append({
				"title": self.RANK_TICKS[rank_num],
				"rank_num": rank_num,
				"color": self.RANK_COLOR[self.RANK_TICKS[rank_num]],
				"duration": duration,
				"percentage": duration / total_duration,
				"start":yet_duration / total_duration
			})
			yet_duration += duration

		return type_summary, rank_summary

	def get_rank_data(self):
		rank_point = []
		rank_path = []
		rank_connection = []

		prev_stamp = self._strfyear(self._to_date(self.official["birth_timestamp"]).year + self.MIN_AGE)
		prev_rank = 0

		for idx, period in enumerate(self.official["type_by_period"]):
			cur_stamp = period["start_timestamp"]
			end_stamp = period["end_timestamp"]
			cur_rank = period["rank_num"]
			# 1. add prefix connection when necessary
			connection = []
			# verify if horizontal connection is required
			if self._to_date(period["start_timestamp"]) > prev_stamp:
				connection.append({
					"class": "connection",
					"rank": prev_rank,
					"date": prev_stamp
				})
			if self._to_date(period["start_timestamp"]) < prev_stamp:
				print("[ERROR] start_timestamp < prev_stamp")
			connection.append({
				"class": "connection",
				"rank": prev_rank,
				"date": cur_stamp
			})
			# verify if vertical connection is required
			if cur_rank != prev_rank:
				connection.append({
					"class": "connection",
					"rank": cur_rank,
					"date": cur_stamp
				})
			if len(connection) > 1:
				rank_connection.append(connection)

			# 2. add current period's line
			rank_path.append([{
					"class": "rank",
					"id": "period" + str(idx),
					"rank": cur_rank,
					"date": cur_stamp
				}, {
					"class": "rank",
					"id": "period" + str(idx),
					"rank": cur_rank,
					"date": end_stamp
				}])

			# 3. add current period's point
			rank_point.append({
				"class": "rank",
				"id": "period" + str(idx),
				"rank": cur_rank,
				"date": cur_stamp,
				"type": cur_type,
				"color": self.TYPE_COLOR[cur_type],
				"age": cur_age,
			})

			# 4. update prev_stamp & prev_rank
			prev_stamp = end_stamp
			prev_rank = cur_rank


	def get_rank_data(self):
		age_dict = defaultdict(lambda:{
			"rank": [],
			"type": Counter(),
			"stamp": None
		})
		for entry in sorted(self.official["resumes"], key=lambda x:self._to_date(x["start_timestamp"])):
			age_dict[entry["start_age"]]["rank"].append(entry["rank_num"])
			age_dict[entry["start_age"]]["type"].update([entry["type_head"]])
			age_dict[entry["start_age"]]["stamp"] = entry["start_timestamp"]

		rank_point = []
		rank_path = []
		prev_rank = 0
		for cur_age in sorted(age_dict.keys()):
			cur_rank = max(age_dict[cur_age]["rank"])
			cur_type = age_dict[cur_age]["type"].most_common()[0][0]
			cur_stamp = age_dict[cur_age]["stamp"]
			rank_point.append({
				"class": "rank",
				"rank": cur_rank,
				"date": cur_stamp,
				"type": cur_type,
				"color": self.TYPE_COLOR[cur_type],
				"age": cur_age,
			})
			rank_path.append({
				"class": "rank",
				"rank": prev_rank,
				"date": cur_stamp,
				"age": cur_age
			})
			if prev_rank != cur_rank:
				prev_rank = cur_rank
				rank_path.append({
					"class": "rank",
					"rank": cur_rank,
					"date": cur_stamp,
					"age": cur_age
				})
		rank_path.append({
			"class": "rank",
			"rank": prev_rank,
			"date": self._parse_date("today"),
			"age": self.official["current_age"]
		})
		return rank_point, rank_path

	def get_edu_data(self):
		edu_point = []
		edu_path = []
		for entry in sorted(self.official["educations"], key=lambda x:self._to_date(x["start_timestamp"])):
			cur_data = [
				{
					"rank": entry['diploma_num'],
					"diploma": entry['diploma_num'],
					"date": entry['start_timestamp'],
					"age": entry['start_age'],
					"part_time": entry['type'],
					"color": self.MAJOR_COLOR[entry["major"]],
					"class": "edu",
					"type": "start"
				}, {
					"rank": entry['diploma_num'],
					"diploma": entry['diploma_num'],
					"date": entry['finish_timestamp'],
					"age": entry['end_age'],
					"part_time": entry['type'],
					"color": self.MAJOR_COLOR[entry["major"]],
					"class": "edu",
					"type": "end"
				}
			]
			edu_point.extend(cur_data)
			edu_path.append(cur_data)
		return edu_point, edu_path

	def get_line_metadata(self):
		birth_year = self._to_date(self.official["birth_timestamp"]).year
		start_year = birth_year + self.MIN_AGE - 5
		min_year = birth_year + self.MIN_AGE
		max_year = birth_year + self.MAX_AGE

		x_list = [""]
		cur_age = self.MIN_AGE
		while cur_age <= self.MAX_AGE:
			cur_year = min_year + (cur_age - self.MIN_AGE)
			x_list.append(str(cur_year) + "(" + str(cur_age) + ")")
			cur_age += 5
		return self._strfyear(start_year), self._strfyear(max_year), self.MIN_TICK, self.MAX_TICK, x_list, self.AXIS_TICKS

	def get_congress_data(self):
		congress_dates = sorted(map(lambda x:self._to_date(x), self.NATIONAL_CONGRESS.values()))
		congress_ranges = zip(congress_dates, congress_dates[1:] + [datetime.today()])
		return [{"start": ranges[0].strftime(self.DATETIME_FORMAT), 
			"end": ranges[1].strftime(self.DATETIME_FORMAT),
			"title": str(list(self.NATIONAL_CONGRESS.keys())[idx]) + "大"
			} for idx, ranges in enumerate(congress_ranges)]

	def get_official(self):
		# get official 
		return self.official

	def _clean_data(self, ofcl_dataset):
		ofcl_dataset["birth_timestamp"] = self._parse_date(ofcl_dataset["birth"])
		ofcl_dataset["current_age"] = self._calc_time_gap(ofcl_dataset["birth_timestamp"])
		ofcl_dataset["death_timestamp"] = self._parse_date(ofcl_dataset["death"])
		
		ofcl_dataset["gender_desc"] = ("男" if ofcl_dataset["gender"] == 1 else "女")
		
		ofcl_dataset["hometown_desc"] = self._create_bilevel_desc(ofcl_dataset["home_province"], ofcl_dataset["home_county"])
		ofcl_dataset["birthplace_desc"] = self._create_bilevel_desc(ofcl_dataset["birth_province"], ofcl_dataset["birth_county"])
		
		ofcl_dataset["work_timestamp"] = self._parse_date(ofcl_dataset["job_time"])
		ofcl_dataset["work_age"] = self._calc_time_gap(ofcl_dataset["work_timestamp"])
		ofcl_dataset["party_timestamp"] = self._parse_date(ofcl_dataset["party_time"])
		ofcl_dataset["party_age"] = self._calc_time_gap(ofcl_dataset["party_timestamp"])

		ofcl_dataset["specialist"] = self._create_single_desc(ofcl_dataset["specialist"])

		# clean up resumes
		for resume_entry in ofcl_dataset["resumes"]:
			# generate string description
			resume_entry["description"] = self._create_work_desc(resume_entry)

			# generate longitude & latitude
			resume_entry["loc_description"], resume_entry["latitude"], resume_entry["longitude"] = \
				self._parse_geo(
					resume_entry["district"]["province"],
					resume_entry["district"]["city"],
					resume_entry["district"]["county"],
					resume_entry["district"]["central"]
				)
	
			# calculate length of stay
			resume_entry['start_timestamp'] = self._parse_date(resume_entry['start_time'], fill_today=True)
			resume_entry['finish_timestamp'] = self._parse_date(resume_entry['finish_time'], fill_today=True)
			resume_entry['duration'] = \
				self._calc_time_gap(resume_entry['start_timestamp'], resume_entry['finish_timestamp'], by="d")

			# calculate age
			resume_entry['start_age'] = \
				self._calc_time_gap(resume_entry['start_timestamp'], ofcl_dataset['birth_timestamp'])
			resume_entry['end_age'] = \
				self._calc_time_gap(resume_entry['finish_timestamp'], ofcl_dataset['birth_timestamp'])

			# get numeric rank
			resume_entry["rank"] = self._create_single_desc(resume_entry["rank"], replace="其他")
			resume_entry['rank_num'] = self._parse_rank(resume_entry["rank"])

			# others
			resume_entry["type_head"] = self._create_single_desc(resume_entry["type_head"], replace="其他")
			resume_entry["type_detail"] = self._create_single_desc(resume_entry["type_detail"], replace="其他")

		# clean up educations 
		for edu_entry in ofcl_dataset["educations"]:
			# generate string description
			edu_entry["description"] = self._create_edu_desc(edu_entry)

			# calculate timestamp
			edu_entry["start_timestamp"] = self._parse_date(edu_entry["start_time"])
			edu_entry["finish_timestamp"] = self._parse_date(edu_entry["finish_time"])

			# calculate age
			edu_entry['start_age'] = \
				self._calc_time_gap(edu_entry['start_timestamp'], ofcl_dataset['birth_timestamp'])
			edu_entry['end_age'] = \
				self._calc_time_gap(edu_entry['finish_timestamp'], ofcl_dataset['birth_timestamp'])

			# get numeric rank
			edu_entry['diploma_num'] = self._parse_degree(edu_entry["title"]);

			# others
			edu_entry["major"] = self._create_single_desc(edu_entry["major"], replace="其他")

		ofcl_dataset["latest_resume"] = self._find_latest_resume(ofcl_dataset["resumes"])
		ofcl_dataset["type_by_period"] = self._summarize_by_type(ofcl_dataset["resumes"])

		return ofcl_dataset

	def _find_latest_resume(self, resumes):
		return resumes[-1]

	def _summarize_by_type(self, resumes):
		def check_overlap(period1, period2):
			if period1[0] < period2[1] and period2[0] < period1[1]:
				return True
			return False

		period_list = []
		# period_dict = defaultdict(lambda: {
		# 	"rank_num": 0,
		# 	"descriptions": defaultdict(set)
		# })

		for entry in resumes:
			cur_desc = entry["description"]
			cur_period = (self._to_date(entry["start_timestamp"]), self._to_date(entry["finish_timestamp"]))
			# period_dict[cur_period]["rank_num"] = \
			# 	max(period_dict[cur_period]["rank_num"], entry["rank_num"])
			# period_dict[cur_period]["descriptions"][cur_period].add(entry["description"])

			overlaps = [cur_period]
			for ext_period in period_list:
				if check_overlap(ext_period, cur_period):
					overlaps.append(ext_period)
			period_list.append(cur_period)
			# use unique start to split new period
			# |----|-----|  -->  |--|-|-----|
			#    |-----|
			time_pt = sorted(list(set(list(map(lambda period:period[0], overlaps)) + \
				[max(list(map(lambda period:period[1], overlaps)))])))

			# use unique time point to split new period
			# |----|-----|  -->  |--|-|---|-|
			#    |-----|
			# unzip_overlap = list(zip(*overlaps))
			# time_pt = sorted(list(set(list(unzip_overlap[0]) + list(unzip_overlap[1]))))

			new_periods = list(zip(time_pt[:-1], time_pt[1:]))
			# for new_period in new_periods:
			# 	for ext_period in period_list:
			# 		if check_overlap(new_period, ext_period):
			# 			period_dict[new_period]["rank_num"] = \
			# 				max(period_dict[new_period]["rank_num"], period_dict[ext_period]["rank_num"])
			# 			for desc_period in period_dict[ext_period]["descriptions"].keys():
			# 				if check_overlap(new_period, desc_period):
			# 					period_dict[new_period]["descriptions"][desc_period] = \
			# 						period_dict[new_period]["descriptions"][desc_period] | \
			# 						period_dict[ext_period]["descriptions"][desc_period]
			period_list = list(set(period_list) - set(overlaps)) + new_periods

		type_by_period = []
		for period in sorted(period_list, key=lambda period:period[0]):
			type_list = []
			desc_list = []
			rank_list = []
			for entry in resumes:
				entry_period = (self._to_date(entry["start_timestamp"]), self._to_date(entry["finish_timestamp"]))
				if check_overlap(period, entry_period):
					type_list.append(entry["type_head"])
					desc_list.append(entry["description"])
					rank_list.append(entry["rank_num"])

			type_by_period.append({
				"start_timestamp": period[0].strftime(self.DATETIME_FORMAT),
				"end_timestamp": period[1].strftime(self.DATETIME_FORMAT),
				"rank_num": max(rank_list),
				"rank": self.RANK_TICKS[max(rank_list)],
				"descriptions": desc_list,
				"type": self._prioritize_type(type_list)
			})

		return type_by_period

	def _summarize_by_rank(self, resumes):
		pass

	def _prioritize_type(self, type_list):
		select_type = ""
		select_idx = max(self.TYPE_MAP.values())
		for cur_type in list(set(type_list)):
			if self.TYPE_MAP[cur_type] <= select_idx:
				select_idx = self.TYPE_MAP[cur_type]
				select_type = cur_type
		return select_type

	def _create_work_desc(self, entry):
		return self._create_date_desc(entry["start_time"], entry["finish_time"]) + \
			self._create_bilevel_desc(entry["sector_head"], entry["sector_detail"], suffix="，") + \
			self._create_bilevel_desc(entry["type_head"], entry["type_detail"], suffix="，") + \
			self._create_single_desc(entry["rank"], replace="无级别")

	def _create_edu_desc(self, entry):
		return self._create_date_desc(entry["start_time"], entry["finish_time"]) + \
			("在职" if entry["type"] == 1 else "非在职") + "，" + \
			entry["title"] + "学历"

	def _create_date_desc(self, start_time, end_time, suffix = "："):
		if start_time != "" and end_time != "" and \
			start_time is not None and end_time is not None and \
			end_time != datetime.today().strftime(self.DATETIME_FORMAT):
			return start_time[:7] + "~" + end_time[:7] + suffix
		elif start_time != "" and start_time is not None:
			return start_time[:7] + "至今" + suffix
		else:
			return ""

	def _create_bilevel_desc(self, head, detail, suffix = ""):
		if head != "" and detail != "":
			return head + " - " + detail + suffix
		elif head != "":
			return head + suffix
		else:
			return ""

	def _create_single_desc(self, value, replace = "无"):
		if value is None:
			return replace
		if value == "" or value == "N.A." or value == "NULL":
			return replace
		else:
			return value

	def _parse_rank(self, rank):
		try:
			return self.RANK_MAP[rank]
		except:
			print("[ERROR] unrecognized rank: " + rank)
			return 0

	def _parse_degree(self, degree):
		try:
			for key in self.DEGREE_MAP.keys():
				if key in degree:
					return self.DEGREE_MAP[key]
			return 0
		except:
			return 0

	def _parse_date(self, dt, ptn="%Y-%m", fill_today=False):
		if dt is None:
			if fill_today:
				return datetime.today().strftime(self.DATETIME_FORMAT)
			else:
				return None
		elif dt == "today":
			return datetime.today().strftime(self.DATETIME_FORMAT)
		else:
			return datetime.strptime(dt[:7], ptn).strftime(self.DATETIME_FORMAT)

	def _to_date(self, dt):
		return datetime.strptime(dt, self.DATETIME_FORMAT)

	def _strfyear(self, year):
		return datetime(year=year, month=1, day=1).strftime(self.DATETIME_FORMAT)

	def _parse_geo(self, province, city, county, central = None):
		try:
			if central is not None and central == True:
				loc_desc = "中央"
				cur_lat = self.CENTRAL_LAT
				cur_lon = self.CENTRAL_LON
			elif province != "" and province != "N.A." and city != "" and county != "":
				loc_desc = province + "-" + city + "-" + county
				cur_lat = self.geo_dict[province][city][county]["lat"]
				cur_lon = self.geo_dict[province][city][county]["lon"]
			elif province != "" and province != "N.A." and city != "":
				loc_desc = province + "-" + city
				cur_lat = self.geo_dict[province][city]["lat"]
				cur_lon = self.geo_dict[province][city]["lon"]
			elif province != "" and province != "N.A." and county != "":
				loc_desc = province + "-" + county
				cur_lat = self.geo_dict[province][county]["lat"]
				cur_lon = self.geo_dict[province][county]["lon"]
			elif city != "":
				loc_desc = city
				cur_lat = self.geo_dict[city]["lat"]
				cur_lon = self.geo_dict[city]["lon"]
			elif province != "N.A." and province != "":
				loc_desc = province
				cur_lat = self.geo_dict[province]["lat"] + 0.05
				cur_lon = self.geo_dict[province]["lon"] + 0.05
			else:
				loc_desc = "不详"
				cur_lat = self.UNKNOWN_LAT
				cur_lon = self.UNKNOWN_LON
		except:
			print(province, city, county)
			loc_desc = "不详"
			cur_lat = self.UNKNOWN_LAT
			cur_lon = self.UNKNOWN_LON

		return loc_desc, cur_lat, cur_lon

	def _calc_time_gap(self, dt1, dt2 = None, by = "y"):
		if dt1 is None:
			dt1 = datetime.today()
		else:
			dt1 = self._to_date(dt1)	
		if dt2 is None:
			dt2 = datetime.today()
		else:
			dt2 = self._to_date(dt2)	

		if by == "d":
			return abs((dt1 - dt2).days)
		elif by == "y":
			return abs((dt1 - dt2).days) // 365
		else:
			return 0

if __name__ == '__main__':
	test_dc = data_center()
	test_dc.update_official("蔡奇")
	pprint(test_dc.official)
