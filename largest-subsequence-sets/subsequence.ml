open Trie;;
open Printf;;
open BatString;;
open BatList;;
open Gc;;

(* words from the dictionary *)
let file = "/usr/share/dict/words"
(* let file = "words_samples.txt" *)

(* Read lines from file until the end *)
let readFile filename =
  let lines = ref [] in
  let chan = open_in filename in
  try
    while true; do
      lines := input_line chan :: !lines
    done; !lines
  with End_of_file ->
    close_in chan;
    List.rev !lines ;;

let constructTrie (words: string list): trie =
  List.fold_left (fun t w -> Trie.insertString w t) Trie.empty words;;

(* Search for all subsequences of s in a trie *)
let rec searchSubsequenceImpl (s: char list) (trie: trie): trie = match s with
  | [] -> Trie.empty
  | first_char :: rest_s ->
    let Node(children, _) = trie in
    (* Branch 1: Pick character *)
    let trieWithChar =  if Trie.ChildList.mem first_char children
      then
        let nextNode = Trie.ChildList.find first_char children in
        let matchesTrie = searchSubsequenceImpl rest_s nextNode in
        let Node(_, next_is_word) = nextNode in
        let Node(matches, _) = matchesTrie in
        let nodeWithChar = Node(
          matches,
          next_is_word
        ) in
        (* Insert the character in front of all words returned *)
        Node (
          ChildList.(empty |> add first_char nodeWithChar),
          false
        )
      else Trie.empty
    in
    (* Branch 2: Do not pick character *)
    let trieWithoutChar = searchSubsequenceImpl rest_s trie
    in
    (* Merge results *)
    Trie.merge trieWithChar trieWithoutChar

let searchSubsequence (s: string) (trie: trie): trie =
  let chars = BatString.to_list s in
  searchSubsequenceImpl chars trie

let resultToString (r: string * int): string =
  "(" ^ (fst r) ^ ", " ^ BatString.of_int(snd r) ^ ")"

(*
  Given a dictionary (list of words), find, for each word, all the subsequences
  of it in the dictionary.
*)
let () =
  let lines = readFile file in
  let trie = constructTrie lines in
  let results = List.map (fun word ->
    let resultTrie = searchSubsequence word trie in
    let resultsCount = Trie.entriesCount resultTrie in
    (
      word,
      resultsCount
    )
  ) lines |>
  (* Select the top scores first *)
  List.sort (fun pair1 pair2 -> (snd pair2) - (snd pair1)) |>
  BatList.take 10 in
  print_endline (String.concat "\n" (List.map resultToString results)
)
