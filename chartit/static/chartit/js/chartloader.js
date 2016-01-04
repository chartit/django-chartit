// jQuery function to create a chart for each of the HighCharts Chart Options
// JSON object (_chartit_hco_array) passed to web page from the view.
$(document).ready(function() {
	$.each(_chartit_hco_array, function(index, chartoptions) {
		chart = new Highcharts.Chart(chartoptions);
	});
});
