type cmd = Jmp of int | Nop of int | Acc of int

type state = { index : int; acc : int }

let init_state = { index = 0; acc = 0 }

let small_step cmd state =
  let { index; acc } = state in
  match cmd with
  | Jmp i -> { state with index = index + i }
  | Acc i -> { index = index + 1; acc = acc + i }
  | Nop _ -> { state with index = index + 1 }

let find_infinite_loop cmds =
  let visited = Array.make (Array.length cmds) false in
  let rec loop state =
    let { index; acc } = state in
    if visited.(index) then acc
    else (
      visited.(index) <- true;
      loop (small_step cmds.(index) state) )
  in
  loop init_state

let parse input =
  let parse_line l =
    match String.split_on_char ' ' l with
    | [ "jmp"; b ] -> Jmp (int_of_string b)
    | [ "nop"; b ] -> Nop (int_of_string b)
    | [ "acc"; b ] -> Acc (int_of_string b)
    | _ -> failwith "Impossible"
  in
  let lst = String.split_on_char '\n' input in
  lst |> List.map parse_line |> Array.of_list

let run ~start input =
  let prg = parse input in
  Printf.printf "_parsing_time:%f\n" ((Sys.time () *. 1000.) -. start);
  find_infinite_loop prg

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run ~start input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
