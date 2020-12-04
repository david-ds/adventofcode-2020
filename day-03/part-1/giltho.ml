module Area = struct
  type t = { block : string array; width : int; height : int }

  let parse_file s =
    let block = Array.of_list (String.split_on_char '\n' s) in

    { block; height = Array.length block; width = String.length block.(0) }

  let get_exn area x y = area.block.(x).[y]

  let is_tree_exn area x y =
    match get_exn area x y with '#' -> true | _ -> false
end

module Toboggan = struct
  type pos = { line : int; column : int }

  type state = { area : Area.t; position : pos }

  let make area =
    let zero = { line = 0; column = 0 } in
    { area; position = zero }

  let move ~(move : pos) (state : state) : state =
    let pos_s = state.position in
    let new_pos =
      {
        line = pos_s.line + move.line;
        column = (pos_s.column + move.column) mod state.area.width;
      }
    in
    { state with position = new_pos }

  let is_done (state : state) : bool =
    state.position.line >= state.area.height - 1

  let is_on_tree state =
    try Area.is_tree_exn state.area state.position.line state.position.column
    with _ -> false
end

let encountered_trees_for_slope ~area slope =
  let state = Toboggan.make area in
  let rec loop encountered_trees (state : Toboggan.state) =
    let encountered_trees =
      if Toboggan.is_on_tree state then encountered_trees + 1
      else encountered_trees
    in
    if Toboggan.is_done state then encountered_trees
    else
      let next_state = Toboggan.move ~move:slope state in
      loop encountered_trees next_state
  in
  loop 0 state

let run input =
  let move = Toboggan.{ line = 1; column = 3 } in
  let area = Area.parse_file input in
  encountered_trees_for_slope ~area move

let () =
  let input = Sys.argv.(1) in
  let start = int_of_float (Sys.time () *. 1000.) in
  let result = run input in
  let end_ = int_of_float (Sys.time () *. 1000.) in
  Printf.printf "_duration:%d\n%d\n" (end_ - start) result
