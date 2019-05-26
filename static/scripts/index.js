'use strict';

/*********************
 * Global Variables **
 *********************/

$.get("/api/get_metadata", function (rtn_string) {
	var metadata = JSON.parse(rtn_string);
	console.log(metadata);

	for (var i = 0; i < metadata["official_list"].length; i++) {
		$("#dropdown-menu").append(
			"<button class='dropdown-item'>" + 
			metadata["official_list"][i] + 
			"</button>"
		);
	}
});

/*********************
 ** Initiate Views ***
 *********************/

init_info_view();
init_map_view();
init_rank_view();

/*********************
 * Manual Responsive *
 *********************/

// additional listener for size-responsiblility of certain views
$(window).resize(function () { 
	update_rank_view(official_idx_dict[current_official]);
});

$(".dropdown-item").on("click", function () {
	current_official = $(this).html();
	update_map_view(official_idx_dict[current_official]);
	update_rank_view(official_idx_dict[current_official]);
	update_info_view(official_idx_dict[current_official]);
	$("#official-btn").html(current_official);
})
