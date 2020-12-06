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
    let map = Map::from(input);
    map.count_tiles(Tile::Tree, &Slope { x: 3, y: 1 })
}

#[derive(PartialEq, Clone, Copy)]
pub enum Tile {
    Tree,
    Square,
}

pub struct Slope {
    pub x: usize,
    pub y: usize,
}

pub struct Map {
    tiles: Vec<Vec<Tile>>,
}

impl Map {
    pub fn from(string: &str) -> Self {
        Self {
            tiles: string
                .lines()
                .map(|line| {
                    line.chars()
                        .map(|c| match c {
                            '#' => Tile::Tree,
                            _ => Tile::Square,
                        })
                        .collect()
                })
                .collect(),
        }
    }

    pub fn count_tiles(&self, tile: Tile, slope: &Slope) -> usize {
        let mut count = 0;
        let mut x = 0;
        let mut y = 0;

        while y + slope.y < self.tiles.len() {
            y += slope.y;
            x += slope.x;
            x %= self.tiles[y].len();

            if self.tiles[y][x] == tile {
                count += 1;
            }
        }

        count
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "..##.......\n#...#...#..\n.#....#..#.\n..#.#...#.#\n.#...##..#.\n..#.##.....\n.#.#.#....#\n.#........#\n#.##...#...\n#...##....#\n.#..#...#.#";
        assert_eq!(run(input), 7)
    }
}
