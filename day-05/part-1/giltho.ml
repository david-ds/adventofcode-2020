type state = EOL | Parsing of int

let cur_state = ref (Parsing 9)

let cur_max = ref 0

let cur_id = ref 0

let rec ( ** ) b n =
  if n == 0 then 1
  else
    let b2 = b ** (n / 2) in
    if n mod 2 = 0 then b2 * b2 else b * b2 * b2

let mul_if i c =
  match c with 'B' | 'R' -> cur_id := !cur_id + (2 ** i) | _ -> ()

let iter c =
  match !cur_state with
  | Parsing i ->
      mul_if i c;
      if i = 0 then (
        cur_max := max !cur_max !cur_id;
        cur_id := 0;
        cur_state := EOL)
      else cur_state := Parsing (i - 1)
  | EOL -> cur_state := Parsing 9

let run input =
  let () = String.iter iter input in
  !cur_max

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
