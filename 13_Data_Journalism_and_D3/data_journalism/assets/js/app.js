var svgWidth = 960;
var svgHeight = 500;

var margin = {
    top: 20,
    right: 40,
    bottom: 80,
    left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

function responsivefy(svg) {
    // get container + svg aspect ratio
    var container = d3.select(svg.node().parentNode),
        width = parseInt(svg.style("width")),
        height = parseInt(svg.style("height")),
        aspect = width / height;

    // add viewBox and preserveAspectRatio properties,
    // and call resize so that svg resizes on inital page load
    svg.attr("viewBox", "0 0 " + width + " " + height)
        .attr("perserveAspectRatio", "xMinYMid")
        .call(resize);

    d3.select(window).on("resize." + container.attr("id"), resize);

    // get width of container and resize svg to fit it
    function resize() {
        var targetWidth = parseInt(container.style("width"));
        svg.attr("width", targetWidth);
        svg.attr("height", Math.round(targetWidth / aspect));
    }
}

// Create an SVG wrapper, append an SVG group that will hold our chart,
// and shift the latter by left and top margins.
var svg = d3
    .select("#scatter")
    .classed("chart",true)
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight)
    .call(responsivefy);

// Append an SVG group
var chartGroup = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Initial Params
var chosenXAxis = "poverty";
var chosenYAxis = "healthcare";

// function used for updating x-scale var upon click on axis label
function xScale(ACSData, chosenXAxis) {
// create scales
var xLinearScale = d3.scaleLinear()
    .domain([d3.min(ACSData, d => d[chosenXAxis]) * 0.9,
    d3.max(ACSData, d => d[chosenXAxis]) * 1.1
    ])
    .range([0, width]);

return xLinearScale;
}

// function used for updating y-scale var upon click on axis label
function yScale(ACSData, chosenYAxis) {
    // create scales
    var yLinearScale = d3.scaleLinear()
        .domain([d3.min(ACSData, d => d[chosenYAxis]) * 0.9,
        d3.max(ACSData, d => d[chosenYAxis]) * 1.1
        ])
        .range([height, 0]);
    
    return yLinearScale;
}

// function used for updating xAxis var upon click on axis label
function renderxAxes(newXScale, xAxis) {
var bottomAxis = d3.axisBottom(newXScale);

xAxis.transition()
    .duration(1000)
    .ease(d3.easeBack)
    .call(bottomAxis);

return xAxis;
}

// function used for updating yAxis var upon click on axis label
function renderyAxes(newYScale, yAxis) {
var leftAxis = d3.axisLeft(newYScale);
    
    yAxis.transition()
        .duration(1000)
        .ease(d3.easeBack)
        .call(leftAxis);
    
    return yAxis;
    }

// function used for updating x circles group with a transition to
// new circles
function renderXstateCircle(XstateCircle, newXScale, chosenXaxis) {

    XstateCircle.transition()
    .duration(1000)
    .ease(d3.easeBack)
    .attr("cx", d => newXScale(d[chosenXAxis]))

return XstateCircle;
}

// function used for updating x circles text group with a transition to
// new circles
function renderXstateText(XstateText, newXScale, chosenXaxis) {

    d3.selectAll(".stateText").transition()
    .duration(1000)
    .ease(d3.easeBack)
    .attr("x", d => newXScale(d[chosenXAxis]))

return XstateText;
}

// function used for updating y circles group with a transition to
// new circles
function renderYstateCircle(YstateCircle, newYScale, chosenYaxis) {

    YstateCircle.transition()
    .duration(1000)
    .ease(d3.easeBack)
    .attr("cy", d => newYScale(d[chosenYAxis]))

return YstateCircle;
}

// function used for updating Y circles text group with a transition to
// new circles
function renderYstateText(YstateText, newYScale, chosenYaxis) {

    d3.selectAll(".stateText").transition()
    .duration(1000)
    .ease(d3.easeBack)
    .attr("y", d => newYScale(d[chosenYAxis])+4);

return YstateText;
}

