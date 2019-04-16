'use strict';

/********************
 * Global Variables *
 ********************/

var official_idx_dict = {};
for (var i = 0; i < raw_data["data"].length; i++) {
	official_idx_dict[raw_data["data"][i]["name"]] = i;
	$("#dropdown-menu").append("<button class='dropdown-item'>" + raw_data["data"][i]["name"] + "</button>");
}

var current_official = "陈一新";


/********************
 ** Initiate Views **
 ********************/

init_map_view(0);
init_rank_view(0);


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
	$("#official-btn").html(current_official);
})
