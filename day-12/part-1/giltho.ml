type card = North | South | West | East

type dir = Card of card | Left | Right | Forward

type state = { facing : card; east : int; north : int }

let init_state = { facing = East; east = 0; north = 0 }

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

let parse input = input |> String.split_on_char '\n' |> List.map parse_one

let rec left fuel card =
  if fuel = 0 then card
  else
    left (fuel - 90)
      ( match card with
      | North -> West
      | West -> South
      | South -> East
      | East -> North )

let rec right fuel card =
  if fuel = 0 then card
  else
    right (fuel - 90)
      ( match card with
      | North -> East
      | East -> South
      | South -> West
      | West -> North )

let manhattan state = abs state.east + abs state.north

let rec step (state : state) (a : action) : state =
  match a with
  | Card North, i -> { state with north = state.north + i }
  | Card East, i -> { state with east = state.east + i }
  | Card South, i -> { state with north = state.north - i }
  | Card West, i -> { state with east = state.east - i }
  | Left, i -> { state with facing = left i state.facing }
  | Right, i -> { state with facing = right i state.facing }
  | Forward, i -> step state (Card state.facing, i)

let run input =
  let parsed = parse input in
  parsed |> List.fold_left step init_state |> manhattan

let () =
  let input = Sys.argv.(1) in
  let start = Sys.time () *. 1000. in
  let result = run input in
  let end_ = Sys.time () *. 1000. in
  Printf.printf "_duration:%f\n%d\n" (end_ -. start) result
