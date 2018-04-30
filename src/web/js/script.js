var math = require("mathjs");

var svg = d3.select("#crimeApprox");
const width = svg.attr("width");
const height = svg.attr("height");

//paddings for minimized size of graph to fit labels/title
const xPadding = 80;
const yPadding = 80;

// Define variables outside the scope of the callback function.
var crimeData;

const parseLine = (line) => {
    return {
        District: line["District"],
        Type: line["Type"],
        Base: '1',
        Population: line["Population"],
        Area: line["Area sqmi"],
        PopUnder5: line["Under 5"],
        Pop5To17: line["5 to 17"],
        Pop18To24: line["18 to 24"],
        Pop25To44: line["25 to 44"],
        Pop45To64: line["45 to 64"],
        PopOver65: line["Over 65"],
        PopulationMale: line["Male"],
        PopulationFemale: line["Female"],
        TotalFamilies: line["Total Families"],
        AvgResValue: line["Avg Residential Value"],
        LiquorLisc: line["Liquor Licenses"],
        FaithOrgs: line["Faith Orgs"],
        Parks: line["Parks"],
        TotalOffenses: line["Total A Offenses"],
        Assaults: line["Assault Offenses"],
        Arson: line["Arson"],
        Burglary: line["Burglary"],
        CriminalDamage: line["Criminal Damages"],
        LockedVehicle: line["Locked Vehicle"],
        Robbery: line["Robbery"],
        SexOffense: line["Sex Offense"],
        Theft: line["Theft"],
        VehicleTheft: line["Vehicle Theft"],
        Homicide: line["Homicide"]
    }
}

const solveLeastSquaresCoefficients = (crimeMatrix) => {
    let A = math.eval('crimeMatrix[:, 3:18]', { crimeMatrix });
    console.log("A");
    console.log(A);
    let y = math.eval('crimeMatrix[:, 19]', { crimeMatrix })
    let betas = math.eval(`inv(A' * A) * A' * y`, { A, y });
    return betas;
}

const calculatedModeledCrime = (crimeMatrix, betas) => {
    let A = math.eval('crimeMatrix[:, 3:18]', { crimeMatrix });
    let model = math.eval('A * betas', { A, betas });
    return model;
}


d3.csv("data/AggregateData/CensusPoliceAldermanicData.csv", parseLine, function(error, data) {
    let filteredData = data.filter(d =>  parseInt(d.Population) > 0 );
    let crimeMatrix = filteredData.map(d => { return Object.values(d) });
    console.log(crimeMatrix);
    let betas = solveLeastSquaresCoefficients(crimeMatrix);
    console.log(betas);
    let modeledCrime = calculatedModeledCrime(crimeMatrix, betas);
    console.log(modeledCrime);
})


