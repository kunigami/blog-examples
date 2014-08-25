var width = 300;
var height = 300;

var svg = d3.select("body").append("svg");
svg
    .attr("width", width)
    .attr("height", height);

var dataset = [ 5, 10, 20, 45, 6, 25 ];

var outerRadius = width / 2;
var innerRadius = 0;
var arc = d3.svg.arc()
                .innerRadius(innerRadius)
                .outerRadius(outerRadius);

var pie = d3.layout.pie();

var arcs = svg.selectAll("g.arc")
        .data(pie(dataset))
        .enter()
        .append("g")
        .attr("class", "arc")
        .attr("transform", "translate(" + outerRadius + ", " + outerRadius + ")");

//Draw arc paths
var color = d3.scale.category10();

arcs.append("path")
    .attr("fill", function(d, i) {
        console.log(d);
        return color(i);
    })
    .attr("stroke", "white")
    .attr("d", arc);

// Trick to displace the labels. The centroid is too close from the
// center IMO. By pretending we have an innerRadius, we can move the
// labels closer to the edge.
var arcLabel = d3.svg.arc()
    .innerRadius(2*outerRadius/3)
    .outerRadius(outerRadius);

arcs.append("text")
    .attr("transform", function(d) {
        return "translate(" + arcLabel.centroid(d) + ")";
    })
    .attr("text-anchor", "middle")
    .attr("fill", "white")
    .text(function(d) {
        return d.value;
    });
