'use strict';

// global variables for map view
var map;
var marker_dict, maxValue;
var entities, branches, controller, baseMaps;
var new_places = L.layerGroup();
var move_path, arrow_head;

var init_map_view = function () {
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

	update_map_view();
}

var update_map_view = function () {
	$.get("/api/get_map_data",  function (rtn_string) {
		var resume_in_map = JSON.parse(rtn_string);
		var resume_by_loc = resume_in_map["loc_dict"];
		var resume_geo_path = resume_in_map["loc_path"];
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
   	})
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
