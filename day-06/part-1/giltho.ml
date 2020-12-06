type state = NextPerson | NextGroup | Reading

let char_code_a = Char.code 'a'

let add_to_array arr c =
  let ofs = Char.code c - char_code_a in
  arr.(ofs) <- true

let count_true arr =
  Array.fold_left (fun acc x -> if x then acc + 1 else acc) 0 arr

let readInput input =
  let len = String.length input in
  let rec loop i total state current_hash =
    if i >= len then total
    else
      match (state, input.[i]) with
      | NextPerson, '\n' ->
          let total = total + count_true current_hash in
          let arr = Array.make 26 false in
          loop (i + 1) total NextGroup arr
      | Reading, '\n' -> loop (i + 1) total NextPerson current_hash
      | _, c ->
          add_to_array current_hash c;
          loop (i + 1) total Reading current_hash
  in
  loop 0 0 NextPerson (Array.make 26 false)

let run input = readInput input

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
