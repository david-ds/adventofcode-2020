type field_name = Byr | Iyr | Eyr | Hgt | Hcl | Ecl | Pid | Cid
[@@deriving enum]

module Parse = struct
  open Angstrom

  let is_whitespace = function ' ' | '\n' -> true | _ -> false

  let isnt_whitespace = function ' ' | '\n' -> false | _ -> true

  let fullword = take_while1 isnt_whitespace

  let whitespace = satisfy is_whitespace

  let validate_anything =
    let+ _ = take_till is_whitespace in
    true

  let byr_f = validate_anything

  let iyr_f = validate_anything

  let eyr_f = validate_anything

  let hgt_f = validate_anything

  let hcl_f = validate_anything

  let ecl_f = validate_anything

  let pid_f = validate_anything

  let cid_f = validate_anything

  let valid_field (f : field_name) =
    match f with
    | Byr -> byr_f
    | Iyr -> iyr_f
    | Eyr -> eyr_f
    | Hgt -> hgt_f
    | Hcl -> hcl_f
    | Ecl -> ecl_f
    | Pid -> pid_f
    | Cid -> cid_f

  let f_name =
    (let+ _ = string "byr" in
     Byr)
    <|> (let+ _ = string "iyr" in
         Iyr)
    <|> (let+ _ = string "eyr" in
         Eyr)
    <|> (let+ _ = string "hgt" in
         Hgt)
    <|> (let+ _ = string "hcl" in
         Hcl)
    <|> (let+ _ = string "ecl" in
         Ecl)
    <|> (let+ _ = string "pid" in
         Pid)
    <|> let+ _ = string "cid" in
        Cid

  let field arr =
    let* f = f_name in
    let+ v = valid_field f in
    if v then
      let () = arr.(field_name_to_enum f) <- v in
      true
    else false

  let all_req_field arr =
    let cont = ref true in
    let ind = ref 0 in
    while !cont && !ind < max_field_name do
      cont := arr.(!ind) || Int.equal !ind (field_name_to_enum Cid);
      incr ind
    done;
    !cont

  let skip_rest =
    fix (fun m ->
        let* _ = fullword in
        whitespace *> m <|> return false)

  let passport () =
    let arr = Array.make (max_field_name + 1) false in
    let rec go () =
      let* f = field arr in
      if f then whitespace *> go () <|> return (all_req_field arr)
      else skip_rest
    in
    go ()

  let double_newline = string "\n\n" >>| fun _ -> ()

  let file =
    let rec go acc =
      let* p = passport () in
      let acc = if p then acc + 1 else acc in
      double_newline *> go acc <|> return acc
    in
    go 0
end

let run input =
  Result.get_ok @@ Angstrom.parse_string ~consume:All Parse.file input

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
