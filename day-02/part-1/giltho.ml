type state =
  | Start
  | Acc_low of char list
  | Only_low of int
  | Acc_high of int * char list
  | Low_and_high of (int * int)
  | Count of int
  | SkipRest

let state = ref Start

let count = ref 0

let last_policy_low = ref 0

let last_policy_high = ref 0

let last_policy_letter = ref 'a'

let set_policy i j c =
  last_policy_low := i;
  last_policy_high := j;
  last_policy_letter := c

let incr_if_valid i = if i >= !last_policy_low then incr count

let is_too_big i = i > !last_policy_high

let jump = ref 0

let int_of_char c = Char.code c - 48

let int_of_rev_char_list l =
  let rec aux pow acc = function
    | [] -> acc
    | a :: r ->
        let a = int_of_char a in
        let acc = acc + (pow * a) in
        aux (10 * pow) acc r
  in
  aux 1 0 l

let iter c =
  if !jump > 0 then decr jump
  else
    let new_state =
      match (!state, c) with
      | Start, _ -> Acc_low [ c ]
      | Acc_low l, '-' -> Only_low (int_of_rev_char_list l)
      | Acc_low l, c -> Acc_low (c :: l)
      | Only_low i, _ -> Acc_high (i, [ c ])
      | Acc_high (i, l), ' ' -> Low_and_high (i, int_of_rev_char_list l)
      | Acc_high (i, l), c -> Acc_high (i, c :: l)
      | Low_and_high (i, j), c ->
          jump := 2;
          set_policy i j c;
          Count 0
      | Count i, '\n' ->
          incr_if_valid i;
          Start
      | Count i, c ->
          if Char.equal c !last_policy_letter then
            if Int.equal i !last_policy_high then SkipRest else Count (i + 1)
          else Count i
      | SkipRest, '\n' -> Start
      | SkipRest, _ -> SkipRest
    in

    state := new_state

let run input =
  let () = String.iter iter input in
  let () = match !state with Count i -> incr_if_valid i | _ -> () in
  !count

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
