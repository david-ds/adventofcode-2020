module SS = Set.Make (String)

let graph = Hashtbl.create 100

let count_per_container = Hashtbl.create 100

let register container containee = Hashtbl.add graph container containee

let rec count_for_container container =
  match Hashtbl.find_opt count_per_container container with
  | Some n -> n
  | None ->
      let n =
        List.fold_left
          (fun acc (k, b) -> acc + (k * count_for_container b))
          1
          (Hashtbl.find graph container)
      in
      Hashtbl.add count_per_container container n;
      n

module Parser = struct
  open Angstrom

  let word = take_while1 (function 'a' .. 'z' -> true | _ -> false)

  let integer =
    take_while1 (function '0' .. '9' -> true | _ -> false) >>| int_of_string

  let bag_type =
    scan_string `Adj (fun st c ->
        match (st, c) with
        | `Adj, ' ' -> Some `Col
        | `Col, ' ' -> None
        | st, _ -> Some st)

  let container = bag_type <* string " bags contain "

  let bags_plur qty = if qty > 1 then string " bags" else string " bag"

  let containee =
    let* qty = integer <* char ' ' in
    let+ typ = bag_type <* bags_plur qty in
    (qty, typ)

  let several_containees = sep_by1 (string ", ") containee

  let no_containees = string "no other bags" >>| fun _ -> []

  let rule =
    let* container = container in
    let+ containees = no_containees <|> several_containees <* char '.' in
    register container containees

  let rules =
    fix (fun rules -> rule >>= fun () -> char '\n' *> rules <|> return ())
end

let run input =
  let () =
    Result.get_ok (Angstrom.parse_string ~consume:All Parser.rules input)
  in
  count_for_container "shiny gold" - 1

let () =
  print_newline ();
  print_newline ();
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
