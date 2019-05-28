'use strict';
var summary_margin = {
	"left": 10,
	"right": 10,
	"top": 5,
	"bottom": 10
};
var summary_svg;
var x_scale, y_scale;
// var rank_tmp_color = ['#ffffcc','#ffeda0','#fed976','#feb24c','#fd8d3c','#fc4e2a','#e31a1c','#bd0026','#800026'];
// var type_tmp_color = d3.scale.category20();

var init_summary_view = function () {
	x_scale = d3.scale.linear();
	y_scale = d3.scale.linear();

	// Adds the svg canvas
	summary_svg = d3.select("#summary-container")
		.append("svg");

	update_summary_view();
}

var update_summary_view = function () {

	// The size of the whole view
	var summary_view_width = $("#summary-container").width() - summary_margin.left - summary_margin.right;
	var summary_view_height = $("#summary-container").height() - summary_margin.top - summary_margin.bottom;

	summary_svg.attr("width", summary_view_width + summary_margin.left + summary_margin.right)
		.attr("height", summary_view_height + summary_margin.top + summary_margin.bottom);

	$.get("/api/get_summary_data", function (rtn_string) {
		var summary_data = JSON.parse(rtn_string);
		console.log(summary_data);

		var type_summary = summary_data["type_summary"];
		var rank_summary = summary_data["rank_summary"];

		x_scale.range([0, summary_view_width]).domain([0, 1]);
		y_scale.range([0, summary_view_height]).domain([0, 6]);

		console.log(summary_view_height);
		console.log(y_scale(1));

		summary_svg.selectAll("*").remove();
		var title_group = summary_svg.append("g")
			.attr("transform", "translate(" + summary_margin.left + "," + summary_margin.top + ")");
		var type_group = summary_svg.append("g")
			.attr("transform", "translate(" + summary_margin.left + "," + (summary_margin.top + y_scale(1)) + ")");
		var rank_group = summary_svg.append("g")
			.attr("transform", "translate(" + summary_margin.left + "," + (summary_margin.top + y_scale(4)) + ")");

		type_group.selectAll("rect")
			.data(type_summary)
			.enter()
			.append("rect")
			.attr("width", function (d) {
				return x_scale(d.percentage);
			})
			.attr("height", function (d) {
				return y_scale(3) - y_scale(1);
			})
			.attr("x", function (d) {
				return x_scale(d.start);
			})
			.attr("y", 0)
			.attr("fill", function (d) {
				return d.color;
			});

		type_group.selectAll("text")
			.data(type_summary)
			.enter()
			.append("text")
			.attr("transform", "rotate(-90)")
			.attr("dx", -1)
			.attr("dy", function (d) {
				return x_scale(d.start) + 8;
			})
			.html(function (d) {
		        var dx = d3.select(this).attr("dx");//get the x position of the text
		        var dy = d3.select(this).attr("dy");//get the y position of the text
		        var duration = "<tspan x="+dx+" dy=9>"+d.duration+"天</tspan>";
		        return d.title + duration;//appending it to the html
			})
			.style({
				"text-anchor": "end",
				"font-size": 8
			})

		rank_group.selectAll("rect")
			.data(rank_summary)
			.enter()
			.append("rect")
			.attr("width", function (d) {
				return x_scale(d.percentage);
			})
			.attr("height", function (d) {
				return y_scale(3) - y_scale(1);
			})
			.attr("x", function (d) {
				return x_scale(d.start);
			})
			.attr("y", 0)
			.attr("fill", function (d) {
				return d.color;
			});

		rank_group.selectAll("text")
			.data(rank_summary)
			.enter()
			.append("text")
			.attr("transform", "rotate(-90)")
			.attr("dx", -1)
			.attr("dy", function (d) {
				return x_scale(d.start) + 8;
			})
			.html(function (d) {
		        var dx = d3.select(this).attr("dx");//get the x position of the text
		        var dy = d3.select(this).attr("dy");//get the y position of the text
		        var duration = "<tspan x="+dx+" dy=9>"+d.duration+"天</tspan>";
		        return d.title + duration;//appending it to the html
			})
			.style({
				"text-anchor": "end",
				"font-size": 8
			})
			.style("fill", function (d) {
				if (d.rank_num < 6) {
					return "#000000";
				} else {
					return "#ffffff";
				}
			})

		title_group.append("text")
			.attr("dx", 0)
			.attr("dy", (y_scale(0) + y_scale(1)) / 2 + 2)
			.attr("alignment-baseline", "middle")
			.html("各归口年限：")
			.style({
				"font-size": 15
			});

		title_group.append("text")
			.attr("dx", 0)
			.attr("dy", (y_scale(3) + y_scale(4)) / 2 + 2)
			.attr("alignment-baseline", "middle")
			.html("各级别年限：")
			.style({
				"font-size": 15
			});
	})
}