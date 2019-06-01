'use strict';

var valueline;
var rank_svg;
var x_scale, y_scale, xaxis_scale, yaxis_scale;
var view_width, view_height;
var x_axis, y_axis;
var margin = {
    "left": 75,
    "right": 25,
    "top": 20,
    "bottom": 20
};
var color_congress = ['#fff5f0','#fee0d2','#fcbba1','#fc9272','#fb6a4a','#ef3b2c','#cb181d','#a50f15','#67000d'];

var init_rank_view = function () {
    x_scale = d3.scale.linear();
    y_scale = d3.scale.linear();
    xaxis_scale = d3.scale.ordinal();
    yaxis_scale = d3.scale.ordinal();

    // Define the axes
    x_axis = d3.svg.axis().scale(xaxis_scale)
        .orient("bottom");
    y_axis = d3.svg.axis().scale(yaxis_scale)
        .orient("left");

    // Define the line
    valueline = d3.svg.line()
        .x(function(d) {return x_scale(new Date(d.date));})
        .y(function(d) {return y_scale(d.rank);});

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

    $.get("/api/get_line_data",  function (rtn_string) {
        var line_data = JSON.parse(rtn_string);
        console.log(line_data);

        var rank_path = line_data["rank_path"];
        var edu_paths = line_data["edu_path"];
        var rank_point = line_data["rank_point"];
        var edu_point = line_data["edu_point"];
        var congress_ranges = line_data["congress_ranges"]

        // Set the ranges
        x_scale.range([0, view_width]).domain([new Date(line_data["x_min"]), new Date(line_data["x_max"])]);
        y_scale.range([view_height, 0]).domain([line_data["y_min"], line_data["y_max"]]);
        xaxis_scale.rangePoints([0, view_width]).domain(line_data["x_list"]);
        yaxis_scale.rangePoints([view_height, 0]).domain(line_data["y_list"]);
        x_axis.tickValues(line_data["x_list"].slice(0, -1))

        rank_svg.selectAll("*").remove();
        var congress_group = rank_svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        var axis_group = rank_svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        var rank_group = rank_svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        var edu_group = rank_svg.append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        // rank
        rank_group.append("path")
            .attr("class", "line")
            .attr("d", valueline(rank_path));

        rank_group.selectAll("circle")
            .data(rank_point)
            .enter()
            .append("circle")
            .attr("cx", function(d) {
                return x_scale(new Date(d.date));
            })
            .attr("cy", function(d) {
                return y_scale(d.rank);
            })
            .attr("r", 4)
            .style({
                "opacity": 0.9,
                "fill-opacity": 0.8,
                "stroke-width": 2
            })
            .style("stroke", function (d) {
                return d.color;
            })
            .style("fill", function (d) {
                return d.color;
            });

        // education
        for (let i = 0; i < edu_paths.length; i++) {
            edu_group.append("path")
                .attr("class", "line")
                .attr("d", valueline(edu_paths[i]));
        }

        edu_group.selectAll("circle")
            .data(edu_point)
            .enter()
            .append("circle")
            .attr("cx", function(d) {
                return x_scale(new Date(d.date));
            })
            .attr("cy", function(d) {
                return y_scale(d.diploma);
            })
            .attr("r", 4)
            .style({
                "opacity": 0.9,
                "stroke-width": 2
            })
            .style("stroke", function (d) {
                return d.color;
            })
            .style("fill", function (d) {
                if (d.part_time == 1) {
                    return "transparent";
                } else {
                    return d.color;
                }
            });

        // Add the X Axis
        axis_group.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + y_scale(0) + ")")
            .call(x_axis);

        // Add the Y Axis
        axis_group.append("g")
            .attr("class", "y axis")
            .call(y_axis);

        for (let date = new Date(line_data["x_min"]); date < new Date(line_data["x_max"]);) {
            axis_group.append("line")
                .attr("x1", x_scale(date))
                .attr("y1", 0)
                .attr("x2", x_scale(date))
                .attr("y2", view_height)
                .style({
                    "stroke-width": 1,
                    "stroke": "lightgray",
                    "fill": "none",
                    "stroke-dasharray": 2,
                    "opacity": 0.5
                });
            date = new Date(date.getFullYear() + 5, 1, 1);
        }

        for (let rank = line_data["y_min"]; rank <= line_data["y_max"]; rank += 1) {
            axis_group.append("line")
                .attr("x1", 0)
                .attr("y1", y_scale(rank))
                .attr("x2", view_width)
                .attr("y2", y_scale(rank))
                .style({
                    "stroke-width": 1,
                    "stroke": "lightgray",
                    "fill": "none",
                    "stroke-dasharray": 2,
                    "opacity": 0.5
                });
        }

        congress_group.selectAll("rect")
            .data(congress_ranges)
            .enter()
            .append("rect")
            .attr("width", function (d) {
                return x_scale(new Date(d.end)) - x_scale(new Date(d.start));
            })
            .attr("height", function (d) {
                return y_scale(line_data["y_min"]) - y_scale(line_data["y_max"]);
            })
            .attr("x", function (d) {
                return x_scale(new Date(d.start));
            })
            .attr("y", function (d) {
                return y_scale(line_data["y_max"]);
            })
            .attr("fill", function (d, i) {
                return color_congress[i];
            })
            .attr("opacity", 0.15);

        congress_group.selectAll("text")
            .data(congress_ranges)
            .enter()
            .append("text")
            .attr("dx", function (d) {
                return (x_scale(new Date(d.start)) + x_scale(new Date(d.end))) / 2;
            })
            .attr("dy", y_scale(0) - 4)
            .html(function (d) {
                return d.title;
            })
            .style({
                "text-anchor": "middle",
                "font-size": 10,
                "opacity": 0.5
            })

        axis_group.append("text")
            .attr("dx", x_scale(new Date(line_data["x_max"])))
            .attr("dy", y_scale(0) + 15)
            .html("年份(年龄)")
            .style({
                "text-anchor": "middle",
                "font-size": 10
            })
    })
}
