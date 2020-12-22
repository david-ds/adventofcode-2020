use std::cmp::{max, min};
use std::collections::HashMap;
use std::env::args;
use std::mem::swap;
use std::time::Instant;

fn is_hash(c: u8) -> u16 {
    match c as char {
        '#' => 1,
        '.' => 0,
        _ => panic!("Invalid char: {}", c),
    }
}

fn rev_u10(b: u16) -> u16 {
    let mut res = ((b & 31) << 5) | ((b & 992) >> 5);
    let fix = res & 132;
    res = (res & 792) >> 3 | (res & 99) << 3;
    (res & 594) >> 1 | (res & 297) << 1 | fix
}

#[derive(Debug)]
struct Tile {
    id: u16,
    top: u16,
    right: u16,
    bottom: u16,
    left: u16,
}

impl Tile {
    fn parse(text: &[u8]) -> Self {
        let mut id = 0;
        for j in &text[5..9] {
            id = id * 10 + (*j as char).to_digit(10).unwrap()
        }
        let mut top = 0;
        let mut left = 0;
        let mut right = 0;
        let mut bottom = 0;
        for i in 0..10 {
            top = (top << 1) + is_hash(text[11 + i]);
            left = (left << 1) + is_hash(text[11 * (i + 1)]);
            right = (right << 1) + is_hash(text[11 * (i + 1) + 9]);
            bottom = (bottom << 1) + is_hash(text[110 + i]);
        }
        Self {
            id: id as u16,
            top,
            left,
            right,
            bottom,
        }
    }
}

#[derive(Clone, Copy, Debug)]
enum Direction {
    Up,
    Right,
    Down,
    Left,
}

const ALL_DIRECTIONS: [Direction; 4] = [
    Direction::Up,
    Direction::Down,
    Direction::Left,
    Direction::Right,
];

impl Direction {
    fn flip_horizontally(self) -> Self {
        match self {
            Self::Up => Self::Up,
            Self::Down => Self::Down,
            Self::Left => Self::Right,
            Self::Right => Self::Left,
        }
    }

    fn flip_vertically(self) -> Self {
        match self {
            Self::Up => Self::Down,
            Self::Down => Self::Up,
            Self::Left => Self::Left,
            Self::Right => Self::Right,
        }
    }
}

fn right_of(tile: &Tile, dir: Direction, flipped: bool) -> u16 {
    if !flipped {
        match dir {
            Direction::Up => tile.right,
            Direction::Right => tile.top,
            Direction::Down => rev_u10(tile.left),
            Direction::Left => rev_u10(tile.bottom),
        }
    } else {
        left_of(tile, dir.flip_horizontally(), false)
    }
}

fn left_of(tile: &Tile, dir: Direction, flipped: bool) -> u16 {
    if !flipped {
        match dir {
            Direction::Up => tile.left,
            Direction::Right => tile.bottom,
            Direction::Down => rev_u10(tile.right),
            Direction::Left => rev_u10(tile.top),
        }
    } else {
        right_of(tile, dir.flip_horizontally(), false)
    }
}

fn top_of(tile: &Tile, dir: Direction, flipped: bool) -> u16 {
    if !flipped {
        match dir {
            Direction::Up => tile.top,
            Direction::Right => rev_u10(tile.left),
            Direction::Left => tile.right,
            Direction::Down => rev_u10(tile.bottom),
        }
    } else {
        bottom_of(tile, dir.flip_vertically(), false)
    }
}

fn bottom_of(tile: &Tile, dir: Direction, flipped: bool) -> u16 {
    if !flipped {
        match dir {
            Direction::Up => tile.bottom,
            Direction::Right => rev_u10(tile.right),
            Direction::Left => tile.left,
            Direction::Down => rev_u10(tile.top),
        }
    } else {
        top_of(tile, dir.flip_vertically(), false)
    }
}

#[derive(Debug)]
struct LaidTile {
    dir: Direction,
    flipped: bool,
    tile: Tile,
}

impl LaidTile {
    fn new(tile: Tile, dir: Direction, flipped: bool) -> Self {
        Self { tile, dir, flipped }
    }

    fn right(&self) -> u16 {
        right_of(&self.tile, self.dir, self.flipped)
    }

    fn left(&self) -> u16 {
        left_of(&self.tile, self.dir, self.flipped)
    }

    fn top(&self) -> u16 {
        top_of(&self.tile, self.dir, self.flipped)
    }

    fn bottom(&self) -> u16 {
        bottom_of(&self.tile, self.dir, self.flipped)
    }

