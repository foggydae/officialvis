from flask import Flask, request, render_template
from utils.data_center import data_center
import json

app = Flask(__name__)
dt = data_center()

@app.route("/", methods=['GET'])
def Index():
	dt.update_official()
	return render_template("main.html")

@app.route("/api/get_metadata", methods=["GET"])
def get_metadata():
	official_list, default_official = dt.get_metadata()
	return json.dumps({
		"official_list": official_list,
		"default_official": default_official
	})

@app.route("/api/get_official", methods=["GET"])
def get_official():
	return json.dumps(dt.get_official())

@app.route("/api/get_line_data", methods=["GET"])
def get_line_data():
	rank_point, rank_path, rank_connection = dt.get_rank_data()
	edu_point, edu_path = dt.get_edu_data()
	x_min, x_max, y_min, y_max, x_list, y_list = dt.get_line_metadata()
	congress_ranges = dt.get_congress_data()
	return json.dumps({
		"rank_point": rank_point,
		"rank_path": rank_path,
		"rank_connection": rank_connection,
		"edu_point": edu_point,
		"edu_path": edu_path,
		"congress_ranges": congress_ranges,
		"x_min": x_min, 
		"x_max": x_max, 
		"y_min": y_min, 
		"y_max": y_max, 
		"x_list": x_list, 
		"y_list": y_list
	})

@app.route("/api/get_map_data", methods=["GET"])
def get_map_data():
	loc_dict, loc_path = dt.get_loc_data()
	return json.dumps({
		"loc_dict": loc_dict, 
		"loc_path": loc_path
	})

@app.route("/api/get_summary_data", methods=["GET"])
def get_summary_data():
	type_summary = dt.get_type_summary_data()
	rank_summary = dt.get_rank_summary_data()
	return json.dumps({
		"type_summary": type_summary,
		"rank_summary": rank_summary
	})

@app.route("/api/update_official/<message>", methods=["GET"])
def update_official(message):
	new_official = json.loads(message)["official"]
	dt.update_official(new_official)
	return "DONE"

if __name__ == "__main__":
	app.run(debug=True)
