use std::time::Instant;
use std::{
    env::args,
    ops::{Index, IndexMut},
};

const ROUNDS: usize = 6;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut grid = Grid::init(input);
    // grid.pretty_print(0);
    let mut grid2 = grid.clone();
    let mut round = 0;
    loop {
        round += 1;
        grid.round(&mut grid2, round);
        // println!("Round {}", round);
        // grid2.pretty_print(round);
        if round == ROUNDS {
            return grid2.count_active();
        }
        round += 1;
        grid2.round(&mut grid, round);
        // println!("Round {}", round);
        // grid.pretty_print(round);
        if round == ROUNDS {
            return grid.count_active();
        }
    }
}
#[derive(Debug, Clone)]
struct Grid {
    width: usize,
    length: usize,
    height: usize,
    cubes: Vec<Cube>,
}

impl Grid {
    fn init(input: &str) -> Self {
        // measurements
        let width: usize = input.find('\n').unwrap() + (ROUNDS * 2) + 2;
        let height: usize = ROUNDS + 2;
        let mut cubes = Vec::with_capacity(width * width * width);
        let mut length = ROUNDS * 2 + 2;
        cubes.append(&mut vec![Cube::Inactive; width * (ROUNDS + 1)]);
        for line in input.lines() {
            length += 1;
            cubes.append(&mut vec![Cube::Inactive; ROUNDS + 1]);
            let new_width: usize = line.len() + (ROUNDS * 2) + 2;
            assert_eq!(width, new_width);
            for c in line.as_bytes() {
                cubes.push(Cube::from_str(*c));
            }
            cubes.append(&mut vec![Cube::Inactive; ROUNDS + 1]);
        }
        cubes.append(&mut vec![Cube::Inactive; width * (ROUNDS + 1)]);
        // Insert empty levels
        cubes.append(&mut vec![Cube::Inactive; (ROUNDS + 1) * width * length]);

        Self {
            width,
            length,
            height,
            cubes,
        }
    }

    fn round(&self, other: &mut Grid, nb: usize) {
        for z in 0..=nb {
            for y in (1 + ROUNDS - nb)..(self.length - 1) {
                for x in (1 + ROUNDS - nb)..(self.width - 1) {
                    other[(x, y, z as isize)].update(self.iter(x, y, z), &self);
                }
            }
        }
    }

    fn count_active(&self) -> usize {
        let mut count = 0;
        for (i, &c) in self.cubes.iter().enumerate() {
            if c == Cube::Active {
                if i < self.width * self.length {
                    count += 1;
                } else {
                    count += 2;
                }
            }
        }
        count
    }

    fn iter(&self, x: usize, y: usize, z: usize) -> AdjacentSeats {
        AdjacentSeats {
            x_center: x as isize,
            y_center: y as isize,
            z_center: z as isize,
            x_diff: -1,
            y_diff: -1,
            z_diff: -1,
        }
    }

    #[allow(dead_code)]
    fn pretty_print(&self, height: usize) {
        for z in 0..=height {
            println!("z={}", z);
            for y in 0..self.length {
                let mut s = String::with_capacity(self.width);
                for x in 0..self.width {
                    s.push(self[(x, y, z as isize)].to_str())
                }
                println!("{}", s);
            }
            println!();
        }
    }
}

impl Index<(usize, usize, isize)> for Grid {
    type Output = Cube;

    fn index(&self, index: (usize, usize, isize)) -> &Self::Output {
        let z: usize = index.2.abs() as usize;
        if index.0 >= self.width {
            panic!("The width is {} but the index is {:?}", self.width, &index);
        }
        if index.1 >= self.length {
            panic!(
                "The length is {} but the index is {:?}",
                self.length, &index
            );
        }
        if z >= self.height {
            panic!(
                "The height is {} but the index is {:?}",
                self.height, &index
            );
        }
        &self.cubes[index.0 + index.1 * self.width + z * self.width * self.length]
    }
}

impl IndexMut<(usize, usize, isize)> for Grid {
    fn index_mut(&mut self, index: (usize, usize, isize)) -> &mut Self::Output {
        &mut self.cubes
            [index.0 + index.1 * self.width + (index.2.abs() as usize) * self.width * self.length]
    }
}

struct AdjacentSeats {
    x_center: isize,
    y_center: isize,
    z_center: isize,
    x_diff: isize,
    y_diff: isize,
    z_diff: isize,
}

impl AdjacentSeats {
    fn get_center(&self) -> (usize, usize, isize) {
        (
            self.x_center as usize,
            self.y_center as usize,
            self.z_center,
        )
    }
}

impl Iterator for AdjacentSeats {
    type Item = (usize, usize, isize);

    fn next(&mut self) -> Option<Self::Item> {
        if self.z_diff < 2 {
            // println!("{} {} {} / {} {} {}", self.x_center, self.y_center, self.z_center, self.x_diff, self.y_diff, self.z_diff);
            let out = (
                (self.x_center + self.x_diff) as usize,
                (self.y_center + self.y_diff) as usize,
                (self.z_center + self.z_diff),
            );
            let (x, y, z) = match (self.x_diff, self.y_diff, self.z_diff) {
                (1, 1, z) => (-1, -1, z + 1),
                (1, y, z) => (-1, y + 1, z),
                (-1, 0, 0) => (1, 0, 0),
                (x, y, z) => (x + 1, y, z),
            };
            self.x_diff = x;
            self.y_diff = y;
            self.z_diff = z;
            Some(out)
        } else {
            None
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        (26, Some(26))
    }
}

#[derive(Debug, Copy, Clone, Eq, PartialEq)]
enum Cube {
    Active = b'#' as isize,
    Inactive = b'.' as isize,
}

impl Cube {
    fn from_str(input: u8) -> Self {
        match input {
            b'.' => Self::Inactive,
            b'#' => Self::Active,
            _ => panic!(),
        }
    }

    fn to_str(&self) -> char {
        match self {
            Self::Inactive => '.',
            Self::Active => '#',
        }
    }

    fn update(&mut self, adjacent: AdjacentSeats, grid: &Grid) {
        let coords = adjacent.get_center();
        let goal = 3;
        let mut count = 0;
        for (x, y, z) in adjacent {
            if grid[(x, y, z)] == Self::Active {
                count += 1;
            }
            if count > goal {
                *self = Self::Inactive;
                return;
            }
        }
        *self = match grid[coords] {
            Self::Inactive => {
                if count == 3 {
                    Self::Active
                } else {
                    Self::Inactive
                }
            }
            Self::Active => {
                if count == 3 || count == 2 {
                    Self::Active
                } else {
                    Self::Inactive
                }
            }
        };
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_example = r#".#.
..#
###"#;
        assert_eq!(run(small_example), 112)
    }
}