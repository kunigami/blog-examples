open Trie
open Printf
open Batteries

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
  List.fold_right Trie.insertString words Trie.empty;;

(* Search for all subsequences of s in a trie *)
let rec searchSubsequenceImpl (s: char list) (trie: trie): char list list = match s with
  | [] -> []
  | first_char :: rest_s ->
    let Node(children, _) = trie in
    (* Branch 1: Pick character *)
    let withChar =  if Trie.ChildList.mem first_char children
      then
        let nextNode = Trie.ChildList.find first_char children in
        let matches = searchSubsequenceImpl rest_s nextNode in
        let Node(_, next_is_word) = nextNode in
        let fullMatches = if next_is_word then ([] :: matches) else matches in
        (* Add the current matching character to all matches *)
        List.map (fun word -> first_char :: word) fullMatches
      else []
    in
    (* Branch 2: Do not pick character *)
    let withoutChar = searchSubsequenceImpl rest_s trie
    in
    (* Merge results *)
    withChar @ withoutChar

let rec removeDuplicatesImpl
  (prevWord: string)
  (sortedWords: string list)
: string list = match sortedWords with
  | [] -> []
  | nextWord :: sortedWordsRest ->
    let uniqueWords = removeDuplicatesImpl nextWord sortedWordsRest in
    if String.equal prevWord nextWord then uniqueWords
    else nextWord :: uniqueWords

let removeDuplicates (words: string list): string list =
  match (List.sort String.compare words) with
    | [] -> []
    | firstWord :: sortedWordsRest ->
      firstWord :: (removeDuplicatesImpl firstWord sortedWordsRest)

let searchSubsequence (s: string) (trie: trie): string list =
  let chars = String.to_list s in
  let results = searchSubsequenceImpl chars trie in
  List.map String.of_list results |> removeDuplicates

let rec top (n: int) (xs: 'a list): 'a list = match xs with
  | [] -> []
  | x :: rest -> if n == 0 then [] else x :: (top (n - 1) rest)

let resultToString (r: string * float): string =
  "(" ^ (fst r) ^ ", " ^ String.of_float(snd r) ^ ")"

(*
  Given a dictionary (list of words), find, for each word, all the subsequences
  of it in the dictionary.
*)
let () =
  let lines = readFile file in
  let trie = constructTrie lines in
  let results = List.map (fun word ->
    let results = searchSubsequence word trie in
    (
      word,
      (float_of_int (List.length results)) /. (float_of_int (String.length word))
    )
  ) lines |>
  (* Select the top scores first *)
  List.sort (fun pair1 pair2 -> compare (snd pair2) (snd pair1)) |>
  top 100 in
  print_endline (String.concat "\n" (List.map resultToString results)
)
