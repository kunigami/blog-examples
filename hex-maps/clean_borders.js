/**
 * Script to clean up the state border data from the CSV downloaded from
 * http://users.econ.umn.edu/~holmes/data/BorderData.html
 *
 * How to run this:
 * node --use_strict clean_borders.js
 */
// Polyfills functions like Object.assign() and Object.values()
require("babel-polyfill");

const d3 = require('d3');
const fs = require('fs');

// https://en.wikipedia.org/wiki/List_of_political_and_geographic_borders
// http://wikitables.geeksta.net/
const bordersData = fs.readFileSync('./raw_countries_borders.csv', 'utf8');
// http://dev.maxmind.com/geoip/legacy/codes/country_latlon/
const countriesCentersData = fs.readFileSync('./countries_center.csv', 'utf8');
// https://github.com/datasets/country-codes/blob/master/data/country-codes.csv
const countriesCodesData = fs.readFileSync('./countries_codes.csv', 'utf8');

const borders = d3.csvParse(bordersData);
const countriesCenters = d3.csvParse(countriesCentersData);
const countriesCodes = d3.csvParse(countriesCodesData);

const countryNameToCountryCode = {};
countriesCodes.forEach(function(countryData) {
  const name = countryData.name;
  const code = countryData['ISO3166-1-Alpha-2'];
  if (code == '') {
    return;
  }
  countryNameToCountryCode[name.toLowerCase()] = code;
});

const countryCenterByCountryCode = {};
const projection = d3
  .geoMercator();

/*
 * Convert the lon-lat coordinate representing the center of the country to
 * 2D using the mercator projection.
 */
const countryCentersProcessed = countriesCenters.map(countryCenter => {
  const code = countryCenter['iso 3166 country'];
  const lat = parseFloat(countryCenter['latitude']);
  const lon = parseFloat(countryCenter['longitude']);
  const projected = projection([lon, lat]);
  const x = projected[0];
  const y = projected[1];
  const row = [code, x.toFixed(1), y.toFixed(1)];
  return row;
});

const invalidCountries = new Set([
  '',
  '(alphabetical order)',
  'Akrotiri',
  'Ceuta',
  'Dhekelia',
  'Melilla',
  'Peñón de Vélez de la Gomera',
]);

const aliases = {
  'Antigua and Barbuda': 'Antigua & Barbuda',
  'Bosnia and Herzegovina': 'Bosnia',
  'Bosnia Herzegovina': 'Bosnia',
  'Brunei Darussalam': 'Brunei',
  'Congo, Democratic Republic of the': 'Congo - Kinshasa',
  'Czech Republic': 'Czechia',
  'Democratic People\'s Republic of Korea': 'North Korea',
  'East Timor': 'Timor-Leste',
  'Federated States of Micronesia': 'Micronesia',
  'Guinea Bissau': 'Guinea-Bissau',
  'Ivory Coast': 'Côte d’Ivoire',
  'Korea, South': 'South Korea',
  'Myanmar (Burma)': 'Myanmar',
  // 'Laos': 'Lao People\'s Democratic Republic',
  // 'Russia': 'Russian Federation',
  'Republic of Korea': 'South Korea',
  'Republic of the Congo': 'Congo - Kinshasa',
  'São Tomé and Príncipe': 'São Tomé & Príncipe',
  'Saint Kitts and Nevis': 'St. Kitts & Nevis',
  'Saint Lucia': 'St. Lucia',
  'Saint Vincent and the Grenadines': 'St. Vincent & Grenadines',
  // 'Tanzania': 'Tanzania, United Republic of',
  'United States': 'US',
  'United Kingdom': 'UK',
  // 'Vatican City': 'Holy See',
  // 'Venezuela': 'Venezuela (Bolivarian Republic of)',
  // 'Vietnam': 'Viet Nam',
  'The Gambia': 'Gambia',
  'Trinidad and Tobago': 'Trinidad & Tobago',
};

function getCountryCode(countryName) {
  if (countryName.startsWith('*')) {
    return null;
  }
  if (invalidCountries.has(countryName)) {
    return null;
  }
  const aliasedCountryName =
    (aliases[countryName] || countryName).toLowerCase();
  if (!(aliasedCountryName in countryNameToCountryCode)) {
    console.log(countryName + ' not found.');
    return null;
  }
  return countryNameToCountryCode[aliasedCountryName];
}

const borderPairs = [];
borders.forEach(function(border) {
  // Normalize the borders to use country codes (ISO 2)
  const sourceName = border['Name of country'];
  const destinationsNames = border['Borders'].split('/').map(entry => entry.trim());

  const source = getCountryCode(sourceName);
  if (source == null) {
    return;
  }

  const destinations = destinationsNames
    .map(destination => getCountryCode(destination))
    .filter(destination => destination != null);

  destinations.forEach(destination => {
    if (source > destination) {
      return;
    }
    borderPairs.push([source, destination]);
  });
});

(function saveCountriesBorder() {
  const rows = [['country1', 'country2']].concat(Object.values(borderPairs));
  const borderPairsSerialized = d3.csvFormatRows(rows);

  fs.writeFile(
    "./countries_border_processed.csv",
    borderPairsSerialized,
    function(err) {
      if(err) {
          return console.log(err);
      }
      console.log("countries_border_processed was saved!");
    }
  );
})();

(function saveCountriesCenters() {
  const countryCentersProcessedWithHeader = [['country', 'x', 'y']]
    .concat(countryCentersProcessed);
  const countryCentersSerialized = d3
    .csvFormatRows(countryCentersProcessedWithHeader);

  fs.writeFile(
    "./countries_centers_processed.csv",
    countryCentersSerialized,
    function(err) {
      if(err) {
          return console.log(err);
      }
      console.log("countries_centers_processed was saved!");
    }
  );
})();
