function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel
  var selector = d3.select("#sample-metadata");
  // Use `d3.json` to fetch the metadata for a sample
  d3.json("/metadata/" + sample).then((metadata) => {
    console.log(metadata);

    // Use d3 to select the panel with id of `#sample-metadata`

    // Use `.html("") to clear any existing metadata
    selector.html("");

    d3.entries(metadata)
      .forEach((d) => {
        selector
          .append("li")
          .text(`${d.key} : ${d.value}`)
        console.log(d);
      });
    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    console.log(d3.entries(metadata));
    // BONUS: Build the Gauge Chart
    // buildGauge(data.WFREQ);
  });
};

function buildCharts(sample) {

  // @TODO: Use `d3.json` to fetch the sample data for the plots
  d3.json("/samples/" + sample).then((data) => {
    //data contains sample 'otu _ids', 'otu_labels', and 'sample_values'
    var dict = [];
    //Use for loop to fill dictionary
    for (i = 0; i < data.otu_ids.length; i++) {
      dict.push({ 'otu_id': data.otu_ids[i], 'otu_label': data.otu_labels[i], 'sample_value': data.sample_values[i] });
    };
    //sort dictionary by sample value descending order.
    dict.sort(function (a, b) {
      return b.sample_value - a.sample_value;
    });

    // Slice the first 10 objects for plotting. Grab top 10
    dict = dict.slice(0, 10);
    var ids = dict.map(d => d.otu_id);
    var chartlabels = dict.map(d => d.otu_label);
    var chartvalues = dict.map(d => d.sample_value);
    console.log(ids);
    console.log(chartlabels);
    console.log(chartvalues);
    console.log(data);
    console.log(dict);

    // @TODO: Build a Pie Chart
    var pie_trace = {
      labels: ids,
      values: chartvalues,
      hovertext: chartlabels,
      type: 'pie',
      title: `Pie Chart ${sample}`
    };
    var pie_data = [pie_trace];
    var pie_layout = {
      height: 550,
      width: 550
    };
    Plotly.newPlot("pie", pie_data, pie_layout);

    // @TODO: Build a Bubble Chart using the sample data
    var bubble_trace = {
      x: ids,
      y: chartvalues,
      hovertext: chartlabels,
      mode: 'markers',
      marker: {
        size: chartvalues,
        color: ids,
        opacity: 0.4
      }
    };
    var bubble_data = [bubble_trace];
    var bubble_layout = {
      showlegend: false,
      height: 500,
      width: 1200,
      title: `Bubble Chart ${sample}`,
      xaxis: {
        title: "otu_id"
      },
    };
    Plotly.newPlot("bubble", bubble_data, bubble_layout);
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
  });
};
//Note to Self. init() populates the drop down selector.
// init() also calls for buildCharts() and buildMetadata()
function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
};

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
};

// Initialize the dashboard
init();
