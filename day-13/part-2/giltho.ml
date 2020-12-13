let rec egcd a b =
  if b = 0 then (1, 0)
  else
    let q = a / b and r = a mod b in
    let s, t = egcd b r in
    (t, s - (q * t))

let mod_inv a b =
  let x, y = egcd a b in
  if (a * x) + (b * y) = 1 then Some x else None

let calc_inverses ns ms =
  let rec list_inverses ns ms l =
    match (ns, ms) with
    | [], [] -> Some l
    | [], _ | _, [] -> assert false
    | n :: ns, m :: ms -> (
        let inv = mod_inv n m in
        match inv with None -> None | Some v -> list_inverses ns ms (v :: l) )
  in
  Option.bind (list_inverses ns ms []) (fun l -> Some (List.rev l))

let list_reduce l ~f =
  match l with [] -> failwith "bite" | hd :: tl -> List.fold_left f hd tl

let rec list_map3 la lb lc ~f =
  match (la, lb, lc) with
  | a :: ra, b :: rb, c :: rc -> f a b c :: list_map3 ra rb rc ~f
  | [], [], [] -> []
  | _ -> failwith "bite"

let chinese_remainder congruences =
  let residues, modulii = List.split congruences in
  let mod_pi = list_reduce modulii ~f:( * ) in
  let crt_modulii = List.map (fun m -> mod_pi / m) modulii in
  Option.bind (calc_inverses crt_modulii modulii) (fun inverses ->
      Some
        ( list_map3 residues inverses crt_modulii ~f:(fun a b c -> a * b * c)
        |> list_reduce ~f:( + )
        |> fun n ->
          let n' = n mod mod_pi in
          if n' < 0 then n' + mod_pi else n' ))

let parse () =
  let _ = input_line stdin in
  let vs = String.split_on_char ',' (input_line stdin) in
  let vsi = List.mapi (fun i v -> (-i, v)) vs in
  let values =
    List.filter_map
      (function _, "x" -> None | i, v -> Some (i, int_of_string v))
      vsi
  in
  values

let run () =
  let values = parse () in
  Option.get (chinese_remainder values)

let () =
  let start = Sys.time () *. 1000. in
  let result = run () in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
