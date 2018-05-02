var math = require("mathjs");
var jsregression = require("js-regression");

var svg = d3.select("#crimeApprox");
const width = svg.attr("width");
const height = svg.attr("height");

//paddings for minimized size of graph to fit labels/title
const xPadding = 80;
const yPadding = 80;

// Define variables outside the scope of the callback function.
var crimeData;

const parseLineRelative = (line) => {
    return {
        District: parseInt(line["District"]),
        Type: line["Type"],
        Base: 1,
        Population: parseFloat(line["Population"]),
        Area: parseFloat(line["Area (Sq. Mile)"]),
        Pop18To24: parseFloat(line["% Pop 18 to 24"]),
        PopulationMale: parseFloat(line["% Male"]),
        LiquorLisc: parseFloat(line["Liquor Licenses/Sq. Mi."]),
        FaithOrgs: parseFloat(line["Faith Orgs/Sq. Mi."]),
		Parks: parseFloat(line["Parks/Sq. Mi."]),
		ResValue: parseFloat(line["Avg Residential Value"]),
        TotalOffenses: parseInt(line["Total Offenses"])
    }
}

const solveLeastSquaresCoefficients = (crimeMatrix) => {
	var nPredictorCols = crimeMatrix[0].length - 1;
	var iActualsCol = crimeMatrix[0].length;

	let A = math.eval('crimeMatrix[:, 1:' + nPredictorCols + ']', { crimeMatrix });
	let y = math.eval('crimeMatrix[:, ' + iActualsCol + ']', { crimeMatrix })

	let betas = math.eval(`inv(A' * A) * A' * y`, { A, y });
    return betas;
};

const calculatedModeledCrime = (crimeMatrix, betas) => {
	var nPredictorCols = crimeMatrix[0].length - 1;
    let A = math.eval('crimeMatrix[:, 1:' + nPredictorCols + ']', { crimeMatrix });
	let model = math.eval('A * betas', { A, betas });
    return model;
};

const calculatePopulationDensity = (district) => { return district.Population / district.Area };

const plotAxes = (xScale, yScale) => {
    //x-axis, District (sorted by actual crime)
    var bottomAxis = d3.axisBottom(xScale);
    svg.append("g")
        .attr("transform", "translate(0," + (height - xPadding) + ")")
        .attr("class", "xaxis")
        .call(bottomAxis);

    //y-axis, Total Crimes
    var leftAxis = d3.axisLeft(yScale);
    svg.append("g")
        .attr("class", "yaxis")
        .attr("transform", "translate(" + yPadding + ", 0)")
        .call(leftAxis);

    //x-axis label
    svg.append("text")
        .attr("transform", "translate(" + (width / 2.3) + "," + (height - (xPadding / 2)) + ")")
        .text("District");

    //y-axis label, rotated to be vertical text
    svg.append("text")
        .attr("transform", "translate(" + yPadding / 3 + "," + (height / 1.7) + ")rotate(270)")
        .text("Total Crime Occurred");

}

const plotActualCrimePerPopulationDensity = (data) => {
    let disctrictNumExtent = d3.extent(data, (district) => { return district.SortedOrder; });
    let disctrictNumScale = d3.scaleLinear()
        .domain(disctrictNumExtent)
        .range([xPadding, width - xPadding]);

    let actualCrimeExtent = d3.extent(data, (district) => { return district.ActualCrime; });
    let crimeScale = d3.scaleLinear()
        .domain(actualCrimeExtent)
        .range([height - yPadding, yPadding]);

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .html(function (d) { return "hello" })
        .direction('n')
        .offset([-3, 0])

    var vis = svg.append('g')
        .attr('transform', 'translate(20, 20)')
        .call(tip)

    var datapoints = vis.selectAll('circle')
        .data(data, (d) => { return d; })

    var modeled = datapoints.enter()
        .append('circle')
        .attr('r', 2.5)
        .attr('cx', (d) => disctrictNumScale(d.SortedOrder))
        .attr('cy', (d) => crimeScale(d.ModeledCrime))
        .style("fill", "FFA500")
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)

    var actuals = datapoints.enter()
        .append('circle')
        .attr("cx", (d) => disctrictNumScale(d.SortedOrder))
        .attr("cy", (d) => crimeScale(d.ActualCrime))
        .attr("r", 2.5)
        .style("fill", "45B3E7")
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)

    var errorBars = datapoints.enter()
        .append("line")
        .style("stroke", "gray") // Add a color
        .attr("x1", (d) => disctrictNumScale(d.SortedOrder))
        .attr("y1", (d) => crimeScale(d.ActualCrime))
        .attr("x2", (d) => disctrictNumScale(d.SortedOrder))
        .attr("y2", (d) => crimeScale(d.ModeledCrime));


    plotAxes(disctrictNumScale, crimeScale);
}

