open OUnit2;;
open Subsequence;;
open Trie;;

let testConstructingTrie text_ctx =
  let trie = Subsequence.constructTrie ["abc" ; "ab" ; "a"] in
  assert_bool "Should all strings inserted" (
    (Trie.hasString "abc" trie) &&
    (Trie.hasString "ab" trie) &&
    (Trie.hasString "a" trie)
  )
;;

let testSubsequenceSearch text_ctx =
  let trie = Subsequence.constructTrie
    ["a" ; "ab" ; "abc" ; "ac" ; "aa" ; "ad" ; "bc"] in
  let sortedResults = Subsequence.searchSubsequence "abc" trie |>
      List.sort String.compare
  in
  assert_equal ~msg:"Should find the subsequences properly"
    ["a"; "ab"; "abc"; "ac"; "bc"] sortedResults

let testRemovingDuplicates text_ctx =
  let results = Subsequence.removeDuplicates ["a" ; "b" ; "b"; "a" ; "b" ; "c"] in
  assert_equal ["a" ; "b" ; "c"] results

let suite =
"suite">:::
 [
    "testConstructingTrie">:: testConstructingTrie;
    "testSubsequenceSearch">:: testSubsequenceSearch;
    "testRemovingDuplicates">:: testRemovingDuplicates;
 ]
;;

let () =
  run_test_tt_main suite
;;
