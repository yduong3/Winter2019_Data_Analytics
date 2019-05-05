// from data.js
var tableData = data;

// Console.log the ufo data
console.log(tableData);


// Get a reference to the table body
var tbody = d3.select("tbody");

// Function to loop through data to append row, iterate through values and append cell, 
// Update each cell's text
function renderTable(datas) {
    datas.forEach((data) => {
    var row = tbody.append("tr");
    Object.values(data).forEach(value => {
      var cell = row.append("td");
      cell.text(value);
    });
  });
}

// UFO sighting data in table
renderTable(tableData);


// Select the filter button
var filter = d3.select("#filter-btn");

// Filter button handler
function filterButton() {

    // Prevent the page from refreshing
    d3.event.preventDefault();

    // Select the input element and get the raw HTML node
    // Get the value property of the input element
    var searchDate = d3.select("#datetime").property("value");
    var searchCity = d3.select("#city").property("value");
	var searchState = d3.select("#state").property("value");
	var searchCountry = d3.select("#country").property("value");
	var searchShape = d3.select("#shape").property("value");

    var filteredDatas = data;

    if (searchDate != ""){
    	filteredDatas = filteredDatas.filter(filterdata => filterdata.datetime === searchDate);
    }
    if (searchCity != ""){
    	filteredDatas = filteredDatas.filter(filterdata => filterdata.city.toLowerCase() === searchCity.toLowerCase());
    }
    if (searchState != ""){
        filteredDatas = filteredDatas.filter(filterdata => filterdata.state.toLowerCase() === searchState.toLowerCase());
    }
    if (searchCountry != ""){
        filteredDatas = filteredDatas.filter(filterdata => filterdata.country.toLowerCase() === searchCountry.toLowerCase());
    }
    if (searchShape != ""){
        filteredDatas = filteredDatas.filter(filterdata => filterdata.shape.toLowerCase() === searchShape.toLowerCase());
    }

    tbody.html("");
    renderTable(filteredDatas);
}
// Event listner for filter button
filter.on("click", filterButton);


// Select the reset button
var reset = d3.select("#reset-btn");

// Reset button handler
reset.on("click", function() {
    tbody.html(renderTable(tableData))
});