// @flow

function nullthrows<T>(value: ?T, message: string): T {
  if (value == null) {
    throw new Error(message);
  }
  return value;
}

class Edge<T> {
  _vertex1: T;
  _vertex2: T;
  _isVisited: boolean;

  constructor(vertex1: T, vertex2: T) {
    this._vertex1 = vertex1;
    this._vertex2 = vertex2;
    this._isVisited = false;
  }

  getVertex1(): T {
    return this._vertex1;
  }

  getVertex2(): T {
    return this._vertex2;
  }

  getTheOtherVertex(vertex: T): T {
    if (vertex === this._vertex1) {
      return this._vertex2;
    }
    if (vertex === this._vertex2) {
      return this._vertex1;
    }
    throw new Error("vertex must be one of the endpoints of the edge");
  }

  markAsVisited(): this {
    this._isVisited = true;
    return this;
  }

  isVisited(): boolean {
    return this._isVisited;
  }
}

class List<T> {
  _list: Array<T>;
  _index: number;

  constructor(list: ?Array<T>) {
    this._list = list || [];
    this._index = 0;
  }

  add(element: T): this {
    this._list.push(element);
    return this;
  }

  current(): ?T {
    if (this._index >= this._list.length) {
      return null;
    }

    return this._list[this._index] || null;
  }

  next(): ?T {
    if (this._index >= this._list.length) {
      return null;
    }
    this._index += 1;
    return this._list[this._index];
  }
}

class Graph {
  _adjacencyList: { [number]: List<Edge<number>> };
  // We need an explicit count for the degrees because edges from adjacency
  // list can be deleted lazily.
  _vertexDegrees: { [number]: number };
  // Number of vertices in the graph
  _vertexCount: number;

  constructor({ vertexCount }: { vertexCount: number }) {
    this._adjacencyList = {};
    this._vertexCount = vertexCount;

    // Initialize degrees
    this._vertexDegrees = {};
    for (let i = 0; i < vertexCount; i++) {
      this._vertexDegrees[i] = 0;
    }
  }

  addEdge(edge: Edge<number>): this {
    const vertex1 = edge.getVertex1();
    const vertex2 = edge.getVertex2();

    const adjacencyList = this._adjacencyList;
    if (!(vertex1 in adjacencyList)) {
      adjacencyList[vertex1] = new List();
    }
    if (!(vertex2 in adjacencyList)) {
      adjacencyList[vertex2] = new List();
    }

    adjacencyList[vertex1].add(edge);
    adjacencyList[vertex2].add(edge);

    // Update degrees
    this._vertexDegrees[vertex1] += 1;
    this._vertexDegrees[vertex2] += 1;

    this._adjacencyList = adjacencyList;
    return this;
  }

  /**
   * Returns the next edge for a given vertex or null if it visited the last
   * edge.
   */
  getNextUnvisitedEdgeForVertex(vertex: number): ?Edge<number> {
    if (!(vertex in this._adjacencyList)) {
      throw new Error("Vertex is not in adjacency list");
    }
    const neighbors = this._adjacencyList[vertex];
    while (true) {
      const edge = neighbors.current();
      // End of the list
      if (edge == null) {
        return null;
      }
      neighbors.next();

      // Found a valid edge
      if (!edge.isVisited()) {
        return edge;
      }
    }
  }

  deleteEdge(edge: Edge<number>): this {
    edge.markAsVisited();
    this._vertexDegrees[edge.getVertex1()] -= 1;
    this._vertexDegrees[edge.getVertex2()] -= 1;
    return this;
  }

  getDegree(vertex: number): number {
    return this._vertexDegrees[vertex];
  }
}

/**
 * Node of a path (linked list node).
 */
class Node<T> {
  _element: T;
  _nextNode: ?Node<T>;

  constructor(element: T) {
    this._element = element;
    this._nextNode = null;
  }

  linkTo(node: ?Node<T>): this {
    this._nextNode = node;
    return this;
  }

  getElement(): T {
    return this._element;
  }

  getNextNode(): ?Node<T> {
    return this._nextNode;
  }
}

