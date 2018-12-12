// Fetch the JSON data from flask server, (path is '/data') and console log it to check that we are able to read it into the browser/dom
const url = "/data";
d3.json(url).then(function(data) {console.log(data);});

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
  
      // for (i = 0; i < country.key.length; i++) {
        dropdown_options.push(country.key)
        console.log("Dropdown options are: " + dropdown_options)
      // };
  
      var options = d3.select("dropdown")
      .selectAll("option")
      .data(dropdown_options)
      .enter()
      .append("option")
      .attr("value", function(option) { return option.value; })
      .text(function(option) { return option.text; });
  
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
  
  d3.json("/data", createMarkers);

Plotly.d3.json(url, function (err, data) {
  // Create a lookup table to sort and regroup the columns of data,
  // first by year, then by country:
  var lookup = {};
  function getData(Year, Country) {
    var byYear, trace;
    if (!(byYear = lookup[Year])) {;
      byYear = lookup[Year] = {};
    }
	 // If a container for this year + country doesn't exist yet,
	 // then create one:
    if (!(trace = byYear[Country])) {
      trace = byYear[Country] = {
        x: [],
        y: [],
        id: [],
        text: [],
        marker: {size: []}
      };
    }
    return trace;
  }

  // Go through each row, get the right trace, and append the data:
  for (var i = 0; i < data.length; i++) {
    var datum = data[i];
    var trace = getData(datum.Year, datum.Country);
    trace.text.push(datum.Country);
    trace.id.push(datum.Country);
    trace.x.push(datum.lifeExp);
    trace.y.push(datum.gdpPercap);
    trace.marker.size.push(datum.pop);
  }

  // Get the group names:
  var years = Object.keys(lookup);
  // In this case, every year includes every continent, so we
  // can just infer the continents from the *first* year:
  var firstYear = lookup[years[0]];
  var continents = Object.keys(firstYear);

  // Create the main traces, one for each continent:
  var traces = [];
  for (i = 0; i < continents.length; i++) {
    var data = firstYear[continents[i]];
	 // One small note. We're creating a single trace here, to which
	 // the frames will pass data for the different years. It's
	 // subtle, but to avoid data reference problems, we'll slice
	 // the arrays to ensure we never write any new data into our
	 // lookup table:
    traces.push({
      name: continents[i],
      x: data.x.slice(),
      y: data.y.slice(),
      id: data.id.slice(),
      text: data.text.slice(),
      mode: 'markers',
      marker: {
        size: data.marker.size.slice(),
        sizemode: 'area',
        sizeref: 200000
      }
    });
  }

  // Create a frame for each year. Frames are effectively just
  // traces, except they don't need to contain the *full* trace
  // definition (for example, appearance). The frames just need
  // the parts the traces that change (here, the data).
  var frames = [];
  for (i = 0; i < years.length; i++) {
    frames.push({
      name: years[i],
      data: continents.map(function (continent) {
        return getData(years[i], continent);
      })
    })
  }

  // Now create slider steps, one for each frame. The slider
  // executes a plotly.js API command (here, Plotly.animate).
  // In this example, we'll animate to one of the named frames
  // created in the above loop.
  var sliderSteps = [];
  for (i = 0; i < years.length; i++) {
    sliderSteps.push({
      method: 'animate',
      label: years[i],
      args: [[years[i]], {
        mode: 'immediate',
        transition: {duration: 300},
        frame: {duration: 300, redraw: false},
      }]
    });
  }

  var layout = {
    xaxis: {
      title: '',
      range: [30, 85]
    },
    yaxis: {
      title: 'Medals won',
      type: 'log'
    },
    hovermode: 'closest',
	 // We'll use updatemenus (whose functionality includes menus as
	 // well as buttons) to create a play button and a pause button.
	 // The play button works by passing `null`, which indicates that
	 // Plotly should animate all frames. The pause button works by
	 // passing `[null]`, which indicates we'd like to interrupt any
	 // currently running animations with a new list of frames. Here
	 // The new list of frames is empty, so it halts the animation.
    updatemenus: [{
      x: 0,
      y: 0,
      yanchor: 'top',
      xanchor: 'left',
      showactive: false,
      direction: 'left',
      type: 'buttons',
      pad: {t: 87, r: 10},
      buttons: [{
        method: 'animate',
        args: [null, {
          mode: 'immediate',
          fromcurrent: true,
          transition: {duration: 300},
          frame: {duration: 500, redraw: false}
        }],
        label: 'Play'
      }, {
        method: 'animate',
        args: [[null], {
          mode: 'immediate',
          transition: {duration: 0},
          frame: {duration: 0, redraw: false}
        }],
        label: 'Pause'
      }]
    }],
	 // Finally, add the slider and use `pad` to position it
	 // nicely next to the buttons.
    sliders: [{
      pad: {l: 130, t: 55},
      currentvalue: {
        visible: true,
        prefix: 'Year:',
        xanchor: 'right',
        font: {size: 20, color: '#666'}
      },
      steps: sliderSteps
    }]
  };

  // Create the plot:
  Plotly.plot('myDiv', {
    data: traces,
    layout: layout,
    frames: frames,
  });
});