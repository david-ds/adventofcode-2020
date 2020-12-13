let parse () =
  let timestamp = int_of_string (input_line stdin) in
  let buffer = Buffer.create 10 in
  let seq =
    Seq.unfold
      (fun b ->
        if b then None
        else
          let b = ref false in
          let cont = ref true in
          while !cont do
            let x =
              try input_char stdin
              with End_of_file ->
                b := true;
                ','
            in
            match x with ',' -> cont := false | c -> Buffer.add_char buffer c
          done;
          let content = Buffer.contents buffer in
          Buffer.clear buffer;
          Some (content, !b))
      false
  in
  (timestamp, seq)

let run () =
  let timestamp, seq = parse () in
  let bus, wait =
    Seq.fold_left
      (fun acc v ->
        match v with
        | "x" -> acc
        | _ ->
            let bus = int_of_string v in
            let _, cwait = acc in
            let new_wait = bus - (timestamp mod bus) in
            if new_wait < cwait then (bus, new_wait) else acc)
      (0, max_int) seq
  in
  bus * wait

let () =
  let start = Sys.time () *. 1000. in
  let result = run () in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
