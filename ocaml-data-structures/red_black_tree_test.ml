open OUnit2;;
open Red_black_tree;;

let testEqualityOfEmptyTrees text_ctx =
  assert_bool "Should return true for empty trees"
  (Red_black_tree.equals Empty Empty)
;;

let testEqualityOfSingletonTrees text_ctx =
  assert_bool "Should return true for similar singleton trees"
  (
    Red_black_tree.equals
      (Node (Red, Empty, 10, Empty))
      (Node (Red, Empty, 10, Empty))
  )
;;

let testEqualityOfDifferentColorSingletonTrees text_ctx =
  assert_bool "Should return false for trees with different colors"
  (not (
    Red_black_tree.equals
      (Node (Red, Empty, 10, Empty))
      (Node (Black, Empty, 10, Empty))
  ))
;;

let testInsertionOnEmptyTree test_ctx =
  let tree =
    insert Empty 10
  in
  assert_bool "" (Red_black_tree.equals
    tree
    (Node (Black, Empty, 10, Empty))
  )
;;

let testInsertionsStep2 test_ctx =
  let tree = List.fold_left insert Empty [10; 11]
  in
  assert_bool "" (Red_black_tree.equals
    tree
    (Node (
      Black,
      Empty,
      10,
      Node (Red, Empty, 11, Empty)
    ))
  )
;;

let testCase1OfBalancing test_ctx =
  let tree = List.fold_left insert Empty [12; 11; 10]
  in
  assert_bool "" (Red_black_tree.equals
    tree
    (Node (
      Black,
      Node (Black, Empty, 10, Empty),
      11,
      Node (Black, Empty, 12, Empty)
    ))
  )
;;

let testCase2OfBalancing test_ctx =
  let tree = List.fold_left insert Empty [12; 10; 11]
  in
  assert_bool "" (Red_black_tree.equals
    tree
    (Node (
      Black,
      Node (Black, Empty, 10, Empty),
      11,
      Node (Black, Empty, 12, Empty)
    ))
  )
;;

let testCase3OfBalancing test_ctx =
  let tree = List.fold_left insert Empty [10; 12; 11]
  in
  assert_bool "" (Red_black_tree.equals
    tree
    (Node (
      Black,
      Node (Black, Empty, 10, Empty),
      11,
      Node (Black, Empty, 12, Empty)
    ))
  )
;;

let testCase4OfBalancing test_ctx =
  let tree = List.fold_left insert Empty [10; 11; 12]
  in
  assert_bool "" (Red_black_tree.equals
    tree
    (Node (
      Black,
      Node (Black, Empty, 10, Empty),
      11,
      Node (Black, Empty, 12, Empty)
    ))
  )
;;

let suite =
"suite">:::
 [
  "testEqualityOfEmptyTrees">:: testEqualityOfEmptyTrees;
  "testEqualityOfSingletonTrees">:: testEqualityOfSingletonTrees;
  "testEqualityOfDifferentColorSingletonTrees">:: testEqualityOfDifferentColorSingletonTrees;
  "testInsertionOnEmptyTree">:: testInsertionOnEmptyTree;
  "testInsertionsStep2">:: testInsertionsStep2;
  "testCase1OfBalancing">:: testCase1OfBalancing;
  "testCase2OfBalancing">:: testCase2OfBalancing;
  "testCase3OfBalancing">:: testCase3OfBalancing;
  "testCase4OfBalancing">:: testCase4OfBalancing;
 ]
;;

let () =
  run_test_tt_main suite
;;
