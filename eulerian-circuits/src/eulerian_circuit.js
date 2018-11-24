// @flow

const { Edge, Graph, Path, Node } = require("./Graph.js");

/**
 * Given a graph, returns any circuit from it, remove the edges from it.
 */
function find_circuit(graph: Graph, initialVertex: number) {
  let vertex = initialVertex;
  const path = new Path();
  path.append(vertex);

  while (true) {
    // Get the next vertex
    const edge = graph.getNextEdgeForVertex(vertex);

    if (edge == null) {
      throw new Error("This graph is not Eulerian");
    }
    const nextVertex = edge.getTheOtherVertex(vertex);

    graph.deleteEdge(edge);
    vertex = nextVertex;

    path.append(vertex);

    // Circuit closed
    if (nextVertex === initialVertex) {
      break;
    }
  }

  // Search for sub-circuits
  for (vertex of path.getContentAsArray()) {
    // Since the vertex was added, its edges could have been removed
    if (graph.getDegree(vertex) === 0) {
      continue;
    }
    let subPath = find_circuit(graph, vertex);
    // Merge sub-path into path
    path.insertAtVertex(vertex, subPath);
  }

  return path;
}

function eulerian_circuit(initialGraph: Graph): Path {
  // Clone because we'll mutate it
  const graph = initialGraph.clone();
  return find_circuit(graph, 0);
}

// test();

module.exports = eulerian_circuit;
