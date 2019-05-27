'use strict';


var init_info_view = function () {
    update_info_view();
}


var update_info_view = function () {
	$.get("/api/get_official", function (rtn_string) {
		var official_data = JSON.parse(rtn_string);
		console.log(official_data);
		$("#official-name").html(official_data["name"]);
		$("#race").html(official_data["nationality"]);
		$("#age").html(official_data["current_age"]);
		$("#work-age").html(official_data["work_age"]);
		$("#specialty").html(official_data["specialist"]);
		$("#party-age").html(official_data["party_age"]);
		$("#birth-place").html(official_data["birthplace_desc"]);
		$("#gender").html(official_data["gender_desc"]);
		$("#birth-date").html(official_data["birth"]);
		$("#work-date").html(official_data["job_time"]);
		$("#party").html(official_data["party"]);
		$("#party-date").html(official_data["party_time"]);
		$("#origin").html(official_data["hometown_desc"]);
		$("#start-date").html(official_data["latest_resume"]["start_time"]);
		$("#work-status").html(official_data["latest_resume"]["title_head"]);
		$("#work-specialty").html(official_data["latest_resume"]["type_head"]);
		$("#organization").html(official_data["latest_resume"]["sector_head"]);
		$("#position-rank").html(official_data["latest_resume"]["rank"]);
		$("#location-id").html(official_data["latest_resume"]["district_code"]);
		$("#end-date").html(official_data["latest_resume"]["finish_time"]);
		$("#work-status-type").html(official_data["latest_resume"]["title_detail"]);
		$("#work-specialty-detail").html(official_data["latest_resume"]["type_detail"]);
		$("#position").html(official_data["latest_resume"]["sector_detail"]);
		$("#location").html(official_data["latest_resume"]["loc_description"]);
	})
}


