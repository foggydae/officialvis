'use strict';

/********************
 * Global Variables *
 ********************/

var official_idx_dict = {
	"陈一新": 0,
	"李克强": 2,
	"习近平": 1
};


/********************
 ** Initiate Views **
 ********************/

init_map_view(0);

/*********************
 * Manual Responsive *
 *********************/

// additional listener for size-responsiblility of certain views
$(window).resize(function () { 
});

$(".dropdown-item").on("click", function () {
	update_map_view(official_idx_dict[$(this).html()]);
})
