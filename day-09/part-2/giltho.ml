let psize = 25

let find_two ~input low high v =
  let rec loop_int vp k =
    if k > high then false else vp + input.(k) = v || loop_int vp (k + 1)
  in
  let rec loop_ext c =
    if c >= high then false else loop_int input.(c) (c + 1) || loop_ext (c + 1)
  in
  loop_ext low

let find_first input =
  let rec aux cur_i =
    let cur = input.(cur_i) in
    if find_two ~input (cur_i - psize) (cur_i - 1) cur then aux (cur_i + 1)
    else cur
  in
  aux psize

let parse input =
  String.split_on_char '\n' input |> Array.of_list |> Array.map int_of_string

let min_max_sum input low high =
  let rec fold l h c =
    if c > high then l + h
    else
      let v = input.(c) in
      fold (min l v) (max h v) (c + 1)
  in
  fold max_int 0 low

let find_vuln searched input =
  let rec loop sum low high st =
    match st with
    | `Incr ->
        let new_val = input.(high + 1) in
        if new_val >= searched then
          loop input.(high + 2) (high + 2) (high + 2) `Incr
        else
          let new_sum = sum + new_val in
          if new_sum = searched then min_max_sum input low (high + 1)
          else if new_sum < searched then loop new_sum low (high + 1) `Incr
          else loop new_sum low (high + 1) `Decr
    | `Decr ->
        let val_to_remove = input.(low) in
        let new_sum = sum - val_to_remove in
        if new_sum = searched then min_max_sum input (low + 1) high
        else if new_sum < searched then loop new_sum (low + 1) high `Incr
        else loop new_sum (low + 1) high `Decr
  in
  loop input.(0) 0 0 `Incr

let run input =
  let parsed = parse input in
  let value = find_first parsed in
  find_vuln value parsed

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