// function used for updating circles group with new tooltip
function updateToolTip(chosenYAxis, chosenXAxis, stateCircle, stateText) {

var toolTip = d3.tip()
    .attr("class", "d3-tip")
    .offset([80, -60])
    .html(function(d) {
        if(chosenXAxis === "poverty")
            return (`${d.state}<br>${chosenYAxis}: ${d[chosenYAxis]}%
                <br>${chosenXAxis}: ${d[chosenXAxis]}%`)
        else if (chosenXAxis === "income")
            return (`${d.state}<br>${chosenYAxis}: ${d[chosenYAxis]}%
                <br>${chosenXAxis}: $${d[chosenXAxis]}`)
        else
            return (`${d.state}<br>${chosenYAxis}: ${d[chosenYAxis]}%
                <br>${chosenXAxis}: ${d[chosenXAxis]}`)
    });

stateCircle.call(toolTip);
stateCircle.on("mouseover", toolTip.show).on("mouseout", toolTip.hide);

d3.selectAll(".stateText").call(toolTip);
d3.selectAll(".stateText").on("mouseover", toolTip.show).on("mouseout", toolTip.hide);

return stateCircle;
return stateText;
}

// Retrieve data from the CSV file and execute everything below
d3.csv("assets/data/data.csv").then(function(ACSData) {

// parse data
ACSData.forEach(function(d) {
    d.poverty = +d.poverty;
    d.healthcare = +d.healthcare;
    d.age = +d.age;
    d.income = +d.income;
    d.obesity = +d.obesity;
    d.smokes = +d.smokes;
});

// Create scale functions
var xLinearScale = xScale(ACSData, chosenXAxis);
var yLinearScale = yScale(ACSData, chosenYAxis);

// Create initial axis functions
var bottomAxis = d3.axisBottom(xLinearScale);
var leftAxis = d3.axisLeft(yLinearScale);

// append x axis
var xAxis = chartGroup.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(bottomAxis);

// append y axis
var yAxis = chartGroup.append("g")
    .call(leftAxis);

// append initial circles
var stateCircle = chartGroup.selectAll("circle")
    .data(ACSData)
    .enter()
    .append("circle")
    .classed("stateCircle",true)
    .attr("cx", d => xLinearScale(d[chosenXAxis]))
    .attr("cy", d => yLinearScale(d[chosenYAxis]))
    .attr("r", "10")

var stateText = chartGroup.append("g").selectAll("text")
    .data(ACSData)
    .enter()
    .append("text")
    .text(d => d.abbr)
    .classed("stateText",true)
    .attr("x", d => xLinearScale(d[chosenXAxis]))
    .attr("y", d => yLinearScale(d[chosenYAxis])+4)
    .attr("font-size", "11px")

// Create group for  3 x axis labels
var xlabelsGroup = chartGroup.append("g")
    .attr("transform", `translate(${width / 2}, ${height + 20})`);

var povertyLabel = xlabelsGroup.append("text")
    .attr("x", 0)
    .attr("y", 20)
    .attr("value", "poverty") // value to grab for event listener
    .classed("aText active", true)
    .text("In Poverty (%)");

var ageLabel = xlabelsGroup.append("text")
    .attr("x", 0)
    .attr("y", 40)
    .attr("value", "age") // value to grab for event listener
    .classed("aText inactive", true)
    .text("Age (Median)");

var incomeLabel = xlabelsGroup.append("text")
    .attr("x", 0)
    .attr("y", 60)
    .attr("value", "income") // value to grab for event listener
    .classed("aText inactive", true)
    .text("Household Income (Median)");

// Create group for 3 y axis lables
var ylabelsGroup = chartGroup.append("g")
    .attr("transform", "rotate(-90)")
    .attr("dy", "1em")

var healthcareLabel = ylabelsGroup.append("text")
    .attr("y", 0 - margin.left + 60)
    .attr("x", 0 - (height / 2))
    .attr("value", "healthcare") // value to grab for event listener
    .classed("aText active", true)
    .text("Lacks Healthcare (%)");

var smokesLabel = ylabelsGroup.append("text")
    .attr("y", 0 - margin.left + 40)
    .attr("x", 0 - (height / 2))
    .attr("value", "smokes") // value to grab for event listener
    .classed("aText inactive", true)
    .text("Smokes (%)");

var obesityLabel = ylabelsGroup.append("text")
    .attr("y", 0 - margin.left + 20)
    .attr("x", 0 - (height / 2))
    .attr("value", "obesity") // value to grab for event listener
    .classed("aText inactive", true)
    .text("Obesity (%)");

// updateToolTip function above csv import

var stateCircle = updateToolTip(chosenYAxis,chosenXAxis,stateCircle,stateText);
var stateText = updateToolTip(chosenYAxis,chosenXAxis,stateCircle,stateText);

// x axis labels event listener
xlabelsGroup.selectAll("text")
    .on("click", function() {
    // get value of selection
    var value = d3.select(this).attr("value");
    if (value !== chosenXAxis) {

        // replaces chosenXaxis with value
        chosenXAxis = value;

        // functions here found above csv import
        // updates x scale for new data
        xLinearScale = xScale(ACSData, chosenXAxis);

        // updates x axis with transition
        xAxis = renderxAxes(xLinearScale, xAxis);

        // updates circles with new x values
        stateCircle = renderXstateCircle(stateCircle, xLinearScale, chosenXAxis);
        stateText = renderXstateText(stateText, xLinearScale, chosenXAxis);

        // updates tooltips with new info
        stateCircle = updateToolTip(chosenYAxis, chosenXAxis, stateCircle, stateText);
        stateText = updateToolTip(chosenYAxis, chosenXAxis, stateCircle, stateText);

        // changes classes to change bold text
        if (chosenXAxis === "poverty") {
        povertyLabel
            .classed("active", true)
            .classed("inactive", false);
        ageLabel
            .classed("active", false)
            .classed("inactive", true);
        incomeLabel
            .classed("active", false)
            .classed("inactive", true);
        }
        else if (chosenXAxis === "age") {
        povertyLabel
            .classed("active", false)
            .classed("inactive", true);
        ageLabel
                .classed("active", true)
                .classed("inactive", false);
        incomeLabel
                .classed("active", false)
                .classed("inactive", true);
            }
        else {
        povertyLabel
            .classed("active", false)
            .classed("inactive", true);
        ageLabel
            .classed("active", false)
            .classed("inactive", true);
        incomeLabel
            .classed("active", true)
            .classed("inactive", false);
        }
    }
    });

// y axis labels event listener
ylabelsGroup.selectAll("text")
    .on("click", function() {
    // get value of selection
    var value = d3.select(this).attr("value");
    if (value !== chosenYAxis) {

        // replaces chosenYaxis with value
        chosenYAxis = value;

        // functions here found above csv import
        // updates y scale for new data
        yLinearScale = yScale(ACSData, chosenYAxis);

        // updates y axis with transition
        yAxis = renderyAxes(yLinearScale, yAxis);

        // updates circles with new y values
        stateCircle = renderYstateCircle(stateCircle, yLinearScale, chosenYAxis);
        stateText = renderYstateText(stateText, yLinearScale, chosenYAxis);

        // updates tooltips with new info
        stateCircle = updateToolTip(chosenYAxis, chosenXAxis, stateCircle, stateText);
        stateText = updateToolTip(chosenYAxis, chosenXAxis, stateCircle, stateText);

        // changes classes to change bold text
        if (chosenYAxis === "healthcare") {
        healthcareLabel
            .classed("active", true)
            .classed("inactive", false);
        smokesLabel
            .classed("active", false)
            .classed("inactive", true);
        obesityLabel
            .classed("active", false)
            .classed("inactive", true);
        }
        else if (chosenYAxis === "smokes") {
        healthcareLabel
            .classed("active", false)
            .classed("inactive", true);
        smokesLabel
                .classed("active", true)
                .classed("inactive", false);
        obesityLabel
                .classed("active", false)
                .classed("inactive", true);
            }
        else {
        healthcareLabel
            .classed("active", false)
            .classed("inactive", true);
        smokesLabel
            .classed("active", false)
            .classed("inactive", true);
        obesityLabel
            .classed("active", true)
            .classed("inactive", false);
        }
    }
    });
});