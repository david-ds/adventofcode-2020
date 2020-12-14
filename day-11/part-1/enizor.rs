use std::time::Instant;
use std::{
    env::args,
    ops::{Index, IndexMut},
};

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
    loop {
        if !grid.round(&mut grid2) {
            return grid2.count_ocuppied();
        }
        if !grid2.round(&mut grid) {
            return grid.count_ocuppied();
        }
    }
}
#[derive(Debug, Clone)]
struct Grid {
    width: usize,
    length: usize,
    seats: Vec<Seat>,
}

impl Grid {
    fn init(input: &str) -> Self {
        let mut seats = Vec::new();
        let mut width = None;
        for line in input.lines() {
            seats.push(Seat::Floor);
            let new_width = line.len();
            if let Some(w) = width {
                assert_eq!(w, new_width);
            } else {
                width = Some(new_width);
                seats.append(&mut vec![Seat::Floor; new_width + 2])
            }
            width = match width {
                None => Some(new_width),
                Some(w) if w != new_width => panic!(),
                _ => width,
            };
            for c in line.as_bytes() {
                seats.push(Seat::from_str(*c));
            }
            seats.push(Seat::Floor);
        }

        seats.append(&mut vec![Seat::Floor; width.unwrap() + 2]);
        Self {
            width: width.unwrap() + 2,
            length: seats.len() / (width.unwrap() + 2),
            seats,
        }
    }

    fn round(&self, other: &mut Grid) -> bool {
        let mut updated = false;
        for x in 1..self.width {
            for y in 1..self.length {
                if other[(x, y)].update(self.iter(x, y)) {
                    updated = true;
                }
            }
        }
        updated
    }

    fn count_ocuppied(&self) -> usize {
        self.seats.iter().filter(|&&s| s == Seat::Occupied).count()
    }

    fn iter(&self, x: usize, y: usize) -> AdjacentSeats<'_> {
        AdjacentSeats {
            x_center: x as isize,
            y_center: y as isize,
            x_diff: -1,
            y_diff: -1,
            grid: &self,
        }
    }
}

struct AdjacentSeats<'a> {
    x_center: isize,
    y_center: isize,
    x_diff: isize,
    y_diff: isize,
    grid: &'a Grid,
}

impl<'a> AdjacentSeats<'a> {
    fn get_center(&self) -> &'a Seat {
        &self.grid[(self.x_center as usize, self.y_center as usize)]
    }
}

impl<'a> Iterator for AdjacentSeats<'a> {
    type Item = &'a Seat;

    fn next(&mut self) -> Option<Self::Item> {
        if self.y_diff < 2 {
            let out = &self.grid[(
                (self.x_center + self.x_diff) as usize,
                (self.y_center + self.y_diff) as usize,
            )];
            let (x, y) = match (self.x_diff, self.y_diff) {
                (1, y) => (-1, y + 1),
                (-1, 0) => (1, 0),
                (x, y) => (x + 1, y),
            };
            self.x_diff = x;
            self.y_diff = y;
            Some(out)
        } else {
            None
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        (8, Some(8))
    }
}

impl Index<(usize, usize)> for Grid {
    type Output = Seat;

    fn index(&self, index: (usize, usize)) -> &Self::Output {
        if index.0 >= self.width {
            panic!("The width is {} but the index is {:?}", self.width, &index);
        }
        if index.1 >= self.length {
            panic!(
                "The length is {} but the index is {:?}",
                self.length, &index
            );
        }
        &self.seats[index.0 + index.1 * self.width]
    }
}

impl IndexMut<(usize, usize)> for Grid {
    fn index_mut(&mut self, index: (usize, usize)) -> &mut Self::Output {
        &mut self.seats[index.0 + index.1 * self.width]
    }
}

#[derive(Debug, Copy, Clone, Eq, PartialEq)]
enum Seat {
    Floor,
    Empty,
    Occupied,
}

impl Seat {
    fn from_str(input: u8) -> Self {
        match input {
            b'.' => Self::Floor,
            b'L' => Self::Empty,
            b'#' => Self::Occupied,
            _ => panic!(),
        }
    }

    fn update(&mut self, mut adjacent: AdjacentSeats) -> bool {
        let new = match adjacent.get_center() {
            Self::Floor => (Self::Floor, false),
            Self::Empty => {
                if adjacent.any(|&s| s == Self::Occupied) {
                    (Self::Empty, false)
                } else {
                    (Self::Occupied, true)
                }
            }
            Self::Occupied => {
                if adjacent.filter(|&&s| s == Self::Occupied).count() >= 4 {
                    (Self::Empty, true)
                } else {
                    (Self::Occupied, false)
                }
            }
        };
        *self = new.0;
        new.1
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_example = r#"L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"#;
        assert_eq!(run(small_example), 37)
    }
}
