module Parse = struct
  open Angstrom

  let int_of_char c = Char.code c - 48

  let parens e = char '(' *> e <* char ')'

  let nl = char '\n'

  let digit = any_char >>| int_of_char

  let plus = string " + " *> return ( + )

  let times = string " * " *> return ( * )

  let chainl1 e op =
    let rec go acc = lift2 (fun f x -> f acc x) op e >>= go <|> return acc in
    e >>= go

  let expr = fix (fun expr -> chainl1 (parens expr <|> digit) (plus <|> times))

  let all = fix (fun m -> lift2 ( + ) expr (nl *> m <|> return 0))
end

let run input =
  match Angstrom.parse_string ~consume:All Parse.all input with
  | Ok s -> s
  | Error s -> failwith s

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
