(*
  Implementation of streams based on Chapter 4 of Purely Functional Data
  Structures.
*)

type 'a streamCell = Nil | StreamCell of 'a * 'a stream and
     'a stream = ('a streamCell) Lazy.t

(*
  StreamCelltructs a stream from a list
*)
let rec fromList (l: 'a list): ('a stream) = match l with
  | [] -> lazy Nil
  | x :: xs -> lazy (StreamCell (x, fromList xs))
;;

(*
  Evaluates the entire stream as a list
*)
let rec toList (stream: 'a stream): ('a list) =
  let computedStream = Lazy.force stream in
  match computedStream with
    | Nil -> []
    | StreamCell (elem, rest) -> elem :: (toList rest)
;;

(*
  Concatenate two streams. Note that it never evaluates streamB and it only
  evaluates the first cell of streamA.
*)
let rec (++) (streamA: 'a stream) (streamB: 'a stream): ('a stream) =
  let computedStreamA = Lazy.force streamA in
  match computedStreamA with
    | Nil -> streamB
    | StreamCell (elem, rest) -> lazy (StreamCell (elem, rest ++ streamB))
;;

(*
  Lazily extracts the first n elements from a stream. Recursive calls are
  delayed
*)
let rec take (n: int) (stream: 'a stream) : ('a stream) =
  if n == 0 then lazy Nil
  else
    let computedStream = Lazy.force stream in
    match computedStream with
      | Nil -> lazy Nil
      | StreamCell (elem, rest) -> lazy (StreamCell (elem, (take (n - 1) rest)))
;;

(*
  Drops the first n elements from a stream. Has to evaluate the dropped
  elements (i.e. recursive calls are not delayed)
*)
let rec drop (n: int) (stream: 'a stream): ('a stream) =
  if n == 0 then stream
  else
    let computedStream = Lazy.force stream in
    match computedStream with
      | Nil -> lazy Nil
      | StreamCell (_, rest) -> drop (n - 1) rest
;;

(*
  Reverse the order of the elements in the stream. Has to evaluate the entire
  stream
*)
let reverse (stream: 'a stream): ('a stream) =
  let rec reverse' = fun oldStream newStream ->
    let computedStream = Lazy.force oldStream in
    match computedStream with
      | Nil -> newStream
      | StreamCell (elem, rest) -> reverse' rest  (lazy (StreamCell (elem, newStream)))
  in reverse' stream (lazy Nil)
;;
