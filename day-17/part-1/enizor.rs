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
    let mut grid2 = grid.clone();
    let mut round = 0;
    loop {
        round += 1;
        let count = grid.round(&mut grid2, round, round == ROUNDS);
        if round == ROUNDS {
            return count;
        }
        round += 1;
        let count = grid2.round(&mut grid, round, round == ROUNDS);
        if round == ROUNDS {
            return count;
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
        let mut cubes = Vec::with_capacity(width * width * height);
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

    fn round(&self, other: &mut Grid, nb: usize, should_count: bool) -> usize {
        let mut count = 0;
        for z in 0..=nb {
            for y in (1 + ROUNDS - nb)..(self.length - 1 - ROUNDS + nb) {
                for x in (1 + ROUNDS - nb)..(self.width - 1 - ROUNDS + nb) {
                    other[(x as isize, y as isize, z as isize)]
                        .update(&self, (x as isize, y as isize, z as isize));
                    if should_count && other[(x as isize, y as isize, z as isize)] == Cube::Active {
                        if z == 0 {
                            count += 1;
                        } else {
                            count += 2;
                        };
                    }
                }
            }
        }
        count
    }

    #[allow(dead_code)]
    fn pretty_print(&self, height: usize) {
        for z in 0..=height {
            println!("z={}", z);
            for y in 0..self.length {
                let mut s = String::with_capacity(self.width);
                for x in 0..self.width {
                    s.push(self[(x as isize, y as isize, z as isize)].to_str())
                }
                println!("{}", s);
            }
            println!();
        }
    }
}

impl Index<(isize, isize, isize)> for Grid {
    type Output = Cube;

    fn index(&self, index: (isize, isize, isize)) -> &Self::Output {
        let x: usize = index.0 as usize;
        let y: usize = index.1 as usize;
        let z: usize = index.2.abs() as usize;
        if x >= self.width {
            panic!("The width is {} but the index is {:?}", self.width, &index);
        }
        if y >= self.length {
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
        &self.cubes[x + y * self.width + z * self.width * self.length]
    }
}

impl IndexMut<(isize, isize, isize)> for Grid {
    fn index_mut(&mut self, index: (isize, isize, isize)) -> &mut Self::Output {
        &mut self.cubes[index.0 as usize
            + (index.1 as usize) * self.width
            + (index.2.abs() as usize) * self.width * self.length]
    }
}

const NEIGHBORS: [(isize, isize, isize); 26] = generate_neighbors();

const fn generate_neighbors() -> [(isize, isize, isize); 26] {
    let mut out = [(0, 0, 0); 26];
    let mut z: isize = -1;
    while z < 2 {
        let mut y: isize = -1;
        while y < 2 {
            let mut x: isize = -1;
            while x < 2 {
                if x != 0 || y != 0 || z != 0 {
                    let mut pos = ((x + 1) + (y + 1) * 3 + (z + 1) * 9) as usize;
                    if pos >= 13 {
                        pos -= 1;
                    }
                    out[pos] = (x, y, z);
                }
                x += 1;
            }
            y += 1;
        }
        z += 1;
    }
    out
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

    fn update(&mut self, grid: &Grid, coords: (isize, isize, isize)) {
        let goal = 3;
        let mut count = 0;
        for (x, y, z) in &NEIGHBORS {
            if grid[(x + coords.0, y + coords.1, z + coords.2)] == Self::Active {
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
