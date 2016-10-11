(*

  A binomial tree can be defined recursively based on its rank. The base is a tree
  of rank 1, which is a single node. A tree of rank n > 1, is defined as

*)

type elemType = int;;
(*
  The list of nodes in the subtree list is of decreasing order of rank
*)
type treeType = Node of int * elemType * treeType list;;
(*
  The list of nodes in tree list is of increasing order of rank
*)
type heapType = treeType list;;

exception Invariant_violation of string;;

(*
  Construct a node by combining two nodes of the same rank
  TODO: Add the invariant rank(heapA) = rank(heapB)
*)
let link (treeA: treeType) (treeB: treeType): treeType =
  match (treeA, treeB) with
    | (Node (rankA, elemA, childrenA), Node (rankB, elemB, childrenB)) ->
      let () = assert (rankA == rankB) in
      if elemA <= elemB then Node (rankA + 1, elemA, treeB :: childrenA)
      else Node (rankA + 1, elemB, treeA :: childrenB)
;;

let rank (Node (rank, _, _)) = rank;;
let root (Node (_, elem, _)) = elem;;
let singletonTree (elem: elemType) = Node (1, elem, [])
let emptyHeap = []

(*
  Inserts a tree inside a heap.
  Invariant: rank tree >= rank of the highest ranked tree in the heap
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
        insertTree tree rest
;;

let insert (element: elemType) (heap: heapType): heapType =
  insertTree (singletonTree element) heap

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

let findMin (heap: heapType) =
  let (minTree, _) = removeMinTree heap in
    match minTree with
      | None -> None
      | Some tree -> Some (root tree)
;;

let removeMin (heap: heapType) =
  let (minTree, rest) = removeMinTree heap in
  match minTree with
    | None -> []
    | Some (Node (_, _, children)) -> merge (List.rev children) rest
;;
