// @flow

const { Edge, Graph, Path, Node } = require("./Graph.js");

function increment_cell_in_matrix(matrix, dimension1, dimension2) {
  if (matrix[dimension1] == null) {
    matrix[dimension1] = {};
  }

  if (matrix[dimension1][dimension2] == null) {
    matrix[dimension1][dimension2] = 0;
  }

  matrix[dimension1][dimension2] += 1;
  return matrix;
}

function is_eulerian_circuit(graph: Graph, circuit: Path): boolean {
  const edges = graph.getEdges();
  // Construct a frequency matrix from the edges endpoints (note that we have
  // two edges for two given endpoints, so we're double counting)
  const frequencyMap = {};
  edges.forEach(edge => {
    const vertex1 = edge.getVertex1();
    const vertex2 = edge.getVertex2();
    increment_cell_in_matrix(frequencyMap, vertex1, vertex2);
    increment_cell_in_matrix(frequencyMap, vertex2, vertex1);
  });

  const vertices = circuit.getContentAsArray();
  for (let index = 1; index < vertices.length; index++) {
    const vertex1 = vertices[index - 1];
    const vertex2 = vertices[index];
    if (
      frequencyMap[vertex1] == null ||
      frequencyMap[vertex1][vertex2] == null
    ) {
      throw new Error(
        "There is an edge in the path that does not belong to the graph"
      );
    }
    frequencyMap[vertex1][vertex2] -= 1;
    frequencyMap[vertex2][vertex1] -= 1;
  }

  let uncoveredEdges = 0;
  // Verify that all edges were covered
  Object.values(frequencyMap).forEach(frequencyMapForVertex =>
    Object.values(frequencyMapForVertex).forEach(
      edgeCount => (uncoveredEdges += edgeCount)
    )
  );

  return uncoveredEdges === 0;
}

module.exports = is_eulerian_circuit;
