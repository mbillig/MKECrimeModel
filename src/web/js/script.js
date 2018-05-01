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
        Population: parseInt(line["Population"]),
        Area: parseFloat(line["Area sqmi"]),
        Pop18To24: parseFloat(line["18 to 24"]),
        PopulationMale: parseFloat(line["Male"]),
        LiquorLisc: parseFloat(line["Liquor Licenses"]),
        FaithOrgs: parseFloat(line["Faith Orgs"]),
        Parks: parseFloat(line["Parks"]),
        TotalOffenses: parseInt(line["Total A Offenses"])
    }
}

const solveLeastSquaresCoefficients = (crimeMatrix) => {
    let A = math.eval('crimeMatrix[:, 1:8]', { crimeMatrix });
    //console.log("A");
    //console.log(A);
    let y = math.eval('crimeMatrix[:, 9]', { crimeMatrix })
    //console.log("y");
    //console.log(y);
    let betas = math.eval(`inv(A' * A) * A' * y`, { A, y });
    return betas;
};

const calculatedModeledCrime = (crimeMatrix, betas) => {
    let A = math.eval('crimeMatrix[:, 1:8]', { crimeMatrix });
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

const plotActualCrimePerPopulationDensity = (svg, data) => {
    let disctrictNumExtent = d3.extent(data, (district) => { return district.SortedOrder; });
    let disctrictNumScale = d3.scaleLinear()
        .domain(disctrictNumExtent)
        .range([xPadding, width - xPadding]);

    console.log(disctrictNumExtent);

    let actualCrimeExtent = d3.extent(data, (district) => { return district.ActualCrime; });
    let crimeScale = d3.scaleLinear()
        .domain(actualCrimeExtent)
        .range([height - yPadding, yPadding]);

    data.map((district) => {
        svg.append("circle")
            .attr("cx", disctrictNumScale(district.SortedOrder))
            .attr("cy", crimeScale(district.ActualCrime))
            .attr("r", 2)
            .style("fill", "45B3E7");

        svg.append("circle")
            .attr("cx", disctrictNumScale(district.SortedOrder))
            .attr("cy", crimeScale(district.ModeledCrime))
            .attr("r", 2)
            .style("fill", "FFA500");

        svg.append("line")
            .style("stroke", "gray") // Add a color
            .attr("x1", disctrictNumScale(district.SortedOrder))
            .attr("y1", crimeScale(district.ActualCrime))
            .attr("x2", disctrictNumScale(district.SortedOrder))
            .attr("y2", crimeScale(district.ModeledCrime));
    })

    plotAxes(disctrictNumScale, crimeScale);
}

d3.csv("data/AggregateData/AggregateRelative.csv", parseLineRelative, function (error, data) {
    console.log(data);
    let filteredData = data.filter(d =>
        parseInt(d.Population) > 0 && (d.Type == "CensusTract"));
    // console.log(filteredData);
    let crimeMatrix = filteredData.map(d => { return Object.values(d).slice(2, 11) });
    // console.log(crimeMatrix);
    let betas = solveLeastSquaresCoefficients(crimeMatrix);
    // console.log(betas);
    let modeledCrime = calculatedModeledCrime(crimeMatrix, betas).map(d => { return parseFloat(d) });
    // console.log(modeledCrime);

    let toPlot = crimeMatrix.map((district, i) => {
        let population = district[1];
        let areaSqMi = district[2];
        let actual = district[8];
        let predicted = modeledCrime[i];
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
        return d1.ActualCrime > d2.ActualCrime ? 1
            : d1.ActualCrime < d2.ActualCrime ? -1
                : 0;
    });
    let sortedDataWithIndex = toPlot.map((district, i) => {
        district.SortedOrder = i;
        return district;
    })

    console.log(sortedDataWithIndex);

    let averageError = 0;
    toPlot.forEach((district) => {
        averageError += district.Error;
    });
    averageError /= toPlot.length;

    console.log(averageError);

    plotActualCrimePerPopulationDensity(svg, sortedDataWithIndex);
})




