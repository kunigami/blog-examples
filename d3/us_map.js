var w = 800;
var h = 500;

var svg = d3.select("body").append("svg");
svg
    .attr("width", w)
    .attr("height", h);

var projection = d3.geo.albersUsa()
    .translate([w/2, h/2])
    .scale([1000]);

var USMap = {

    run: function() {
        this.init();
        d3.json(
	"data/us-states.json",
	this.handleGeoJSONLoaded.bind(this)
        );
    },

    init: function() {
        this.color = d3.scale.quantize()
            .range([
	    "rgb(237,248,233)",
	    "rgb(186,228,179)",
                "rgb(116,196,118)",
	    "rgb(49,163,84)",
	    "rgb(0,109,44)"
	]);
    },

    handleGeoJSONLoaded: function(json) {
        this._geoJSON = json;
        d3.csv(
	"data/us-ag-productivity-2004.csv",
	this.handleUSDataLoaded.bind(this)
        );
    },

    handleUSDataLoaded: function(data) {
        this.color.domain([
            d3.min(data, function(d) { return d.value; }),
            d3.max(data, function(d) { return d.value; })
        ]);
        this.joinWithData(data);
        this.render();
    },

    joinWithData: function(data) {
        // Index geo objects by state name
        geoByState = {};
        this._geoJSON.features.forEach(function(feature) {
	var jsonState = feature.properties.name;
	geoByState[jsonState] = feature;
        });
        // Add the value attribute to the geoJSON
        data.forEach(function(row) {
	var dataState = row.state;
	geoByState[dataState].properties.value = parseFloat(row.value);
        });
    },

    render: function() {
        var path = d3.geo.path()
            .projection(projection);
        svg.selectAll("path")
	.data(this._geoJSON.features)
	.enter()
	.append("path")
	.attr("d", path)
	.style("fill", function(d) {
	    var value = d.properties.value;
                return (value) ? this.color(value) : '#ccc';
	}.bind(this));

        d3.csv(
	"data/us-cities.csv",
	this.handleCityDataLoaded.bind(this)
        );
    },

    handleCityDataLoaded: function(data) {
        svg.selectAll("circle")
	.data(data)
	.enter()
	.append("circle")
	.attr("cx", function(d) {
                return projection([d.lon, d.lat])[0];
	})
	.attr("cy", function(d) {
                return projection([d.lon, d.lat])[1];
	})
	.attr("r", function(d) {
                return Math.sqrt(parseInt(d.population) * 0.0004);
	})
	.style("fill", "gray")
	.style("stroke", "black")
	.style("opacity", 0.75);
    }
};

USMap.run();