    fn lay_on_right(&self, tile: &Tile) -> Option<(Direction, bool)> {
        for &flipped in [true, false].iter() {
            for &dir in ALL_DIRECTIONS.iter() {
                if left_of(&tile, dir, flipped) == self.right() {
                    return Some((dir, flipped));
                }
            }
        }
        None
    }

    fn lay_above(&self, tile: &Tile) -> Option<(Direction, bool)> {
        for &flipped in [true, false].iter() {
            for &dir in ALL_DIRECTIONS.iter() {
                if bottom_of(tile, dir, flipped) == self.top() {
                    return Some((dir, flipped));
                }
            }
        }
        None
    }

    fn lay_under(&self, tile: &Tile) -> Option<(Direction, bool)> {
        for &flipped in [true, false].iter() {
            for &dir in ALL_DIRECTIONS.iter() {
                if top_of(tile, dir, flipped) == self.bottom() {
                    return Some((dir, flipped));
                }
            }
        }
        None
    }

    fn lay_on_left(&self, tile: &Tile) -> Option<(Direction, bool)> {
        for &flipped in [true, false].iter() {
            for &dir in ALL_DIRECTIONS.iter() {
                if right_of(tile, dir, flipped) == self.left() {
                    return Some((dir, flipped));
                }
            }
        }
        None
    }
}

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

#[derive(Debug)]
struct Board {
    board: HashMap<(i8, i8), LaidTile>,
}

impl Board {
    fn new() -> Self {
        Self {
            board: HashMap::with_capacity(150),
        }
    }

    fn insert(&mut self, x: i8, y: i8, tile: Tile, dir: Direction, flipped: bool) {
        self.board.insert((x, y), LaidTile::new(tile, dir, flipped));
    }

    fn add_tiles(&mut self, data: &mut Vec<Tile>) -> (i8, i8, i8, i8) {
        let mut data = data;
        let mut secondary = &mut Vec::with_capacity(150);
        let mut maxy = 0;
        let mut miny = 0;
        let mut maxx = 0;
        let mut minx = 0;
        while !data.is_empty() {
            'tile_loop: for tile in data.drain(..) {
                for (&(x, y), laid_tile) in self.board.iter() {
                    if !self.board.contains_key(&(x, y + 1)) {
                        if let Some((dir, flipped)) = laid_tile.lay_on_right(&tile) {
                            self.insert(x, y + 1, tile, dir, flipped);
                            maxy = max(maxy, y + 1);
                            continue 'tile_loop;
                        }
                    }
                    if !self.board.contains_key(&(x, y - 1)) {
                        if let Some((dir, flipped)) = laid_tile.lay_on_left(&tile) {
                            self.insert(x, y - 1, tile, dir, flipped);
                            miny = min(miny, y - 1);
                            continue 'tile_loop;
                        }
                    }
                    if !self.board.contains_key(&(x - 1, y)) {
                        if let Some((dir, flipped)) = laid_tile.lay_above(&tile) {
                            self.insert(x - 1, y, tile, dir, flipped);
                            minx = min(minx, x - 1);
                            continue 'tile_loop;
                        }
                    }
                    if !self.board.contains_key(&(x + 1, y)) {
                        if let Some((dir, flipped)) = laid_tile.lay_under(&tile) {
                            self.insert(x + 1, y, tile, dir, flipped);
                            maxx = max(maxx, x + 1);
                            continue 'tile_loop;
                        }
                    }
                }
                secondary.push(tile);
            }
            swap(&mut data, &mut secondary);
        }
        (minx, miny, maxx, maxy)
    }

    fn get_id(&self, x: i8, y: i8) -> u16 {
        self.board.get(&(x, y)).unwrap().tile.id
    }
}

fn run(input: &str) -> u64 {
    let raw_data = input.as_bytes();
    let mut data = Vec::with_capacity(150);
    for i in 0..((raw_data.len() + 2) / 122) {
        data.push(Tile::parse(&raw_data[122 * i..]))
    }

    let mut board = Board::new();
    board.insert(0, 0, data.pop().unwrap(), Direction::Up, false);
    let (minx, miny, maxx, maxy) = board.add_tiles(&mut data);
    (board.get_id(minx, miny) as u64)
        * (board.get_id(minx, maxy) as u64)
        * (board.get_id(maxx, miny) as u64)
        * (board.get_id(maxx, maxy) as u64)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run(r#"Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
"#),
            20899048083289
        )
    }
}
