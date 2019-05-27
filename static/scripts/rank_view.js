'use strict';

var valueline;
var rank_svg;
var xaxis_scale, yaxis_scale;
var view_width, view_height;
var x_axis, y_axis;
var margin = {
    "left": 20,
    "right": 20,
    "top": 10,
    "bottom": 10
}


var init_rank_view = function () {
    xaxis_scale = d3.scale.linear();
    yaxis_scale = d3.scale.linear();

    // Define the axes
    x_axis = d3.svg.axis().scale(xaxis_scale).innerTickSize(6)
        .orient("bottom").tickValues([15,20,25,30,35,40,45,50,55,60,65,70,75]);

    y_axis = d3.svg.axis().scale(yaxis_scale)
        .orient("left").ticks(15);

    // Define the line
    valueline = d3.svg.line()
        .x(function(d) {return xaxis_scale(d.age);})
        .y(function(d) {return yaxis_scale(d.rank);});

    // Adds the svg canvas
    rank_svg = d3.select("#rank-container")
        .append("svg");

    update_rank_view();
}


var update_rank_view = function () {

    // The size of the whole view
    view_width = $("#rank-container").width() - margin.left - margin.right;
    view_height = $("#rank-container").height() - margin.top - margin.bottom;

    rank_svg.attr("width", view_width + margin.left + margin.right)
        .attr("height", view_height + margin.top + margin.bottom);

    // Set the ranges
    // xaxis_scale = d3.time.scale().range([0, view_width]);
    xaxis_scale.range([0, view_width]).domain([10, 80]);
    yaxis_scale.range([view_height, 0]).domain([-5, 11]);

    $.get("/api/get_line_data",  function (rtn_string) {
        var line_data = JSON.parse(rtn_string);
        console.log(line_data);
    
        var rank_data = line_data["rank_path"];
        var diploma_data = line_data["edu_path"];
        var promo_data = line_data["rank_point"];
        var edu_data = line_data["edu_point"];

        rank_svg.selectAll("*").remove();
        var rank_group = rank_svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        var edu_group = rank_svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        var axis_group = rank_svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        // rank
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

        // education
        for (let i = 0; i < diploma_data.length; i++) {
            console.log(diploma_data[i]);
            edu_group.append("path")
                .attr("class", "line")
                .attr("d", valueline(diploma_data[i]));
        }

        edu_group.selectAll("circle")
            .data(edu_data)
            .enter()
            .append("circle")
            .attr("cx", function(d) {
                return xaxis_scale(d.age);
            })
            .attr("cy", function(d) {
                return yaxis_scale(d.diploma);
            })
            .attr("r", 3)
            .style({
                "opacity": 0.9,
                "stroke": "darkred",
                "fill": "transparent",
                "stroke-width": 2
            });

        // Add the X Axis
        axis_group.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + yaxis_scale(0) + ")")
            .call(x_axis);

        // Add the Y Axis
        axis_group.append("g")
            .attr("class", "y axis")
            .call(y_axis);

        for (let age = 15; age < 80; age += 5) {
            axis_group.append("line")
                .attr("x1", xaxis_scale(age))
                .attr("y1", 0)
                .attr("x2", xaxis_scale(age))
                .attr("y2", view_height)
                .style({
                    "stroke-width": 1,
                    "stroke": "lightgray",
                    "fill": "none",
                    "stroke-dasharray": 2,
                    "opacity": 0.5
                });
        }

        for (let rank = -5; rank < 12; rank += 1) {
            axis_group.append("line")
                .attr("x1", 0)
                .attr("y1", yaxis_scale(rank))
                .attr("x2", view_width)
                .attr("y2", yaxis_scale(rank))
                .style({
                    "stroke-width": 1,
                    "stroke": "lightgray",
                    "fill": "none",
                    "stroke-dasharray": 2,
                    "opacity": 0.5
                });
        }

        axis_group.append("text")
            .attr("dx", xaxis_scale(80))
            .attr("dy", yaxis_scale(0) + 15)
            .html("年龄")
            .style({
                "text-anchor": "middle",
                "font-size": 10
            })
    })
}
