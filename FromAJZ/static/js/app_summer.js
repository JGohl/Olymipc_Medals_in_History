
function buildCharts(year, sport, medal) {
    d3.json("/summer/" + year + "/" + sport + "/" + medal).then((data) => {
        console.log(data);
        console.log(d3.entries(data));
        dict = data;
        dict = dict.slice(0,10);
        var countries = dict.map(d=>d.Country);
        console.log(countries);
        var medals = dict.map(d=>d.Medal);
        console.log(medals);

        // @TODO: Build a Pie Chart
    var pie_trace = {
        labels: countries,
        values: medals,
        type: 'pie',
        title: `Summer ${year} ${sport} ${medal} Medals`
      };
      var pie_data = [pie_trace];
      var pie_layout = {
        height: 550,
        width: 550
      };
      Plotly.newPlot("pie_ajz", pie_data, pie_layout);
    });
};

function init() {
    // Grab a reference to the dropdown select element
    // Use the list of sample names to populate the select options
    d3.json("/summer/filters").then((filters) => {
        years = filters.years
        console.log(years);
        sports = filters.sports
        console.log(sports);
        years.forEach((year) => {
            selector_year
                .append("option")
                .text(year)
                .property("value", year);
        });
        sports.forEach((sport) => {
            selector_sport
                .append("option")
                .text(sport)
                .property("value", sport);
        });
        // Use the first values from the lists to build the initial plots
        const firstYear = years[0];
        console.log(firstYear);
        const firstSport = sports[0];
        console.log(firstSport);
        const firstMedal = "Gold";
        console.log(firstMedal);
        buildCharts(firstYear, firstSport, firstMedal);
    });
};

function optionChanged() {
    var newYear = selector_year.node().value;
    var newSport = selector_sport.node().value;
    var newMedal = selector_medal.node().value;
    // Fetch new data each time a new sample is selected
    buildCharts(newYear, newSport, newMedal);
};
var selector_year = d3.select("#sel_year_ajz");
var selector_sport = d3.select("#sel_sport_ajz");
var selector_medal = d3.select("#sel_medal_ajz");
var dict = [];
var years = [];
var sports = [];
init();