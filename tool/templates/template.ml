let run () = 0

let () =
  (* Input is given is Sys.argv.(1) as well as stdin *)
  let start = Sys.time () *. 1000. in
  let result = run () in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
