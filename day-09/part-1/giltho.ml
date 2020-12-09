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

let run input = input |> parse |> find_first

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
