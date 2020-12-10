let compute arr =
  let len = Array.length arr in
  let acc = Array.make len 0 in
  let rec loop i =
    if i >= len then ()
    else
      let cur = arr.(i) in
      let sp = if cur - arr.(i - 3) <= 3 then acc.(i - 3) else 0 in
      let fp = if cur - arr.(i - 2) <= 3 then acc.(i - 2) else 0 in
      let () = acc.(i) <- acc.(i - 1) + fp + sp in
      loop (i + 1)
  in
  acc.(0) <- 1;
  acc.(1) <- (if arr.(1) > 3 then 1 else 2);
  acc.(2) <-
    (let f0 = if arr.(2) <= 3 then 1 else 0 in
     let f1 = if arr.(2) - arr.(0) <= 3 then 1 else 0 in
     f0 + f1 + acc.(1));
  loop 3;
  acc.(len - 1)

let parse input =
  input |> String.split_on_char '\n' |> List.map int_of_string |> Array.of_list

let run input =
  let arr = parse input in
  Array.sort Int.compare arr;
  compute arr

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
