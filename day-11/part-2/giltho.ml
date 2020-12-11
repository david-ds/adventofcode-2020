let get_lsize str =
  let rec loop i = match str.[i] with '\n' -> i | _ -> loop (i + 1) in
  loop 0

let get_exn ~lsize b i j = Bytes.get b (((lsize + 1) * i) + j)

let set_exn ~lsize b i j c = Bytes.set b (((lsize + 1) * i) + j) c

let rec occupied_on_line ~mi ~mj ~lsize b i j =
  let i = mi i in
  let j = mj j in
  match get_exn ~lsize b i j with
  | '#' -> true
  | 'L' | '\n' -> false
  | '.' -> occupied_on_line ~mi ~mj ~lsize b i j
  | _ -> failwith "unrecognize char"
  | exception _ -> false

let count ~lsize b i j =
  let add_if_see mi mj x =
    if x >= 5 then x
    else if occupied_on_line ~mi ~mj ~lsize b i j then x + 1
    else x
  in
  let id x = x in
  let incr x = x + 1 in
  let decr x = x - 1 in
  0 |> add_if_see decr decr |> add_if_see decr id |> add_if_see decr incr
  |> add_if_see id decr |> add_if_see id incr |> add_if_see incr decr
  |> add_if_see incr id |> add_if_see incr incr

let no_adj_occupied ~lsize b i j =
  let on_line mi mj = occupied_on_line ~mi ~mj ~lsize b i j in
  let id x = x in
  let incr x = x + 1 in
  let decr x = x - 1 in
  not
    ( on_line decr decr || on_line decr id || on_line decr incr
    || on_line id decr || on_line id incr || on_line incr decr
    || on_line incr id || on_line incr incr )

let new_state ~lsize b i j =
  match get_exn ~lsize b i j with
  | '.' -> ('.', false)
  | 'L' -> if no_adj_occupied ~lsize b i j then ('#', true) else ('L', false)
  | '#' -> if count ~lsize b i j >= 5 then ('L', true) else ('#', false)
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
