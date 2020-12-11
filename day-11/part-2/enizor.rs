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
    let mut grid = Grid::init(input);
    loop {
        match grid.round() {
            (_, false) => return grid.count_ocuppied(),
            (g, true) => grid = g,
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
            let new_width = line.len();
            if let Some(w) = width {
                assert_eq!(w, new_width);
            } else {
                width = Some(new_width);
            }
            width = match width {
                None => Some(new_width),
                Some(w) if w != new_width => panic!(),
                _ => width,
            };
            for c in line.as_bytes() {
                seats.push(Seat::from_str(*c));
            }
        }

        Self {
            width: width.unwrap(),
            length: seats.len() / width.unwrap(),
            seats,
        }
    }

    fn round(&self) -> (Grid, bool) {
        let mut grid = self.clone();
        let mut updated = false;
        for x in 0..self.width {
            for y in 0..self.length {
                if grid
                    .index_mut(x as isize, y as isize)
                    .unwrap()
                    .update(self.iter(x, y))
                {
                    updated = true;
                }
            }
        }
        (grid, updated)
    }

    fn count_ocuppied(&self) -> usize {
        self.seats.iter().filter(|&&s| s == Seat::Occupied).count()
    }

    fn iter(&self, x: usize, y: usize) -> AdjacentSeats<'_> {
        AdjacentSeats {
            x_center: x as isize,
            y_center: y as isize,
            x_direction: -1,
            y_direction: -1,
            grid: &self,
        }
    }

    fn index(&self, x: isize, y: isize) -> Option<&Seat> {
        if x < 0 || x >= self.width as isize || y < 0 || y >= self.length as isize {
            None
        } else {
            Some(&self.seats[x as usize + (y as usize) * self.width])
        }
    }

    fn index_mut(&mut self, x: isize, y: isize) -> Option<&mut Seat> {
        if x < 0 || x >= self.width as isize || y < 0 || y >= self.length as isize {
            None
        } else {
            Some(&mut self.seats[x as usize + (y as usize) * self.width])
        }
    }

    #[allow(dead_code)]
    fn pretty_print(&self) -> String {
        let mut out = String::new();
        for y in 0..self.length {
            for x in 0..self.width {
                out.push(self.index(x as isize, y as isize).unwrap().to_string());
            }
            out.push('\n');
        }
        out
    }
}

struct AdjacentSeats<'a> {
    x_center: isize,
    y_center: isize,
    x_direction: isize,
    y_direction: isize,
    grid: &'a Grid,
}

impl<'a> Iterator for AdjacentSeats<'a> {
    type Item = &'a Seat;

    fn next(&mut self) -> Option<Self::Item> {
        if self.y_direction < 2 {
            let mut out = Some(&Seat::Floor);
            let mut mul = 1;
            while out == Some(&Seat::Floor) {
                out = self.grid.index(
                    self.x_center + mul * self.x_direction,
                    self.y_center + mul * self.y_direction,
                );
                mul += 1;
            }
            let (x, y) = match (self.x_direction, self.y_direction) {
                (1, y) => (-1, y + 1),
                (-1, 0) => (1, 0),
                (x, y) => (x + 1, y),
            };
            self.x_direction = x;
            self.y_direction = y;
            out.or(Some(&Seat::Floor))
        } else {
            None
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        (8, Some(8))
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

    fn update<'a, T: Iterator<Item = &'a Seat>>(&mut self, mut adjacent: T) -> bool {
        let new = match self {
            Self::Floor => (Self::Floor, false),
            Self::Empty => {
                if adjacent.any(|&s| s == Self::Occupied) {
                    (Self::Empty, false)
                } else {
                    (Self::Occupied, true)
                }
            }
            Self::Occupied => {
                if adjacent.filter(|&&s| s == Self::Occupied).count() >= 5 {
                    (Self::Empty, true)
                } else {
                    (Self::Occupied, false)
                }
            }
        };
        *self = new.0;
        new.1
    }

    fn to_string(&self) -> char {
        match self {
            Seat::Floor => '.',
            Seat::Empty => 'L',
            Seat::Occupied => '#',
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn update_test() {
        let line = ".............
.L.L.#.#.#.#.
.............";
        let mut grid = Grid::init(line);
        let g2 = grid.clone();
        grid.index_mut(1, 1).unwrap().update(g2.iter(1, 1));
        assert_eq!(grid.index(1, 1), Some(&Seat::Occupied));

        let line = ".##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.";
        grid = Grid::init(line);
        let g2 = grid.clone();
        grid.index_mut(3, 3).unwrap().update(g2.iter(3, 3));
        assert_eq!(grid.index(3, 3), Some(&Seat::Occupied));
    }

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
        assert_eq!(run(small_example), 26)
    }
}
