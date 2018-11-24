const eulerian_circuit = require("../eulerian_circuit");
const is_eulerian_circuit = require("../is_eulerian_circuit");
const { Edge, Graph } = require("../Graph.js");

test("path returned is an Eulerian circuit", () => {
  getTestCases().forEach(graph => {
    const circuit = eulerian_circuit(graph);
    const isEulerian = is_eulerian_circuit(graph, circuit);
    if (!isEulerian) {
      console.log("Path is not Eulerian", circuit.toString());
    }
    expect(is_eulerian_circuit(graph, circuit)).toBeTruthy();
  });
});

function getTestCases() {
  return [
    new Graph({ vertexCount: 3 })
      .addEdge(new Edge(0, 1))
      .addEdge(new Edge(1, 2))
      .addEdge(new Edge(2, 0)),

    new Graph({ vertexCount: 7 })
      .addEdge(new Edge(0, 1))
      .addEdge(new Edge(1, 2))
      .addEdge(new Edge(2, 0))
      .addEdge(new Edge(2, 3))
      .addEdge(new Edge(3, 4))
      .addEdge(new Edge(4, 5))
      .addEdge(new Edge(5, 6))
      .addEdge(new Edge(6, 4))
      .addEdge(new Edge(4, 2)),

    new Graph({ vertexCount: 7 })
      .addEdge(new Edge(0, 1))
      .addEdge(new Edge(1, 2))
      .addEdge(new Edge(2, 3))
      .addEdge(new Edge(3, 0))
      .addEdge(new Edge(1, 4))
      .addEdge(new Edge(4, 1))
      .addEdge(new Edge(3, 5))
      .addEdge(new Edge(5, 3))
      .addEdge(new Edge(0, 6))
      .addEdge(new Edge(6, 0))
  ];
}
