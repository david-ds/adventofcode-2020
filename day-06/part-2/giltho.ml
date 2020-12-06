type state = NextPerson | NextGroup | Reading

let char_code_a = Char.code 'a'

let add_to_array arr c =
  let ofs = Char.code c - char_code_a in
  arr.(ofs) <- arr.(ofs) + 1

let count_equal_and_reset arr n =
  let acc = ref 0 in
  for i = 0 to 25 do
    if Int.equal arr.(i) n then incr acc;
    arr.(i) <- 0
  done;
  !acc

let count_equal arr n =
  let acc = ref 0 in
  for i = 0 to 25 do
    if Int.equal arr.(i) n then incr acc
  done;
  !acc

let readInput input =
  let len = String.length input in
  let hash = Array.make 26 0 in
  let rec loop i total state nb_people =
    if i >= len then total + count_equal hash (nb_people + 1)
    else
      match (state, input.[i]) with
      | NextPerson, '\n' ->
          let total = total + count_equal_and_reset hash nb_people in
          loop (i + 1) total NextGroup 0
      | Reading, '\n' -> loop (i + 1) total NextPerson (nb_people + 1)
      | _, c ->
          add_to_array hash c;
          loop (i + 1) total Reading nb_people
  in
  loop 0 0 NextPerson 0

let run input = readInput input

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
