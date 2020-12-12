type card = North | South | West | East

type waypoint = { weast : int; wnorth : int }

type dir = Card of card | Left | Right | Forward

type state = { waypoint : waypoint; east : int; north : int }

let init_state =
  let waypoint = { weast = 10; wnorth = 1 } in
  { waypoint; east = 0; north = 0 }

type action = dir * int

let parse_one s =
  let dir =
    match s.[0] with
    | 'N' -> Card North
    | 'S' -> Card South
    | 'E' -> Card East
    | 'W' -> Card West
    | 'L' -> Left
    | 'R' -> Right
    | 'F' -> Forward
    | _ -> failwith "unkown dir"
  in
  (dir, int_of_string (String.sub s 1 (String.length s - 1)))

let rec left fuel (waypoint : waypoint) : waypoint =
  if fuel = 0 then waypoint
  else left (fuel - 90) { weast = -waypoint.wnorth; wnorth = waypoint.weast }

let rec right fuel waypoint =
  if fuel = 0 then waypoint
  else right (fuel - 90) { wnorth = -waypoint.weast; weast = waypoint.wnorth }

let parse input = input |> String.split_on_char '\n' |> List.map parse_one

let manhattan state = abs state.east + abs state.north

let move_waypoint card i waypoint =
  match card with
  | North -> { waypoint with wnorth = waypoint.wnorth + i }
  | South -> { waypoint with wnorth = waypoint.wnorth - i }
  | East -> { waypoint with weast = waypoint.weast + i }
  | West -> { waypoint with weast = waypoint.weast - i }

let step (state : state) (a : action) : state =
  match a with
  | Card card, i ->
      { state with waypoint = move_waypoint card i state.waypoint }
  | Left, i -> { state with waypoint = left i state.waypoint }
  | Right, i -> { state with waypoint = right i state.waypoint }
  | Forward, i ->
      {
        state with
        east = state.east + (i * state.waypoint.weast);
        north = state.north + (i * state.waypoint.wnorth);
      }

let fold_lines ~init ~f =
  let rec loop ac =
    try loop (f ac (input_line stdin)) with End_of_file -> ac
  in
  loop init

let run () =
  fold_lines ~init:init_state ~f:(fun state line -> step state (parse_one line))
  |> manhattan

let () =
  let start = Sys.time () *. 1000. in
  let result = run () in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
