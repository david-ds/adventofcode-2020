let memo = Array.make 2021 false

let try_number x =
  let compl = 2020 - x in
  if memo.(compl) then Some (x * compl)
  else (
    memo.(x) <- true;
    None)

module Parse = struct
  open Angstrom

  let integer =
    take_while1 (function '0' .. '9' -> true | _ -> false) >>| int_of_string

  let result =
    fix (fun result ->
        let* i = integer in
        match try_number i with
        | Some r -> return r
        | None -> char '\n' *> result)
end

let run input =
  Result.get_ok (Angstrom.parse_string ~consume:Prefix Parse.result input)

let () =
  let input = Sys.argv.(1) in
  let start = int_of_float (Sys.time () *. 1000.) in
  let result = run input in
  let end_ = int_of_float (Sys.time () *. 1000.) in
  Printf.printf "_duration:%d\n%d\n" (end_ - start) result
