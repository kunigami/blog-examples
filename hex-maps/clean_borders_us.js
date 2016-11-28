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

fs.readFile('./borders.csv', 'utf8', (err, data) => {
  const borders = d3.csvParse(data);

  const borderSet = {};
  borders.forEach(function(border) {
    const tokens = border.st1st2.split('-');
    let st1 = tokens[0].trim();
    let st2 = tokens[1].trim();
    // Order the states consistently to avoid duplicates
    if (st1 > st2) {
      var tmp = st1;
      st1 = st2;
      st2 = st1;
    }
    borderSet[st1 + '-' + st2] = {'state1': st1, 'state2': st2};
  });

  const bordersCleanedSerialized = d3.csvFormat(Object.values(borderSet));

  fs.writeFile(
    "./borders_cleaned.csv",
    bordersCleanedSerialized,
    function(err) {
      if(err) {
          return console.log(err);
      }
      console.log("The file was saved!");
    }
  );
});
