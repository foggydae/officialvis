'use strict';


var init_info_view = function (official_idx) {
    update_info_view(official_idx);
}


var update_info_view = function (official_idx) {
    var official_data = prepare_data(raw_data, official_idx)["complete"];
    console.log(official_data);
	$("#race").html(official_data[""]);
	$("#age").html(official_data[""]);
	$("#work-age").html(official_data[""]);
	$("#specialty").html(official_data[""]);
	$("#party-age").html(official_data[""]);
	$("#birth-place").html(official_data[""]);
	$("#gender").html(official_data[""]);
	$("#birth-date").html(official_data[""]);
	$("#work-date").html(official_data[""]);
	$("#party").html(official_data[""]);
	$("#party-date").html(official_data[""]);
	$("#origin").html(official_data[""]);
	$("#start-date").html(official_data[""]);
	$("#work-status").html(official_data[""]);
	$("#work-specialty").html(official_data[""]);
	$("#organization").html(official_data[""]);
	$("#position-rank").html(official_data[""]);
	$("#location-id").html(official_data[""]);
	$("#end-date").html(official_data[""]);
	$("#work-status-type").html(official_data[""]);
	$("#work-specialty-detail").html(official_data[""]);
	$("#position").html(official_data[""]);
	$("#location").html(official_data[""]);
}


