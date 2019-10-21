open OUnit2;;
open Binomial_heap;;

let rec insertValues (heap: heapType) (values: elemType list) =
  match values with
    | [] -> heap
    | value :: rest -> insertValues (Binomial_heap.insert value heap) rest
;;

let rec extractValues (heap: heapType): int list =
  match heap with
    | [] -> []
    | heap ->
      let maybeMinElem = findMin heap in
        match maybeMinElem with
          | None -> []
          | Some minElem ->
            let newHeap = removeMin heap in
            minElem :: (extractValues newHeap)
;;

(* Rank tests*)
let testSortingViaHeap test_ctx =
  let heap = insertValues Binomial_heap.emptyHeap [5; 7; 3; 1; 10; 8] in
  let sortedList = extractValues heap in
  assert_equal sortedList [1; 3; 5; 7; 8; 10];;

let suite =
"suite">:::
 [
  "testSortingViaHeap">:: testSortingViaHeap;
 ]
;;

let () =
  run_test_tt_main suite
;;
