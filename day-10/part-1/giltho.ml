let compute l =
  let rec loop (ones, threes) last = function
    | [] -> ones * (threes + 1)
    | a :: r ->
        if a - last = 1 then loop (ones + 1, threes) a r
        else if a - last = 3 then loop (ones, threes + 1) a r
        else loop (ones, threes) a r
  in
  loop (0, 0) 0 l

let parse input = input |> String.split_on_char '\n' |> List.map int_of_string

let run input = parse input |> List.fast_sort Int.compare |> compute

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
