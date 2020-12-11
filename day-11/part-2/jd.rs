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
    Map::from(input).last().unwrap_or(0)
}

struct Map {
    tiles: Vec<u8>,
    seats: Vec<(usize, [Option<usize>; 8])>,
    occupied: usize,
}

impl Map {
    fn from(input: &str) -> Self {
        let tiles: Vec<u8> = input
            .lines()
            .flat_map(|line| line.as_bytes())
            .copied()
            .collect();

        let width = input.lines().next().unwrap().len();
        let height = tiles.len() / width;

        let seats = tiles
            .iter()
            .enumerate()
            .filter(|(_, c)| **c == b'L')
            .map(|(idx, _)| {
                (
                    idx,
                    [
                        Self::build_sight(idx, (width, height), &tiles, (1, 0)),
                        Self::build_sight(idx, (width, height), &tiles, (1, 1)),
                        Self::build_sight(idx, (width, height), &tiles, (0, 1)),
                        Self::build_sight(idx, (width, height), &tiles, (-1, 1)),
                        Self::build_sight(idx, (width, height), &tiles, (-1, 0)),
                        Self::build_sight(idx, (width, height), &tiles, (-1, -1)),
                        Self::build_sight(idx, (width, height), &tiles, (0, -1)),
                        Self::build_sight(idx, (width, height), &tiles, (1, -1)),
                    ],
                )
            })
            .collect();

        Self {
            tiles,
            seats,
            occupied: 0,
        }
    }

    fn build_sight(
        idx: usize,
        dims: (usize, usize),
        tiles: &[u8],
        slope: (isize, isize),
    ) -> Option<usize> {
        let mut x: isize = idx as isize % dims.0 as isize + slope.0;
        let mut y: isize = idx as isize / dims.0 as isize + slope.1;

        while x >= 0 && x < dims.0 as isize && y >= 0 && y < dims.1 as isize {
            let i = y as usize * dims.0 + x as usize;

            if tiles[i] == b'L' {
                return Some(i);
            }

            x += slope.0;
            y += slope.1;
        }

        None
    }

    fn in_sights(&self, seat_idx: usize) -> usize {
        self.seats[seat_idx].1.iter().fold(0, |acc, sight| {
            acc + match sight {
                Some(idx) => (self.tiles[*idx] == b'#') as usize,
                None => 0,
            }
        })
    }
}

impl Iterator for Map {
    type Item = usize;

    fn next(&mut self) -> Option<usize> {
        let mut next_tiles = self.tiles.clone();
        let mut changes = 0;

        for (idx, (s, _)) in self.seats.iter().enumerate() {
            if self.tiles[*s] == b'L' {
                if self.in_sights(idx) == 0 {
                    next_tiles[*s] = b'#';
                    self.occupied += 1;
                    changes += 1;
                }
            } else if self.tiles[*s] == b'#' && self.in_sights(idx) >= 5 {
                next_tiles[*s] = b'L';
                self.occupied -= 1;
                changes += 1;
            }
        }

        if changes == 0 {
            None
        } else {
            self.tiles = next_tiles;
            Some(self.occupied)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL";

        assert_eq!(run(input), 26)
    }
}