const addCoefficientsToTable = (data) => {
    rows = d3.select("table") // UPDATE
        .selectAll("tbody")
        .selectAll("tr")
        .data(data);

    rows.exit().remove(); // EXIT

    rows.enter() //ENTER + UPDATE
        .append('tr')
        .selectAll("td")
        .data(function (d) { return [d.Key, d.Value]; })
        .enter()
        .append("td")
        .text(function (d) { return d; });
}

function update(){
	svg.selectAll("*").remove();
	d3.csv("data/AggregateData/AggregateRelativePerArea.csv", parseLineRelative, function (error, data) {
		// console.log(data);
		let filteredData = data.filter(d =>
			parseInt(d.Population) > 0 && (d.Type == "CensusTract"));

		if(!d3.select("#populationCheckbox").property("checked")){ filteredData.forEach(function(v){ delete v.Population }); }
		if(!d3.select("#areaCheckbox").property("checked")){ filteredData.forEach(function(v){ delete v.areaSqMi }); }
		if(!d3.select("#age18to24Checkbox").property("checked")){ filteredData.forEach(function(v){ delete v.Pop18To24 }); }
		if(!d3.select("#maleCheckbox").property("checked")){ filteredData.forEach(function(v){ delete v.PopulationMale }); }
		if(!d3.select("#liquorCheckbox").property("checked")){ filteredData.forEach(function(v){ delete v.LiquorLisc }); }
		if(!d3.select("#faithOrgsCheckbox").property("checked")){ filteredData.forEach(function(v){ delete v.FaithOrgs }); }
		if(!d3.select("#parksCheckbox").property("checked")){ filteredData.forEach(function(v){ delete v.Parks }); }
		if(!d3.select("#resValueCheckbox").property("checked")){ filteredData.forEach(function(v){ delete v.ResValue }); }

		//console.log("filtered data after processing")
		//console.log(filteredData);

		var nCols = filteredData[0].length
		let crimeMatrix = filteredData.map(d => { return Object.values(d).slice(2, nCols) });
		let betas = solveLeastSquaresCoefficients(crimeMatrix);
		let keys = Object.getOwnPropertyNames(filteredData[0]);
		keys.shift(); // get rid of district number
		keys.shift(); // get rid of district type
		keys.pop(); // get rid of actuals

		console.log(keys);
		// console.log(betas);
		let modeledCrime = calculatedModeledCrime(crimeMatrix, betas).map(d => { return parseFloat(d) });
		// console.log(modeledCrime);

		let toPlot = crimeMatrix.map((district, i) => {
			// TODO: THIS IS A PROBLEM IF POPULATION OR AREA ARE DESELECTED FROM THE CHECKBOXES
			let population = district[1];
			let areaSqMi = district[2];
			var nCols = district.length - 1 ;
			let actual = district[nCols];
			let predicted = modeledCrime[i];
			// console.log(modeledCrime);
			let error = 100 * ((predicted - actual) / actual);
			return {
				Population: population,
				Area: areaSqMi,
				ActualCrime: actual,
				ModeledCrime: modeledCrime[i],
				Error: error
			}
		});


		let sortedData = toPlot.sort((d1, d2) => {
			return d1.ActualCrime > d2.ActualCrime ? 1 //concat to end
				: d1.ActualCrime < d2.ActualCrime ? -1 //prepend to start
					: 0; //equal
		});
		let sortedDataWithIndex = toPlot.map((district, i) => {
			district.SortedOrder = i; //add number for order
			return district;
		})

		//console.log(sortedDataWithIndex);

		let averageError = 0;
		toPlot.forEach((district) => {
			averageError += district.Error;
		});
		averageError /= toPlot.length;

		console.log(averageError);

    	plotActualCrimePerPopulationDensity(sortedDataWithIndex);
		let tableData = keys.map((key, index) => { return { Key: key, Value: betas[index] }; });
		addCoefficientsToTable(tableData);
	})
}

update();
d3.select("#populationCheckbox").on("change", update);
d3.select("#areaCheckbox").on("change", update);
d3.select("#age18to25Checkbox").on("change", update);
d3.select("#maleCheckbox").on("change", update);
d3.select("#liquorCheckbox").on("change", update);
d3.select("#faithOrgsCheckbox").on("change", update);
d3.select("#parksCheckbox").on("change", update);
d3.select("#resValueCheckbox").on("change", update);
