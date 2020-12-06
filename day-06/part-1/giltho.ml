type state = NextPerson | NextGroup | Reading

let char_code_a = Char.code 'a'

let add_to_array arr c =
  let ofs = Char.code c - char_code_a in
  arr.(ofs) <- true

let count_true_and_reset arr =
  let acc = ref 0 in
  for i = 0 to 25 do
    if arr.(i) then (
      incr acc;
      arr.(i) <- false )
  done;
  !acc

let count_true arr =
  let acc = ref 0 in
  for i = 0 to 25 do
    if arr.(i) then incr acc
  done;
  !acc

let readInput input =
  let len = String.length input in
  let hash = Array.make 26 false in
  let rec loop i total state =
    if i >= len then total + count_true hash
    else
      match (state, input.[i]) with
      | NextPerson, '\n' ->
          let total = total + count_true_and_reset hash in
          loop (i + 1) total NextGroup
      | Reading, '\n' -> loop (i + 1) total NextPerson
      | _, c ->
          add_to_array hash c;
          loop (i + 1) total Reading
  in
  loop 0 0 NextPerson

let run input = readInput input

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
