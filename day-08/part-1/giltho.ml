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

module Parser = struct
  open Angstrom

  let integer =
    take_while1 (function '0' .. '9' -> true | _ -> false) >>| int_of_string

  let positive = char '+' *> integer

  let negative = char '-' *> integer >>| fun i -> -i

  let argument = negative <|> positive

  let cmd =
    string "jmp"
    >>= (fun _ -> char ' ' *> argument >>| fun i -> Jmp i)
    <|> ( string "nop" >>= fun _ ->
          char ' ' *> argument >>| fun i -> Nop i )
    <|> ( string "acc" >>= fun _ ->
          char ' ' *> argument >>| fun i -> Acc i )

  let cmds = sep_by1 (char '\n') cmd >>| Array.of_list
end

let run input =
  let prg =
    Angstrom.parse_string ~consume:All Parser.cmds input |> function
    | Ok x -> x
    | Error s -> failwith s
  in
  find_infinite_loop prg

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
