(*

  A spine of a node is the path defined by following the right children
  until a leaf is found (i.e. the rightmost path). The rank is the length
  of the spine.

  A leftist heap is a binary tree such that the value of a parent is greater
  or equal than its children and the rank of the left child is always greater
  or equal than the right child.

  The rank of a tree with n nodes is O(log n).

*)
module LeftistHeap = struct
  type elemType = int
  (* We store the rank as part of the node *)
  type heapType = Empty | Tree of int * elemType * heapType * heapType

  let rank heap =
    match heap with
      | Empty -> 0
      | Tree(r, _, _, _) -> r

  let newHeap (elem: elemType): heapType = Tree(1, elem, Empty, Empty)

  (*
    Construct a heap tree by preserving the leftist property by swapping the
    left and right children if necessary.
  *)
  let makeTree (elem: elemType) (left: heapType) (right: heapType): heapType =
    if rank left < rank right then Tree((rank left) + 1, elem, right, left)
    else Tree((rank right) + 1, elem, left, right)

  let rec merge (heapA: heapType) (heapB: heapType): heapType =
    match (heapA, heapB) with
      | (heapA, Empty) -> heapA
      | (Empty, heapB) -> heapB
      | (Tree(r1, elem1, left1, right1), Tree(r2, elem2, left2, right2)) ->
        if elem1 > elem2 then makeTree elem1 left1 (merge right1 heapB)
        else makeTree elem2 left2 (merge right2  heapA)

  let insert (heap: heapType) (elem: elemType): heapType =
    merge heap (newHeap elem)

  let findMin (heap: heapType) =
    match heap with
      | Empty -> None
      | Tree(_, elem, _, _) -> Some elem

  let deleteMin (heap: heapType) =
    match heap with
      | Empty -> Empty
      | Tree (_, _, left, right) -> merge left right

end

(* Examples *)

let h = LeftistHeap.newHeap 10;;
(* 11 becomes root *)
let h = LeftistHeap.insert h 11;;
let h = LeftistHeap.insert h 9;;
