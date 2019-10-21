var width = 800;
var height = 300;
var axisHeight = 20;

var svg = d3.select("body").append("svg");
svg
    .attr("width", width)
    .attr("height", height + axisHeight);

var dataset = [];
for (var i = 0; i < 25; i++) {
    var newNumber = Math.random() * (height - 1) + 1;
    dataset.push(newNumber);
}

var barWidth = width/dataset.length;
var padding = barWidth/10.0;

svg
    .selectAll("rect")
    .data(dataset)
    .enter()
    .append("rect")
    .attr({
        'x':    function(d, i) {return i*barWidth;},
        'y':    function(d)    {return height - d;},
        width:  barWidth - padding,
        height: function(d)    {return d;},
    })
    .on("mouseover", function (d) { d3.select(this).attr("fill", "orange") })
    .on("mouseout",  function (d) { d3.select(this).attr("fill", "black") })
    .text(function(d) {return d;});

var scale = d3
    .scale
    .linear()
    .domain([0, dataset.length])
    .range([0, width]);

var axis = d3.svg.axis()
    .scale(scale)
    .orient("bottom");

svg.append("g")
    .attr("transform", "translate(0," + (height) + ")")
    .call(axis);
