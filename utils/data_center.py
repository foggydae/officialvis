from utils.config import config
from datetime import datetime
import json
from pprint import pprint
from collections import defaultdict

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
			"duration": 0
		})
		cur_loc = ""
		prev_geo = tuple()
		cur_geo = tuple()
		loc_path = []
		for entry in sorted(self.official["resumes"], key=lambda x:datetime.strptime(x["start_timestamp"], self.DATETIME_FORMAT)):
			loc = entry["loc_description"]
			loc_dict[loc]["lat"] = entry["latitude"]
			loc_dict[loc]["lon"] = entry["longitude"]
			loc_dict[loc]["resume"].append(entry["description"])
			loc_dict[loc]["duration"] += entry["duration"]
			if cur_loc != loc:
				cur_loc = loc
				prev_geo = cur_geo
				cur_geo = (entry["latitude"], entry["longitude"])
				if len(prev_geo) != 0:
					loc_path.append([[prev_geo, cur_geo]])
		return loc_dict, loc_path

	def get_rank_data(self):
		age_dict = defaultdict(lambda:{
			"rank": [],
			"stamp": None
		})
		for entry in sorted(self.official["resumes"], key=lambda x:datetime.strptime(x["start_timestamp"], self.DATETIME_FORMAT)):
			age_dict[entry["start_age"]]["rank"].append(entry["rank_num"])
			age_dict[entry["start_age"]]["stamp"] = entry["start_timestamp"]

		rank_point = []
		rank_path = []
		prev_rank = 0
		for cur_age in sorted(age_dict.keys()):
			cur_rank = max(age_dict[cur_age]["rank"])
			cur_stamp = age_dict[cur_age]["stamp"]
			rank_point.append({
				"class": "rank",
				"rank": cur_rank,
				"date": cur_stamp,
				"age": cur_age
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
		for entry in sorted(self.official["educations"], key=lambda x:datetime.strptime(x["start_timestamp"], self.DATETIME_FORMAT)):
			cur_data = [
				{
					"rank": entry['diploma_num'],
					"diploma": entry['diploma_num'],
					"date": entry['start_timestamp'],
					"age": entry['start_age'],
					"class": "edu",
					"type": "start"
				}, {
					"rank": entry['diploma_num'],
					"diploma": entry['diploma_num'],
					"date": entry['finish_timestamp'],
					"age": entry['end_age'],
					"class": "edu",
					"type": "end"
				}
			]
			edu_point.extend(cur_data)
			edu_path.append(cur_data)
		return edu_point, edu_path

	def get_official(self):
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
			resume_entry['start_timestamp'] = self._parse_date(resume_entry['start_time'])
			resume_entry['finish_timestamp'] = self._parse_date(resume_entry['finish_time'])
			resume_entry['duration'] = \
				self._calc_time_gap(resume_entry['start_timestamp'], resume_entry['finish_timestamp'], by="d")

			# calculate age
			resume_entry['start_age'] = \
				self._calc_time_gap(resume_entry['start_timestamp'], ofcl_dataset['birth_timestamp'])
			resume_entry['end_age'] = \
				self._calc_time_gap(resume_entry['finish_timestamp'], ofcl_dataset['birth_timestamp'])

			# get numeric rank
			resume_entry['rank_num'] = self._parse_rank(resume_entry["rank"])

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

		ofcl_dataset["latest_resume"] = ofcl_dataset["resumes"][-1]
		return ofcl_dataset


	def _create_work_desc(self, entry):
		return self._create_date_desc(entry["start_time"], entry["finish_time"]) + \
			self._create_bilevel_desc(entry["sector_head"], entry["sector_detail"], suffix="，") + \
			entry["rank"]

	def _create_edu_desc(self, entry):
		return self._create_date_desc(entry["start_time"], entry["finish_time"]) + \
			("在职" if entry["type"] == 1 else "非在职") + "，" + \
			entry["title"] + "学历"

	def _create_date_desc(self, start_time, end_time, suffix = "："):
		if start_time != "" and end_time != "" and \
			start_time is not None and end_time is not None:
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

	def _create_single_desc(self, value):
		if value is None:
			return "无"
		if value == "" or value == "N.A.":
			return "无"
		else:
			return value

	def _parse_rank(self, rank):
		try:
			return self.RANK_MAP[rank]
		except:
			return 0

	def _parse_degree(self, degree):
		try:
			for key in self.DEGREE_MAP.keys():
				if key in degree:
					return self.DEGREE_MAP[key]
			return 0
		except:
			return 0

	def _parse_date(self, dt, ptn="%Y-%m"):
		if dt is None:
			return None
		elif dt == "today":
			return datetime.today().strftime(self.DATETIME_FORMAT)
		else:
			return datetime.strptime(dt[:7], ptn).strftime(self.DATETIME_FORMAT)

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
			dt1 = datetime.strptime(dt1, self.DATETIME_FORMAT)	
		if dt2 is None:
			dt2 = datetime.today()
		else:
			dt2 = datetime.strptime(dt2, self.DATETIME_FORMAT)	

		if by == "d":
			return abs((dt1 - dt2).days)
		elif by == "y":
			return abs((dt1 - dt2).days) // 365
		else:
			return 0





if __name__ == '__main__':
	test_dc = data_center()
	test_dc.update_official("蔡奇")
	test_dc.get_loc_info()
