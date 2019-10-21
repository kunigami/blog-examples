(*

  A binomial tree can be defined recursively based on its rank. The base is a
  tree of rank 0, which is a single node. A tree of rank r > 0, is formed by
  combining two trees of rank r-1 making one tree the leftmost child of the
  other. Examples:

  rank 0: o

  rank 1: o
          |
          o

  rank 2: o
         /|
        o o
        |
        o

  rank 3: o
       / /|
      o o o
     /| |
    o o o
    |
    o

  A binomial heap is a list of binomial trees none of which has repeated ranks
  and for each binomal tree the value of a node is always greater or equal to
  its children.
*)

type rankType = int;;
type elemType = int;;
(*
  The list of nodes in the subtree list is of decreasing order of rank. For a
  rank 3 tree, the list contains a list of [rank=2, rank=1, rank=0].
*)
type treeType = Node of rankTye * elemType * treeType list;;
(*
  The list of nodes in tree list is of increasing order of rank (note it's the
  opposite order of the tree).
*)
type heapType = treeType list;;

exception Invariant_violation of string;;

(*
  Construct a node by combining two nodes of the same rank. This is the
  induction step on the definition of the tree.
*)
let link (treeA: treeType) (treeB: treeType): treeType =
  match (treeA, treeB) with
    | (Node (rankA, elemA, childrenA), Node (rankB, elemB, childrenB)) ->
      let () = assert (rankA == rankB) in
      if elemA <= elemB then Node (rankA + 1, elemA, treeB :: childrenA)
      else Node (rankA + 1, elemB, treeA :: childrenB)
;;

(*
  Helper methods
*)
let rank (Node (rank, _, _)) = rank;;
let root (Node (_, elem, _)) = elem;;
let singletonTree (elem: elemType) = Node (1, elem, []);;
let emptyHeap = [];;

(*
  Inserts a tree inside a heap.
  Invariant: trees in the heap are sorted by increasing order of rank. No
    repeated ranks.
*)
let rec insertTree (tree: treeType) (heap: heapType): heapType =
  match (tree, heap) with
    | (tree, []) -> [tree]
    | (tree, (lowestRankTree :: rest as heapTrees)) ->
      if rank tree < rank lowestRankTree then
        tree :: heapTrees
      else if rank tree == rank lowestRankTree then
        insertTree (link tree lowestRankTree) rest
      else
        failwith "This condition should not happen. The heap would be empty"
;;

(*
  Inserts an element inside a heap.
*)
let insert (element: elemType) (heap: heapType): heapType =
  insertTree (singletonTree element) heap
;;

(*
  Merge two heaps by merging their inner trees. Maintains the binomial heap
  invariants.
*)
let rec merge (heapA: heapType) (heapB: heapType) =
  match (heapA, heapB) with
    | (heapA, []) -> heapA
    | ([], heapB) -> heapB
    | ((headTreeA :: restA as heapA), (headTreeB :: restB as heapB)) ->
      if rank headTreeA > rank headTreeB then
        headTreeA :: (merge restA heapB)
      else if rank headTreeA < rank headTreeB then
        headTreeB :: (merge heapA restB)
      else (link headTreeA headTreeB) :: (merge restA restB)
;;

(*
  Remove the tree with the minimum root from the list, returning both the tree
  and the remainder of the list.
*)
let rec removeMinTree (heap: heapType) =
  match heap with
    | [] -> (None, [])
    | [tree] -> (Some tree, [])
    | tree :: rest ->
        let (maybeMinTree, minRest) = removeMinTree rest in
          match maybeMinTree with
            | None -> (None, [])
            | Some minTree ->
              if root tree <= root minTree then (Some tree, rest)
              else (Some minTree, tree :: minRest)
;;

(*
  Returns the minimum element from the heap.
*)
let findMin (heap: heapType) =
  let (minTree, _) = removeMinTree heap in
    match minTree with
      | None -> None
      | Some tree -> Some (root tree)
;;

(*
  Removes the minimum element from the heap.
*)
let removeMin (heap: heapType) =
  let (minTree, rest) = removeMinTree heap in
  match minTree with
    | None -> []
    | Some (Node (_, _, children)) -> merge (List.rev children) rest
;;
