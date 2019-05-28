'use strict';

/*********************
 * Global Variables **
 *********************/

$.get("/api/get_metadata", function (rtn_string) {
	var metadata = JSON.parse(rtn_string);

	for (var i = 0; i < metadata["official_list"].length; i++) {
		$("#dropdown-menu").append(
			"<button class='dropdown-item'>" + 
			metadata["official_list"][i] + 
			"</button>"
		);
	}

	$("#official-btn").html(metadata["default_official"]);

	$(".dropdown-item").on("click", function () {
		var current_official = $(this).html();
		var message = JSON.stringify({
			"official": current_official
		});
		$.get("/api/update_official/" + message, function (rtn_string) {
			if (rtn_string == "DONE") {
				update_map_view();
				update_rank_view();
				update_info_view();
				update_summary_view();
				$("#official-btn").html(current_official);
			} else {
				console.log(rtn_string);
			}
		})
	});	
});

/*********************
 ** Initiate Views ***
 *********************/

init_info_view();
init_summary_view();
init_map_view();
init_rank_view();

/*********************
 * Manual Responsive *
 *********************/

// additional listener for size-responsiblility of certain views
$(window).resize(function () { 
	update_rank_view();
	update_summary_view();
});
