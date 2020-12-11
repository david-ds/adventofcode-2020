use std::cmp::{max, min};
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
    width: usize,
    height: usize,
    seats: Vec<usize>,
    occupied: usize,
}

impl Map {
    fn from(input: &str) -> Self {
        let tiles: Vec<u8> = input
            .lines()
            .flat_map(|line| line.as_bytes())
            .copied()
            .collect();

        let seats = tiles
            .iter()
            .enumerate()
            .filter(|(_, c)| **c == b'L')
            .map(|(i, _)| i)
            .collect();

        let width = input.lines().next().unwrap().len();
        let height = tiles.len() / width;

        Self {
            tiles,
            width,
            height,
            seats,
            occupied: 0,
        }
    }

    fn occupied_around(&self, idx: usize) -> usize {
        let mut count = 0;

        let c_min = max(idx as isize % self.width as isize - 1, 0) as usize;
        let c_max = min(idx % self.width + 1, self.width - 1) as usize;

        let l_min = max(idx as isize / self.width as isize - 1, 0) as usize;
        let l_max = min(idx / self.width + 1, self.height - 1) as usize;

        for j in c_min..=c_max {
            for i in l_min..=l_max {
                if self.tiles[i * self.width + j] == b'#' {
                    count += 1;
                }
            }
        }

        if self.tiles[idx] == b'#' {
            count -= 1;
        }

        count
    }
}

impl Iterator for Map {
    type Item = usize;

    fn next(&mut self) -> Option<usize> {
        let mut next_tiles = self.tiles.clone();
        let mut changes = 0;

        for &s in self.seats.iter() {
            if self.tiles[s] == b'L' {
                if self.occupied_around(s) == 0 {
                    next_tiles[s] = b'#';
                    self.occupied += 1;
                    changes += 1;
                }
            } else if self.tiles[s] == b'#' && self.occupied_around(s) >= 4 {
                next_tiles[s] = b'L';
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

        assert_eq!(run(input), 37)
    }
}
