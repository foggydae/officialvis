'use strict';

var valueline;
var rank_svg;
var xaxis_scale, yaxis_scale;
var view_width, view_height;
var x_axis, y_axis;
var margin = {
    "left": 20,
    "right": 10,
    "top": 10,
    "bottom": 20
}

var init_rank_view = function (official_idx) {
    view_width = $("#rank-container").width() - margin.left - margin.right;
    view_height = $("#rank-container").height() - margin.top - margin.bottom;

    // Set the ranges
    // xaxis_scale = d3.time.scale().range([0, view_width]);
    xaxis_scale = d3.scale.linear().range([0, view_width]);
    yaxis_scale = d3.scale.linear().range([view_height, 0]);

    // Define the axes
    x_axis = d3.svg.axis().scale(xaxis_scale)
        .orient("bottom").ticks(10);

    y_axis = d3.svg.axis().scale(yaxis_scale)
        .orient("left").ticks(10);

    // Define the line
    valueline = d3.svg.line()
        .x(function(d) { return xaxis_scale(d.age); })
        .y(function(d) { return yaxis_scale(d.rank); });

    // Adds the svg canvas
    rank_svg = d3.select("#rank-container")
        .append("svg")
        .attr("width", view_width + margin.left + margin.right)
        .attr("height", view_height + margin.top + margin.bottom);

    update_rank_view(official_idx);
}


var update_rank_view = function (official_idx) {

    var official_data = prepare_data(raw_data, official_idx);
    var rank_data = official_data["rank_data"];
    var promo_data = official_data["promo_data"];

    console.log(promo_data);

    xaxis_scale.domain([15, 75]);
    yaxis_scale.domain([0, 11]);

    rank_svg.selectAll("*").remove();
    var rank_group = rank_svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    rank_group.append("path")
        .attr("class", "line")
        .attr("d", valueline(rank_data));

    rank_group.selectAll("circle")
        .data(promo_data)
        .enter()
        .append("circle")
        .attr("cx", function(d) {
            return xaxis_scale(d.age);
        })
        .attr("cy", function(d) {
            return yaxis_scale(d.rank);
        })
        .attr("r", 3)
        .style({
            "opacity": 0.9,
            "stroke": "darkgreen",
            "fill": "transparent",
            "stroke-width": 2
        });

    // Add the X Axis
    rank_group.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + view_height + ")")
        .call(x_axis);

    // Add the Y Axis
    rank_group.append("g")
        .attr("class", "y axis")
        .call(y_axis);
}
