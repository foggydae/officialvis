'use strict';

// global variables for map view
var map;
var marker_dict, maxValue;
var entities, branches, controller, baseMaps;
var new_places = L.layerGroup();
var move_path, arrow_head;

var init_map_view = function (official_idx) {
	var baseMapLayer_light = L.tileLayer('http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
		id: "light",
		attribution: ""
	});
	var baseMapLayer_standard = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
		id: "standard",
		attribution: ""
	});
	baseMaps = {
		"light": baseMapLayer_light,
		"standard": baseMapLayer_standard
	};

	// put map to map-canvas
	map = L.map("map-canvas").setView([35.86, 104.14], 5);
	// load the map
	baseMapLayer_light.addTo(map);

	// init map with data
	// var message = JSON.stringify([4, 7]);
	// $.get("http://my3zhi.com:8081/api/api/visualization?list=" + message, function (rtn_string) {
	// 	var map_data = JSON.parse(rtn_string);
	// 	console.log(map_data);
		// marker_dict = {};
		// maxValue = 0;
		// for (var key in map_data) {
		//     maxValue = Math.max(Math.log(+map_data[key]["revenue"] + 1), maxValue);
		// }
		// init_marker_dict(map_data);
		// var new_layers = get_entity_group(map_data);
		// entities = new_layers[0];
		// branches = new_layers[1];
		// entities.addTo(map);
		// if (!cur_ignore_branch_flag) {
		// 	branches.addTo(map);
		// }

		// var overlayMaps = {
		//     "entities": entities,
		//     "branches": branches
		// };
		// controller = L.control.layers(baseMaps, overlayMaps);
		// controller.addTo(map);
	// });

	// console.log(data);
	// console.log(geo_dict["北京市"]);
	update_map_view(official_idx);
}

var update_map_view = function (official_idx) {
	$("#dataset-tag").html(raw_data["data"][official_idx]["name"]);

	var resume_in_map = prepare_data(raw_data, official_idx);
	var resume_by_loc = resume_in_map["geo_dict"];
	var resume_geo_path = resume_in_map["geo_path"];
	console.log(resume_in_map);

	new_places = new_places.clearLayers();
	try {
		map.removeLayer(move_path);
		map.removeLayer(arrow_head);
	} catch(error) {
		console.log("unable to remove");
	}

	for (var loc in resume_by_loc) {
		var str = "<span class='info-header'>" + loc.replace(/_/g, " ") + "</span><br><span>";
		for (var idx in resume_by_loc[loc]["resume"]) {
			str += resume_by_loc[loc]["resume"][idx] + "<br>"
		}
		str += "</span>";
		new_places.addLayer(
			L.circleMarker([resume_by_loc[loc]["lat"], resume_by_loc[loc]["lon"]], {
				radius: Math.sqrt(resume_by_loc[loc]["duration"]) / 2,
				weight: 1
			})
			.bindPopup(str)
			.on("mouseover", function(d) {
				this.openPopup();
			})
			.on("mouseout", function(d) {
				this.closePopup();
			})
			.on("click", function(d) {
			})
		);
	}
	new_places.addTo(map);	

	move_path = L.polyline(resume_geo_path, {color: "#ff7800", weight: 1}).addTo(map);
    arrow_head = L.polylineDecorator(move_path, {
        patterns: [
            // {offset: '100%', repeat: 2, symbol: L.Symbol.arrowHead({pixelSize: 15, polygon: false, pathOptions: {stroke: true}})}
            // {offset: 0, repeat: 10, symbol: L.Symbol.dash({pixelSize: 0})}
            { offset: '10%', repeat: '50%', symbol: L.Symbol.arrowHead({pixelSize: 5, polygon: true, pathOptions: {stroke: true}})}
        ]
    }).addTo(map);
}

var init_marker_dict = function (official_data) {
	for (var key in map_data) {
		marker_dict[key] = L.circleMarker(
				[
					+map_data[key]["latitude"], 
					+map_data[key]["longitude"]
				], 
				{
					id: key,
					weight: 1,
					fill: true,
					radius: _get_radius(+map_data[key]["size"]),
					color: _get_colors(map_data[key]["type"]),
					fillColor: _get_colors(map_data[key]["type"]),
					fillOpacity: _get_opacity(map_data[key]["revenue"]),
					zindex: _get_z_index(map_data[key]["type"])
				}
			)
			.bindPopup(
				"<span class='info-header'>Name: </span><span>" + map_data[key]["name"] + "</span>"
			)
			.on("mouseover", function(d) {
				this.openPopup();
			})
			.on("mouseout", function(d) {
				this.closePopup();
			})
			.on("click", function(d) {
				center_node(d.target.options.id, true);
			}
		);
	}
}

var get_entity_group = function (map_data) {
	var new_entities = L.layerGroup(), 
		new_branches = L.layerGroup();
	for (var key in map_data) {
		if (map_data[key]["type"] == "branch") {
			new_branches.addLayer(marker_dict[key]);
		} else {
			new_entities.addLayer(marker_dict[key]);
		}
	}
	return [new_entities, new_branches];
}

// var update_map_view = function (duns) {
// 	// init map with data
// 	var message = JSON.stringify({
// 		select_entity: duns
// 	});
// 	$.get("/api/get_map_data/" + message, function (rtn_string) {
// 		if (rtn_string == "NO_DATA") {
// 			console.log("Error", "Failed in map data.");
// 		} else {
// 			var map_data = JSON.parse(rtn_string);
// 			var new_layers = get_entity_group(map_data);
// 			entities.remove();
// 			branches.remove();
// 			controller.remove();

// 			entities = new_layers[0];
// 			branches = new_layers[1];
// 			entities.addTo(map);
// 			if (!cur_ignore_branch_flag) {
// 				branches.addTo(map);
// 			}

// 			var overlayMaps = {
// 			    "entities": entities,
// 			    "branches": branches
// 			};
// 			controller = L.control.layers(baseMaps, overlayMaps);
// 			controller.addTo(map);
// 			if (duns != "ALL") {
// 				map.setView([+map_data[duns]["latitude"], +map_data[duns]["longitude"]], 2);				
// 			} else {
// 				map.setView([10, 0], 1);				
// 			}
// 		}
// 	});

// }

var _get_colors = function (type) {
	return NODE_COLOR[type];
}

var _get_radius = function (size) {
	// return Math.sqrt(Math.sqrt(size)) * 2 + 4;
	return size;
}

var _get_opacity = function (revenue) {
	return Math.log(+revenue + 1) / maxValue * 0.9 + 0.1;
}

var _get_z_index = function (type) {
	if (type == "branch") {
		return 1;
	} else {
		return 999;
	}
}
