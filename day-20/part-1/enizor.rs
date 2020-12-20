use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut pos = 5;
    let bytes = input.as_bytes();
    let mut tiles = Vec::new();
    while pos < bytes.len() {
        let mut tile = Tile::from_str(bytes, &mut pos);
        reduce_sides(&mut tiles, &mut tile);
        tiles.push(tile);
        pos += 7;
    }
    let mut res = 1;
    for tile in &tiles {
        if tile.sides.iter().filter(|&&s| s != u16::MAX).count() == 2 {
            res *= tile.number;
        }
    }
    res
}
#[derive(PartialEq, Eq)]
struct Tile {
    number: usize,
    sides: [u16; 4],
}

impl Tile {
    fn from_str(input: &[u8], pos: &mut usize) -> Self {
        // let mut pos = 5;
        let mut number = 0;
        while *pos < input.len() {
            let c = input[*pos];
            if (b'0'..=b'9').contains(&c) {
                number *= 10;
                number += (c - b'0') as usize;
                *pos += 1;
            } else {
                break;
            }
        }
        let mut sides = [0; 4];
        *pos += 2;
        let mut line_length = 0;
        let mut line = 0;
        // Parse top line
        loop {
            if input[*pos] == b'\n' {
                sides[2] = sides[0] & 0b10;
                line += 1;
                break;
            } else if input[*pos] == b'#' {
                sides[0] += 1;
            }
            if line_length == 0 {
                sides[1] = sides[0];
                sides[1] <<= 1;
            }
            sides[0] <<= 1;
            line_length += 1;
            *pos += 1;
        }
        sides[0] <<= 2;
        *pos += 1;
        while line < line_length - 1 {
            if input[*pos] == b'#' {
                sides[1] += 1;
            }
            sides[1] <<= 1;
            if input[*pos + line_length - 1] == b'#' {
                sides[2] += 1;
            }
            sides[2] <<= 1;

            line += 1;
            *pos += line_length + 1;
        }
        // Parse last line
        let mut line_pos = 0;
        while *pos < input.len() {
            // dbg!(*pos);
            // dbg!(input[*pos]);
            if input[*pos] == b'\n' {
                break;
            }
            if input[*pos] == b'#' {
                sides[3] += 1;
            }
            sides[3] <<= 1;
            if line_pos == 0 {
                if input[*pos] == b'#' {
                    sides[1] += 1;
                }
                sides[1] <<= 1;
            }
            if line_pos == line_length - 1 {
                if input[*pos] == b'#' {
                    sides[2] += 1;
                }
                sides[2] <<= 1;
            }
            line_pos += 1;
            *pos += 1;
        }
        sides[1] <<= 2;
        sides[2] <<= 2;
        sides[3] <<= 2;
        Self { number, sides }
    }
}

impl std::fmt::Debug for Tile {
    fn fmt(&self, fmt: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        fmt.debug_struct("Tile")
            .field("number", &self.number)
            .field("side 1", &format!("{:b}", self.sides[0]))
            .field("side 2", &format!("{:b}", self.sides[1]))
            .field("side 3", &format!("{:b}", self.sides[2]))
            .field("side 4", &format!("{:b}", self.sides[3]))
            .finish()
    }
}

fn reduce_sides(tiles: &mut [Tile], new_tile: &mut Tile) {
    let mut sides_rev: Vec<u16> = new_tile.sides.iter().map(|&b| reverse(b)).collect();
    let mut count = 0;
    for tile in tiles.iter_mut() {
        for side in tile.sides.iter_mut() {
            if *side != u16::MAX {
                for (new_side, new_side_rev) in new_tile.sides.iter_mut().zip(sides_rev.iter_mut())
                {
                    if *new_side == *side || *new_side_rev == *side {
                        *side = u16::MAX;
                        *new_side = u16::MAX;
                        *new_side_rev = u16::MAX;
                        count += 1;
                        break;
                    }
                }
                if count == 4 {
                    return;
                }
            }
        }
    }
}

fn reverse(mut b: u16) -> u16 {
    let mut s = 16;
    let mut r = 0;
    while b > 0 {
        r <<= 1;
        r |= b & 1;
        s -= 1;
        b >>= 1;
    }
    r <<= s;
    r
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn reverse_test() {
        assert_eq!(reverse(0b1011010000), 0b0000101101000000)
    }

    #[test]
    fn parse_test() {
        let tile = r#"Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
#.###..###
"#;
        assert_eq!(
            Tile::from_str(tile.as_bytes(), &mut 5),
            Tile {
                number: 2311,
                sides: [0b11010010000, 0b111110011000, 0b1011001000, 0b1011100111000,]
            }
        )
    }

    #[test]
    fn run_test() {
        let tiles = r#"Tile 2311:
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
..#.###..."#;
        assert_eq!(run(tiles), 20899048083289)
    }
}
