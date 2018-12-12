function createMap(markers) {

  // Create the tile layer that will be the background of our map
  var streetMap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: API_KEY
});

  var dark = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.dark",
    accessToken: API_KEY
});


  // Create a baseMaps object to hold the streetmap layer
  var baseMaps = {
    "Street Map": streetMap,
    "Dark Map": dark
  };

  // Create an overlayMaps object to hold the markers layer
  var overlayMaps = {
    "Olympic Markers": markers
  };

  // Create the map object with options
  var map = L.map("map-id", {
    center: [0, 15.26],
    zoom: 2,
    layers: [streetMap, markers]
  });

  // Create a layer control, pass in the baseMaps and overlayMaps. Add the layer control to the map
  L.control.layers(baseMaps, overlayMaps, {
    collapsed: false
  }).addTo(map);

}


function createMarkers(response) {
  console.log(response)
    
  // var occurences = response.reduce(function (r, row) {
  //     r[row.Country] = ++r[row.Country] || 1;
  //     return r;
  // }, {});

  // var result = Object.keys(occurences).map(function (key) {
  //     return { Country: key, Medals: occurences[key] };
  // });

  // console.log(result);

  var medalCount = d3.nest()
  .key(function(d) {return d.Year;})
  .key(function(d) {return d.Country;})
  .key(function(d) {return d.Medal;})
  .rollup(function(v) {return {
    Medals: v.length,
    lat: d3.mean(v, function(d) { return d.CapitalLatitude; }),
    lng: d3.mean(v, function(d) { return d.CapitalLongitude; }),
  }; })
  .entries(response)
  .sort(function(a, b){ return d3.ascending(b.Medal, a.Medal)});

  console.log(medalCount);
  // console.log(medalCount[0]);
  // console.log(medalCount[32]);
  console.log(medalCount[0].values[0].values[1].value["Medals"]);
  console.log(medalCount[0].values[0].values[1].key);

  console.log(medalCount[0]); 

  var countries = medalCount;
  
  var countryMarkers =[];
  var dropdown_options = [];
    

  for (var index = 0; index < countries.length; index++) {
    var country = countries[index];

    for (i = 0; i < country.key.length; i++) {
      dropdown_options.push(country.key)
      console.log("Dropdown options are: " + dropdown_options)
    };

    // var selector = d3.select("#selDataset");
    //   console.log(selector)
    //   // Use the list of sample names to populate the select options
    //   d3.json("/data").then(option => {
    //     option.forEach((key) => {
    //       selector
    //         .append("option")
    //         .text(key)  
    //         .property("value", key);
    //     });

    // d3.select("dropdown-menu")
    // .selectAll("dropdown-item")
    // .enter()
    // .data(dropdown_options)
    // .append("option")
    // .attr("value", function(option) { return option.value; })
    // .text(function(option) { return option.value; });

    

    console.log(country);
    console.log(country.values[0]);
    console.log(country.values.length);
    console.log(country.values[0].values.length);

    var starterDate = "2014"

    if (country.key == starterDate) {
      for (var c = 0; c < country.values.length; c++) {
        if (country.values[c].values.length == 3) {
          console.log(country.values[c].values.length);
          var countryMarker = L.marker([country.values[c].values[0].value["lat"], country.values[c].values[0].value["lng"]])
            .bindPopup(
              "<h3>" + country.values[c].key + "</h3><h4>Year: " 
              + country.key + "</h4><h5>" 
              + country.values[c].values[0].key + " Medal(s): " + country.values[c].values[0].value["Medals"] 
              + "</h5><h5>" + country.values[c].values[1].key + " Medal(s): " + country.values[c].values[1].value["Medals"] 
              + "</h5><h5>" + country.values[c].values[2].key + " Medal(s): " + country.values[c].values[2].value["Medals"] + "</h5>");
            }
        else if (country.values[c].values.length == 2) {
          console.log(country.values[c].values.length);
          var countryMarker = L.marker([country.values[c].values[0].value["lat"], country.values[c].values[0].value["lng"]])
            .bindPopup(
              "<h3>" + country.values[c].key + "</h3><h4>Year: " 
              + country.key + "</h4><h5>" 
              + country.values[c].values[0].key + " Medal(s): " + country.values[c].values[0].value["Medals"] 
              + "</h5><h5>" + country.values[c].values[1].key + " Medal(s): " + country.values[c].values[1].value["Medals"] + "</h5>");
            }
        if (country.values[c].values.length == 1) {
          console.log(country.values[c].values.length);
          var countryMarker = L.marker([country.values[c].values[0].value["lat"], country.values[c].values[0].value["lng"]])
            .bindPopup(
              "<h3>" + country.values[c].key + "</h3><h4>Year: " 
              + country.key + "</h4><h5>" 
              + country.values[c].values[0].key + " Medal(s): " + country.values[c].values[0].value["Medals"] + "</h5>");
            }
    
        // Add the marker to the markers array
          countryMarkers.push(countryMarker);

  }}};
      createMap(L.layerGroup(countryMarkers));
};

d3.json("/data").then(createMarkers);

d3.select("dropdown-menu").on("change", createMarkers);

function updateYear(year) {
  var yearUpdate
}
// // Note to Self. init() populates the drop down selector.
// // init() also calls for buildCharts() and buildMetadata()
// function init(response) {
//   // Grab a reference to the dropdown select element
//   console.log(response);
//   var medalCount = d3.nest()
//   .key(function(d) {return d.Year;})
//   .rollup(function(v) {return {
//   }; })
//   .entries(response)
//   .sort(function(a, b){ return d3.ascending(b.Medal, a.Medal)});
//   console.log(medalCount);
  
//   var dropdown_options = [];

//   for (var index = 0; index < medalCount.length; index++) {
//     var medal = medalCount[index];

//     // for (i = 0; i < country.key.length; i++) {
//       dropdown_options.push(medal.key)
//   };
//   console.log("Dropdown options are: " + dropdown_options)

//   var selector = d3.select("#selDataset");
//   console.log(selector)
//   // Use the list of sample names to populate the select options
//   d3.json("/data").then(option => {
//     option.forEach((key) => {
//       selector
//         .append("option")
//         .text(key)  
//         .property("value", key);
//     });
//     console.log("use first key")
//     // Use the first sample from the list to build the initial plots
//     var firstKey = medalCount.key[0];
//     createMarkers(firstKey);
//   });
// };

function optionChanged(newKey) {
  // Fetch new data each time a new sample is selected
  createMarkers(newKey);
};

// Initialize the map
// d3.json("/data").then(init);