class Path {
  _startNode: ?Node<number>;
  _endNode: ?Node<number>;

  // For a given vertex v, store a link to the last node containing an edge
  // (*, v)
  _lastOccurrenceOfVertex: { [number]: ?Node<number> };

  constructor() {
    this._startNode = null;
    this._endNode = null;
    this._lastOccurrenceOfVertex = {};
  }

  append(vertex: number) {
    const node = new Node(vertex);

    if (this._startNode == null) {
      this._startNode = node;
    } else {
      const endNode = nullthrows(this._endNode, "");
      endNode.linkTo(node);
    }
    this._endNode = node;
    this._lastOccurrenceOfVertex[vertex] = node;
    return this;
  }

  getEndNode(): ?Node<number> {
    return this._endNode;
  }

  getStartNode(): ?Node<number> {
    return this._startNode;
  }

  toString(): string {
    if (this._startNode == null) {
      return "[]";
    }
    const initialNode = this._startNode;
    let currentNode = initialNode;
    let result = "[";
    let isFirst = true;
    while (currentNode != null && currentNode.getNextNode() !== initialNode) {
      if (isFirst) {
        isFirst = false;
      } else {
        result += ", ";
      }

      result += currentNode.getElement();
      currentNode = currentNode.getNextNode();
    }
    result += "]";
    return result;
  }

  removeFirst(): this {
    const startNode = this._startNode;
    if (startNode == null) {
      return this;
    }

    this._startNode = startNode.getNextNode();
    // Path became empty
    if (this._startNode == null) {
      this._endNode = null;
    }
    return this;
  }

  insertAtVertex(vertex: number, path: Path): this {
    const node = this._lastOccurrenceOfVertex[vertex];
    if (node == null) {
      throw new Error("Could not find vertex in the path");
    }

    const firstPathNode = path.getStartNode();
    if (firstPathNode == null) {
      throw new Error("Path to insert has to have at least 2 nodes");
    }

    // Skip the first node of the path since it's a duplicated vertex
    const secondPathNode = firstPathNode.getNextNode();
    if (secondPathNode == null) {
      throw new Error("Path to insert has to have at least 2 nodes");
    }

    const lastPathNode = path.getEndNode();
    if (lastPathNode == null) {
      throw new Error("Path to insert has to have at least 2 nodes");
    }

    const oldNextNode = node.getNextNode();
    node.linkTo(secondPathNode);
    lastPathNode.linkTo(oldNextNode);
    return this;
  }
}

/**
 * Given a graph, returns any circuit from it, visiting the edges.
 */
function find_circuit(graph: Graph, initialVertex: number) {
  let vertex = initialVertex;
  const path = new Path();
  path.append(vertex);

  const followUpVertices = new Set();
  while (true) {
    // Get the next vertex
    const edge = graph.getNextUnvisitedEdgeForVertex(vertex);

    // TODO: handle null edge
    if (edge == null) {
      throw new Error("This graph is not Eulerian");
    }
    const nextVertex = edge.getTheOtherVertex(vertex);

    graph.deleteEdge(edge);
    vertex = nextVertex;

    // This means there is another cycle passing through
    if (graph.getDegree(vertex) > 1) {
      // Store a reference to the path
      followUpVertices.add(vertex);
    } else {
      // We need to remove the vertex from consideration because its edges
      // were consumed.
      followUpVertices.delete(vertex);
    }

    path.append(vertex);

    // Circuit closed
    if (nextVertex === initialVertex) {
      break;
    }
  }

  for (vertex of followUpVertices) {
    let subPath = find_circuit(graph, vertex);
    // Merge sub-path into path
    path.insertAtVertex(vertex, subPath);
  }

  return path;
}

function solve(graph: Graph): Path {
  return find_circuit(graph, 0);
}

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

function test() {
  getTestCases().forEach((graph, index) => {
    console.log("running test", index + 1);
    const solution = solve(graph);
    console.log(solution.toString());
  });
}

test();

/**
 * TODO
 *
 * - Add a validation function
 * - Add more test cases
 * - Break into modules
 */
