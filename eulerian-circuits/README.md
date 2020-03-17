# Eulerian Circuit

Implementation of the Hierholzer algorithm in JavaScript (ES6 syntax, Flow typing), 
which finds an Eulerian circuit in a graph if one exists. It runs in linear time 
on the number of edges.

To transpile the code and run the tests

    npm install
    make run
  

## More Dependencies

* yarn: https://classic.yarnpkg.com/en/docs/install/#debian-stable

* flow (see latest instructions in https://flow.org/en/docs/install/)
  * yarn add --dev @babel/core @babel/cli @babel/preset-flow
  * yarn run babel src/ -- -d lib/
  * yarn add --dev flow-bin
  