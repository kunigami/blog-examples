// @flow

const nullthrows = require("./nullthrows");
const StatefulArray = require("./StatefulArray");

class Edge<T> {
  _vertex1: T;
  _vertex2: T;
  // Allows deleting an edge lazily by setting an internal state. It's up to the
  // caller to make sure to not include deleted edges.
  _isDeleted: boolean;

  constructor(vertex1: T, vertex2: T) {
    this._vertex1 = vertex1;
    this._vertex2 = vertex2;
    this._isDeleted = false;
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

  markAsDeleted(): this {
    this._isDeleted = true;
    return this;
  }

  isDeleted(): boolean {
    return this._isDeleted;
  }

  clone(): Edge<T> {
    const clonedEdge = new Edge(this._vertex1, this._vertex2);
    if (this.isDeleted()) {
      clonedEdge.markAsDeleted();
    }
    return clonedEdge;
  }
}

class Graph {
  _adjacencyList: { [number]: StatefulArray<Edge<number>> };
  // We need an explicit count for the degrees because edges from adjacency
  // list can be deleted lazily.
  _vertexDegrees: { [number]: number };
  // Number of vertices in the graph
  _vertexCount: number;
  // We store the list of edges explicitly because in the adjacency list they
  // are duplicated. It gets tricky to differenciate duplicated instances for
  // self-edges, so we pay the cost in complexity to make sure this and
  // _adjacencyList are in sync.
  _edges: Array<Edge<number>>;

  constructor({ vertexCount }: { vertexCount: number }) {
    this._adjacencyList = {};
    this._vertexCount = vertexCount;
    this._edges = [];

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
      adjacencyList[vertex1] = new StatefulArray();
    }
    if (!(vertex2 in adjacencyList)) {
      adjacencyList[vertex2] = new StatefulArray();
    }

    adjacencyList[vertex1].push(edge);
    adjacencyList[vertex2].push(edge);

    // Update degrees
    this._vertexDegrees[vertex1] += 1;
    this._vertexDegrees[vertex2] += 1;

    this._adjacencyList = adjacencyList;

    this._edges.push(edge);

    return this;
  }

  /**
   * Returns a list of the edges in the graph in arbitrary order
   */
  getEdges(): Array<Edge<number>> {
    let edges = [];
    // Filter deleted edges
    return this._edges.filter(edge => !edge.isDeleted());
  }

  /**
   * Returns the next edge for a given vertex or null if it visited the last
   * edge.
   */
  getNextEdgeForVertex(vertex: number): ?Edge<number> {
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
      if (!edge.isDeleted()) {
        return edge;
      }
    }
  }

  deleteEdge(edge: Edge<number>): this {
    edge.markAsDeleted();
    this._vertexDegrees[edge.getVertex1()] -= 1;
    this._vertexDegrees[edge.getVertex2()] -= 1;
    return this;
  }

  getDegree(vertex: number): number {
    return this._vertexDegrees[vertex];
  }

  clone(): Graph {
    const graph = new Graph({ vertexCount: this._vertexCount });
    const edges = this.getEdges();
    edges.forEach(edge => graph.addEdge(edge.clone()));
    return graph;
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

  next(): ?Node<T> {
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

  /**
   * Returns the content of the path as array
   */
  getContentAsArray(): Array<number> {
    let node = this._startNode;
    const result = [];
    // Note: if path is empty this._startNode = this._endNode so we return empty
    while (node != null) {
      result.push(node.getElement());
      node = node.next();
    }
    return result;
  }

  toString(): string {
    if (this._startNode == null) {
      return "[]";
    }
    const initialNode = this._startNode;
    let currentNode = initialNode;
    let result = "[";
    let isFirst = true;
    while (currentNode != null && currentNode.next() !== initialNode) {
      if (isFirst) {
        isFirst = false;
      } else {
        result += ", ";
      }

      result += currentNode.getElement();
      currentNode = currentNode.next();
    }
    result += "]";
    return result;
  }

  removeFirst(): this {
    const startNode = this._startNode;
    if (startNode == null) {
      return this;
    }

    this._startNode = startNode.next();
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
    const secondPathNode = firstPathNode.next();
    if (secondPathNode == null) {
      throw new Error("Path to insert has to have at least 2 nodes");
    }

    const lastPathNode = path.getEndNode();
    if (lastPathNode == null) {
      throw new Error("Path to insert has to have at least 2 nodes");
    }

    const oldNextNode = node.next();
    node.linkTo(secondPathNode);
    lastPathNode.linkTo(oldNextNode);
    return this;
  }
}

module.exports = {
  Edge,
  Graph,
  Path,
  Node
};
