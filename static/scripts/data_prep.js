'use strict';

var CENTRAL_LAT = 39.9113,
	CENTRAL_LON = 116.3805;
var UNKNOWN_LAT = 0,
	UNKNOWN_LON = 0;

// util functions

var clean_data = function (raw_data, official_idx) {
	let official_dataset = raw_data["data"][official_idx];
	official_dataset["birth_timestamp"] = 
		new Date(official_dataset['birth']);
	let today = new Date();
	official_dataset['current_age'] = Math.ceil(
		Math.abs(official_dataset["birth_timestamp"].getTime() - 
			today.getTime()) / (1000 * 3600 * 24 * 365));

	for (var idx in official_dataset['resumes']) {
		let resume_entry = official_dataset['resumes'][idx];
		// generate string description
		resume_entry['description'] = generate_description(resume_entry);

		// generate longitude & latitude
		let geo_info = generate_geo(resume_entry);
		resume_entry['loc_description'] = geo_info[0];
		resume_entry['latitude'] = geo_info[1];
		resume_entry['longitude'] = geo_info[2];

		// calculate length of stay
		resume_entry['start_timestamp'] = 
			new Date(resume_entry['start_time']);
		resume_entry['finish_timestamp'] = 
			new Date(resume_entry['finish_time']);
		let stay_duration = Math.abs(resume_entry['finish_timestamp'].getTime() - 
			resume_entry['start_timestamp'].getTime());
		resume_entry['duration'] = 
			Math.ceil(stay_duration / (1000 * 3600 * 24)); 

		// calculate age
		let age_start = Math.abs(official_dataset["birth_timestamp"].getTime() - 
			resume_entry['start_timestamp'].getTime());
		let age_end = age_start + stay_duration;
		resume_entry['start_age'] = Math.ceil(age_start / (1000 * 3600 * 24 * 365)); 
		resume_entry['end_age'] = Math.ceil(age_end / (1000 * 3600 * 24 * 365));

		// get numeric rank
		resume_entry['rank_num'] = convert_rank(resume_entry["rank"]);
	}
	return official_dataset;
}


var generate_description = function (entry) {
	return entry["start_time"] + "~" + entry["finish_time"] + ": " + 
		entry["sector_head"] + "-" + entry["sector_detail"] + ", " + 
		entry["rank"];
}


var generate_geo = function (entry) {
	let central = entry["district"]["central"],
		province = entry["district"]["province"],
		city = entry["district"]["city"],
		county = entry["district"]["county"];
	let loc, cur_lat, cur_lon;

	if (central) {
		loc = "中央";
		cur_lat = CENTRAL_LAT;
		cur_lon = CENTRAL_LON;
	} else if (province != "" & province != "N.A." & city != "" & county != "") {
		loc = province + "_" + city + "_" + county;
		cur_lat = geo_dict[province][city][county]["lat"];
		cur_lon = geo_dict[province][city][county]["lon"];
	} else if (province != "" & province != "N.A." & city != "") {
		loc = province + "_" + city;
		cur_lat = geo_dict[province][city]["lat"];
		cur_lon = geo_dict[province][city]["lon"];
	} else if (province != "" & province != "N.A." & county != "") {
		loc = province + "_" + county;
		cur_lat = geo_dict[province][county]["lat"];
		cur_lon = geo_dict[province][county]["lon"];
	} else if (city != "") {
		loc = city;
		cur_lat = geo_dict[city]["lat"];
		cur_lon = geo_dict[city]["lon"];
	} else if (province != "N.A." & province != "") {
		loc = province;
		cur_lat = geo_dict[province]["lat"];
		cur_lon = geo_dict[province]["lon"];
	} else {
		loc = "不详";
		cur_lat = UNKNOWN_LAT;
		cur_lon = UNKNOWN_LON;
	}

	return [loc, cur_lat, cur_lon];
}


var convert_rank = function (rank) {
	var rank_map = {
		"正国级": 10,
		"副国级": 9,
		"正大军区级": 8,
		"副大军区级": 7,
		"正部级、正军级": 8,
		"副部级、副军级": 7,
		"正厅级、正师级": 6,
		"副厅级、副师级": 5,
		"正处级、正团级": 4,
		"副处级、副团级": 3,
		"正科级、正营级": 2,
		"副科级、副营级": 1,
		"": 0
	};
	if (typeof rank == 'undefined') {
		return 0;
	} else if (rank in rank_map) {
		return rank_map[rank];
	} else {
		return 0;
	}
}


