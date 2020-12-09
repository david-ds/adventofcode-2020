type cmd = Jmp of int | Nop of int | Acc of int

type state = { index : int; acc : int }

let init_state = { index = 0; acc = 0 }

let safe_small_step cmd state =
  let { index; acc } = state in
  match cmd with
  | Jmp i when index + i < 0 -> Error ()
  | Jmp i -> Ok { state with index = index + i }
  | Acc i -> Ok { index = index + 1; acc = acc + i }
  | Nop _ -> Ok { state with index = index + 1 }

let is_program_ok ~init cmds =
  let length = Array.length cmds in
  let visited = Array.make (Array.length cmds) false in
  let rec loop state =
    let { index; acc } = state in
    if index >= length then Ok acc
    else if visited.(index) then Error ()
    else (
      visited.(index) <- true;
      match safe_small_step cmds.(index) state with
      | Ok state -> loop state
      | Error () -> Error () )
  in
  loop init

let find_and_fix cmds =
  let small_step cmd state = safe_small_step cmd state |> Result.get_ok in
  let rec loop state =
    let index = state.index in
    match cmds.(index) with
    | Acc _ as cmd -> loop (small_step cmd state)
    | Jmp i as cmd -> (
        let () = cmds.(index) <- Nop i in
        match is_program_ok ~init:state cmds with
        | Ok acc -> acc
        | Error () ->
            let () = cmds.(index) <- cmd in
            loop (small_step cmd state) )
    | Nop i as cmd -> (
        let () = cmds.(index) <- Jmp i in
        match is_program_ok ~init:state cmds with
        | Ok acc -> acc
        | Error () ->
            let () = cmds.(index) <- cmd in
            loop (small_step cmd state) )
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

let run input =
  let prg = parse input in
  find_and_fix prg

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
