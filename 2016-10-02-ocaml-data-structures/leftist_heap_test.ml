open OUnit2;;
open Leftist_heap;;

(* Rank tests*)
let testRankForEmptyHeap test_ctx =
  assert_equal (Leftist_heap.rank Empty) 0;;

(* Rank is not computed on the fly. *)
let testRankForSingleNodeHeap test_ctx =
  assert_equal (Leftist_heap.rank (Tree (10, 1, Empty, Empty))) 10;;

let testTwoHeapsAreTheSame test_ctx =
  assert_bool "Should return true for the same heap structure"
    (Leftist_heap.equals
      (Tree (1, 1, Empty, Empty))
      (Tree (1, 1, Empty, Empty))
    )
;;

let testHeapsWithDifferentElementsAreDifferent test_ctx =
  assert_bool "Should return false for different heap structures"
    (not (Leftist_heap.equals
      (Tree (1, 1, Empty, Empty))
      (Tree (1, 2, Empty, Empty))
    ))
;;

let testHeapsWithDifferentRanksAreDifferent test_ctx =
  assert_bool "Should return false for different heap structures"
    (not (Leftist_heap.equals
      (Tree (2, 1, Empty, Empty))
      (Tree (1, 1, Empty, Empty))
    ))
;;

(* Helper function for a more expressive heap insertion *)
let insertInHeap element heap = Leftist_heap.insert heap element
;;
let rec insertListInHeap heap elements = match elements with
  | [] -> heap
  | (head :: rest) -> insertListInHeap (Leftist_heap.insert heap head) rest
;;
let deleteMinFromHeap heap = Leftist_heap.deleteMin heap
;;

let testMultipleInsertionsStep1 test_ctx =
  let heap = insertListInHeap Empty [1] in
  assert_bool "" (Leftist_heap.equals
    heap
    (Tree (1, 1, Empty, Empty))
  )
;;

let testMultipleInsertionsStep2 test_ctx =
  let heap = insertListInHeap Empty [1; 3] in
  assert_bool "" (Leftist_heap.equals
    heap
    (Tree (1, 1,
      Tree (1, 3, Empty, Empty),
      Empty
    ))
  )
;;

let testMultipleInsertionsStep3 test_ctx =
  let heap = insertListInHeap Empty [1; 3; 4] in
  assert_bool "" (Leftist_heap.equals
    heap
    (Tree (2, 1,
      Tree (1, 3, Empty, Empty),
      Tree (1, 4, Empty, Empty)
    ))
  )
;;

let testMultipleInsertionsStep4 test_ctx =
  let heap = insertListInHeap Empty [1; 3; 4; 2] in
  assert_bool "" (Leftist_heap.equals
    heap
    (Tree (2, 1,
      Tree (1, 3, Empty, Empty),
      Tree (1, 2,
        Tree (1, 4, Empty, Empty),
        Empty
      )
    ))
  )
;;

let testRemoval test_ctx =
  let heap =
    insertListInHeap Empty [1; 3; 4; 2] |>
    deleteMinFromHeap in
  assert_bool "" (Leftist_heap.equals
    heap
    (Tree (2, 2,
      Tree (1, 4, Empty, Empty),
      Tree (1, 3, Empty, Empty)
    ))
  )
;;

let suite =
"suite">:::
 [
  "testRankForEmptyHeap">:: testRankForEmptyHeap;
  "testRankForSingleNodeHeap">:: testRankForSingleNodeHeap;
  "testTwoHeapsAreTheSame">:: testTwoHeapsAreTheSame;
  "testHeapsWithDifferentElementsAreDifferent">:: testHeapsWithDifferentElementsAreDifferent;
  "testHeapsWithDifferentRanksAreDifferent">:: testHeapsWithDifferentRanksAreDifferent;
  "testMultipleInsertionsStep1">:: testMultipleInsertionsStep1;
  "testMultipleInsertionsStep2">:: testMultipleInsertionsStep2;
  "testMultipleInsertionsStep3">:: testMultipleInsertionsStep3;
  "testMultipleInsertionsStep4">:: testMultipleInsertionsStep4;
  "testRemoval">:: testRemoval
 ]
;;

let () =
  run_test_tt_main suite
;;
