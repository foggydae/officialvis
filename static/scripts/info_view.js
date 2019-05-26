'use strict';


var init_info_view = function () {
    update_info_view();
}


var update_info_view = function () {
	$.get("/api/get_official", function (rtn_string) {
		var official_data = JSON.parse(rtn_string);
		console.log(official_data);

		$("#race").html(official_data["nationality"]);
		$("#age").html(official_data["current_age"]);
		$("#work-age").html(official_data[""]);
		$("#specialty").html(official_data["specialist"]);
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
	})
}


