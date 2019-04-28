from config import config

class data_center(config):

	def __init__(self):
		pass

	def update_official(self, official_id = None):
		
		if official_id is None:
			official_id = self.DEFAULT_ID

		

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
