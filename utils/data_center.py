from config import config
import json

class data_center(config):

	def __init__(self):
		# Establish direct connection with the raw data
		# TODO: Change this to connecting the database
		with open("../dataset/test.json", "r") as json_file:
			self.dataset = json.load(json_file)

	def update_official(self, official_name = None):
		if official_name is None:
			official_name = self.DEFAULT_OFFICIAL
		self.official = self.dataset[official_name]



	def _clean_data(self):
		pass

	def _create_work_desc(self):
		pass

	def _create_edu_desc(self):
		pass

	def _create_date_desc(self):
		pass

	def _create_loc_desc(self):
		pass

	def _create_bilevel_desc(self):
		pass

	def _parse_rank(self, rank):
		print(self.RANK_MAP)

if __name__ == '__main__':
	test_dc = data_center()
