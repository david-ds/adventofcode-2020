let run _input = 0

let () = 
  let input = Sys.argv.(1) in
  let start = int_of_float (Sys.time() *. 1000.) in
  let result = run input in
  let end_ = int_of_float (Sys.time() *. 1000.) in
  Printf.printf "_duration:%d\n%d\n" (end_ - start) result
  