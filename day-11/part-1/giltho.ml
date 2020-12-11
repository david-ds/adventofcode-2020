let get_lsize str =
  let rec loop i = match str.[i] with '\n' -> i | _ -> loop (i + 1) in
  loop 0

let get_exn ~lsize b i j = Bytes.get b (((lsize + 1) * i) + j)

let set_exn ~lsize b i j c = Bytes.set b (((lsize + 1) * i) + j) c

let occupied ~lsize b i j =
  match get_exn ~lsize b i j with
  | '#' -> true
  | _ -> false
  | exception _ -> false

let count ~lsize b i j =
  let incr (k, l) x = if occupied ~lsize b k l then x + 1 else x in
  0
  |> incr (i, j - 1)
  |> incr (i - 1, j - 1)
  |> incr (i - 1, j)
  |> incr (i - 1, j + 1)
  |> incr (i, j + 1)
  |> incr (i + 1, j + 1)
  |> incr (i + 1, j)
  |> incr (i + 1, j - 1)

let no_adj_occupied ~lsize b i j =
  let occupied = occupied ~lsize b in
  not
    ( occupied i (j - 1)
    || occupied (i - 1) (j - 1)
    || occupied (i - 1) j
    || occupied (i - 1) (j + 1)
    || occupied i (j + 1)
    || occupied (i + 1) (j + 1)
    || occupied (i + 1) j
    || occupied (i + 1) (j - 1) )

let new_state ~lsize b i j =
  match get_exn ~lsize b i j with
  | '.' -> ('.', false)
  | 'L' -> if no_adj_occupied ~lsize b i j then ('#', true) else ('L', false)
  | '#' -> if count ~lsize b i j >= 4 then ('L', true) else ('#', false)
  | _ -> Fmt.failwith "unrecognized state %d %d" i j

let step ~lsize ~nlines bsrc bdst =
  let new_state = new_state ~lsize bsrc in
  let set = set_exn ~lsize bdst in
  let rec loop_columns i changed j =
    if j >= lsize then changed
    else
      let n, c = new_state i j in
      set i j n;
      loop_columns i (changed || c) (j + 1)
  in
  let rec loop_lines changed i =
    if i >= nlines then changed
    else loop_lines (loop_columns i changed 0) (i + 1)
  in
  loop_lines false 0

let main ~lsize ~nlines b1 b2 =
  let count = ref 0 in
  let rec loop src dst =
    incr count;
    let changed = step ~lsize ~nlines src dst in
    if changed then loop dst src else dst
  in
  let final_state = loop b1 b2 in
  let count = ref 0 in
  Bytes.iter (function '#' -> incr count | _ -> ()) final_state;
  !count

let run input =
  let lsize = get_lsize input in
  let nlines = (String.length input + 1) / (lsize + 1) in
  let b1 = Bytes.of_string input in
  let b2 = Bytes.of_string input in
  main ~lsize ~nlines b1 b2

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
