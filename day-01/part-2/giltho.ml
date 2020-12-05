let memo = Array.make 2021 false

let try_number ~acc n =
  memo.(n) <- true;
  let rec aux = function
    | [] -> None
    | a :: r ->
        if a + n > 2020 then aux r
        else
          let compl = 2020 - a - n in
          if memo.(compl) then Some (compl * a * n) else aux r
  in
  aux acc

module Parse = struct
  open Angstrom

  let integer =
    take_while1 (function '0' .. '9' -> true | _ -> false) >>| int_of_string

  let result =
    let rec go acc =
      let* i = integer in
      match try_number ~acc i with
      | Some x -> return x
      | None -> char '\n' *> go (i :: acc)
    in
    go []
end

let run input =
  Result.get_ok (Angstrom.parse_string ~consume:Prefix Parse.result input)

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