var prepare_geo_dict = function (resumes) {
	let resume_by_loc = {};

	for (let idx in resumes) {
		let entry = resumes[idx];
		let loc = entry["loc_description"];

		if (!resume_by_loc.hasOwnProperty(loc)) {
			resume_by_loc[loc] = {};
			resume_by_loc[loc]["lat"] = entry["latitude"];
			resume_by_loc[loc]["lon"] = entry["longitude"];
			resume_by_loc[loc]["resume"] = [];
			resume_by_loc[loc]["duration"] = entry["duration"];
			resume_by_loc[loc]["resume"].push(entry["description"]);
		} else {
			resume_by_loc[loc]["duration"] += entry["duration"];
			resume_by_loc[loc]["resume"].push(entry["description"]);
		}
	}

	return resume_by_loc;
}


var prepare_geo_path = function (resumes) {
	let geo_path = [];
	let geo_place = [];
	let cur_place = "";
	let prev_geo = [], cur_geo = [];

	function compare (a, b) {
		if (a["first_timestamp"] < b["first_timestamp"])
			return -1;
		if (a["first_timestamp"] > b["first_timestamp"])
			return 1;
		return 0;
	}

	resumes.sort(compare);

	// console.log(resumes);

	for (let idx in resumes) {
		let entry = resumes[idx];
		if (cur_place != entry['loc_description']) {
			cur_place = entry['loc_description'];
			prev_geo = cur_geo;
			cur_geo = [entry["latitude"], entry["longitude"]];
			if (prev_geo.length != 0) {
				geo_path.push([[prev_geo, cur_geo]]);
			}
			geo_place.push(cur_place);
		}
	}

	// console.log(geo_place);

	return geo_path;
}


var prepare_rank_seqs = function (resumes, current_age) {
	let age_dict = {};

	function compare (a, b) {
		if (a["first_timestamp"] < b["first_timestamp"])
			return -1;
		if (a["first_timestamp"] > b["first_timestamp"])
			return 1;
		return 0;
	}

	resumes.sort(compare);

	for (let idx in resumes) {
		let entry = resumes[idx];
		let cur_age = entry['start_age'];
		if (cur_age in age_dict) {
			age_dict[cur_age]["rank"].push(entry['rank_num']);
		} else {
			age_dict[cur_age] = {};
			age_dict[cur_age]['rank'] = [entry['rank_num']];
			age_dict[cur_age]["stamp"] = entry['start_timestamp'];
		}
	}

	let age_list = Object.keys(age_dict).sort();

	let prev_rank = 0;
	let rank_seq = [];
	let date_seq = [];
	let age_seq  = [];
	let rank_data = [];
	let promo_data = [];

	for (let key in age_list) {
		let cur_age = age_list[key];
		let timestamp = age_dict[cur_age]['stamp'];
		let cur_rank = Math.max(...age_dict[cur_age]['rank']);
		rank_seq.push(prev_rank);
		date_seq.push(timestamp);
		age_seq.push(cur_age);
		rank_data.push({
			"rank": prev_rank,
			"date": timestamp,
			"age": cur_age
		})
		promo_data.push({
			"rank": cur_rank,
			"date": timestamp,
			"age": cur_age
		})
		if (prev_rank != cur_rank) {
			prev_rank = cur_rank;
			rank_seq.push(cur_rank);
			date_seq.push(timestamp);
			age_seq.push(cur_age);
			rank_data.push({
				"rank": prev_rank,
				"date": timestamp,
				"age": cur_age
			})
		}
	}

	let today = new Date();

	rank_data.push({
		"rank": prev_rank,
		"date": new Date(),
		"age": current_age
	})

	return {
		"rank_seq": rank_seq,
		"date_seq": date_seq,
		"age_seq": age_seq,
		"rank_data": rank_data,
		"promo_data": promo_data
	};
}


var prepare_data = function (raw_data, official_idx) {
	let official = clean_data(raw_data, official_idx);
	console.log(official);
	let rank_seqs = prepare_rank_seqs(official["resumes"], official["current_age"]);
	return {
		"geo_dict": prepare_geo_dict(official["resumes"]),
		"geo_path": prepare_geo_path(official["resumes"]),
		"rank_seq": rank_seqs['rank_seq'],
		"date_seq": rank_seqs['date_seq'],
		"age_seq":  rank_seqs['age_seq'],
		"rank_data": rank_seqs['rank_data'],
		"promo_data": rank_seqs['promo_data']
	}
}



