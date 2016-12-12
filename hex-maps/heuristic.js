/**
 * Script to generate a valid hexmap from a list of pairs denoting the
 * borders between 2 countries.
 *
 * How to run this:
 * node --use_strict heuristic.js
 */

const d3 = require('d3');
const fs = require('fs');

// TODO: move to a separate module. Use one from npm
class Queue {
  constructor(initialValues) {
    this._front = [];
    this._back = initialValues || [];
  }

  push(elem) {
    this._back.push(elem);
  }

  pop() {
    if (this.empty()) {
      throw Error('cannot remove from empty queue.');
    }
    if (this._front.length == 0) {
      this._front = this._back;
      this._back = [];
      this._front.reverse();
    }
    return this._front.pop();
  }

  empty() {
    return this._front.length == 0 && this._back.length == 0;
  }
}

const bordersDataCSV =
  fs.readFileSync('./countries_border_processed.csv', 'utf8');
const countryCenterCSV =
  fs.readFileSync('./countries_centers_processed.csv', 'utf8');

const borders = d3.csvParse(bordersDataCSV);
const countryCenters = d3.csvParse(countryCenterCSV);

// Construct a list of countries info and order by increasing y
const countriesInfoLookup = {};
countryCenters.forEach(countryCenters => {
  countriesInfoLookup[countryCenters.country] = {
    code: countryCenters.country,
    center: {x: countryCenters.x, y: countryCenters.y},
    // Initialize some metadata used for traversal
    visited: false,
    neighbors: [],
    hexCoordinates: {x: null, y: null},
  };
});

// Build the adjacency matrix
borders.forEach(borderInfo => {
  const country1 = borderInfo.country1;
  const country2 = borderInfo.country2;
  if (
    !(country1 in countriesInfoLookup) ||
    !(country2 in countriesInfoLookup)
  ) {
    // TODO: clean up the data
    return;
  }
  countriesInfoLookup[country1].neighbors.push(country2);
  countriesInfoLookup[country2].neighbors.push(country1);
})

// A map of maps. Indexed first by x then by y.
let occupationMap = {
  __map: new Map(),

  isOccupied(coord) {
    return this.__map[coord.x] && this.__map[coord.x][coord.y];
  },

  occupy(coord) {
    if (!(coord.x in this.__map)) {
      this.__map[coord.x] = {};
    }
    this.__map[coord.x][coord.y] = true;
    return this;
  },
};

const countriesInfo = Object.keys(countriesInfoLookup).map(
  countryCode => countriesInfoLookup[countryCode]
);
countriesInfo.sort((countryInfoA, countryInfoB) => {
  return parseFloat(countryInfoA.center.y) - parseFloat(countryInfoB.center.y);
});

let maxCurrentX = 0;
countriesInfo.forEach(countryInfo => {
  const countryCode = countryInfo.code;
  if (countryInfo.visited) {
    return;
  }

  countryInfo.visited = true;

  const queue = new Queue([countryCode]);

  let currentCoordinates = {x: maxCurrentX + 2, y: 0};
  // A map of maps. Indexed first by x then by y.
  occupationMap.occupy(currentCoordinates);
  // First country to be enqued starts at {x, y}.
  countryInfo.visited = true;
  countryInfo.hexCoordinates = currentCoordinates;

  while (!queue.empty()) {
    let currCountryCode = queue.pop();
    let currCountryInfo = countriesInfoLookup[currCountryCode];
    maxCurrentX = Math.max(maxCurrentX, currCountryInfo.hexCoordinates.x);

    const neighbors = currCountryInfo.neighbors;
    neighbors.forEach(neighborCountryCode => {
      let neighborCountryInfo = countriesInfoLookup[neighborCountryCode];
      if (neighborCountryInfo.visited) {
        return;
      }
      neighborCountryInfo.visited = true;
      let step1;
      let step2;
      // South-east neighbor
      if (neighborCountryInfo.center.x > currCountryInfo.center.x) {
        step1 = {x: 0, y: 1};
        step2 = {x: 1, y: 0};
      } else { // South-west neighbor
        step1 = {x: -1, y: 1};
        step2 = {x: -1, y: 0};
      }

      let startCoord = currCountryInfo.hexCoordinates;
      let tentativeCoord;
      while (true) {
        if (!occupationMap.isOccupied(startCoord)) {
          tentativeCoord = {
            x: startCoord.x + step1.x,
            y: startCoord.y + step1.y
          };
          if (!occupationMap.isOccupied(tentativeCoord)) {
            break;
          }
          // Second option
          tentativeCoord = {
            x: startCoord.x + step2.x,
            y: startCoord.y + step2.y
          };
          if (!occupationMap.isOccupied(tentativeCoord)) {
            break;
          }
        }
        // Try a new starting point
        startCoord = {
          x: startCoord.x + step1.x,
          y: startCoord.y + step1.y
        };
      }
      neighborCountryInfo.hexCoordinates = Object.assign({}, tentativeCoord);

      queue.push(neighborCountryCode);
    });
  }
});

// Save in the format expected by the rendering JavaScript
const outputJSON = [];
countriesInfo.forEach(countryInfo => {
  outputJSON.push({
    code: countryInfo.code,
    // TODO: Add the full country name to countries_centers_processed.csv
    fullname:  countryInfo.code,
    x: countryInfo.hexCoordinates.x,
    y: countryInfo.hexCoordinates.y,
  });
});

const hexCoordinatesSerialized = d3.csvFormat(outputJSON);
fs.writeFile(
  "./countries_hexmap_data.csv",
  hexCoordinatesSerialized,
  function(err) {
    if(err) {
        return console.log(err);
    }
    console.log("countries_hexmap_data was saved!");
  }
);
