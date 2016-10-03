type nodeType =
  Empty |
  Node of nodeType * int * nodeType

(* Returns the node with value @target or None if it doesn't exist *)
let rec search (tree: nodeType) (target: int) : int option =
  match tree with
    | Empty -> None
    | Node (left, value, right) ->
       if value < target then search right target
       else if value > target then search left target
       else Some value

(* Decide whether @target exists in the tree *)
let member (tree: nodeType) (target: int) =
  let searchResult = search tree target in
  match searchResult with
    | None -> false
    | Some _ -> true

(* Insert @value in the tree *)
let rec insert (tree: nodeType) (value: int) =
  match tree with
    | Empty -> Node (Empty, value, Empty)
    | Node (left, nodeValue, right) ->
      if nodeValue < value then Node (left, nodeValue, insert right value)
      else if nodeValue > value then Node (insert left value, nodeValue, right)
      else Node (left, nodeValue, right)

(* Sample trees *)
let example1 = Node (Empty, 10, Empty);;
let example2 = Node (Node (Empty, 5, Empty), 10, Node (Empty, 11, Empty))
