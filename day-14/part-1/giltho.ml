let ( +$ ) = Int64.add

let ( *$ ) = Int64.mul

let ( -$ ) = Int64.sub

let ( |$ ) = Int64.logor

let ( &$ ) = Int64.logand

let ( += ) r i = r := !r +$ i

let ( -= ) r i = r := !r -$ i

let rec pow x n =
  match n with
  | 0 -> 1L
  | 1 -> x
  | n ->
      let r = pow x (n / 2) in
      let z = if n mod 2 = 0 then 1L else x in
      r *$ r *$ z

let ( ** ) = pow

type instr = Mem of int * int64 | Mask of (int64 * int64)

let parse_line l =
  match l.[1] with
  | 'e' ->
      let eq_index = String.index l '=' in
      let addr = String.sub l 4 (eq_index - 6) |> int_of_string in
      let value =
        String.sub l (eq_index + 2) (String.length l - eq_index - 2)
        |> Int64.of_string
      in
      Mem (addr, value)
  | _ ->
      let ones = ref 0L in
      let zeros = ref ((2L ** 36) -$ 1L) in
      for i = 7 to 42 do
        let k = 42 - i in
        match l.[i] with
        | '1' -> ones += (2L ** k)
        | '0' -> zeros -= (2L ** k)
        | _ -> ()
      done;
      Mask (!ones, !zeros)

let iter_input ~f () =
  try
    while true do
      let l = input_line stdin in
      f (parse_line l)
    done
  with End_of_file -> ()

let heap = Hashtbl.create 200

let final_sum () = Hashtbl.fold (fun (_ : int) v acc -> v +$ acc) heap 0L

let apply_mask v (ones, zeros) = v |$ ones &$ zeros

let run () =
  let mask = ref (0L, 0L) in
  iter_input
    ~f:(function
      | Mask m -> mask := m
      | Mem (addr, v) -> Hashtbl.replace heap addr (apply_mask v !mask))
    ();
  final_sum ()

let () =
  let start = Sys.time () *. 1000. in
  let result = run () in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%Ld\n" (end_ -. start) result
