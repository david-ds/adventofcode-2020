use std::time::Instant;
use std::{env::args, str::FromStr};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut plane = Plane::new();
    for line in input.lines() {
        let seat = line.parse::<Seat>().expect("cannot parse");
        plane.add_seat(seat);
    }
    plane.find_seat()
}

struct Seat {
    row: usize,
    col: usize,
}

impl Seat {
    fn id(&self) -> usize {
        8 * self.row + self.col
    }
}

impl FromStr for Seat {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        debug_assert!(s.len() == 10);
        let bytes = s.as_bytes();
        let mut row = 0;
        let mut mask = 1 << 6;
        for &c in &bytes[..7] {
            match c {
                b'B' => row |= mask,
                b'F' => {}
                _ => return Err(()),
            }
            mask >>= 1;
        }
        let mut col = 0;
        let mut mask = 1 << 2;
        for &c in &bytes[7..10] {
            match c {
                b'R' => col |= mask,
                b'L' => {}
                _ => return Err(()),
            }
            mask >>= 1;
        }
        Ok(Seat { row, col })
    }
}

const MAX_NB_ROW: usize = 127;
struct Plane {
    min_row: usize,
    max_row: usize,
    seats: [u8; MAX_NB_ROW],
}

impl Plane {
    fn new() -> Self {
        Self {
            min_row: MAX_NB_ROW,
            max_row: 0,
            seats: [0; MAX_NB_ROW],
        }
    }

    fn add_seat(&mut self, seat: Seat) {
        let row = seat.row;
        self.min_row = self.min_row.min(row);
        self.max_row = self.max_row.max(row);
        self.seats[seat.row] |= 1 << seat.col;
    }

    fn find_seat(&self) -> usize {
        self.seats[(self.min_row + 1)..self.max_row]
            .iter()
            .enumerate()
            .find_map(|(row, &seats)| {
                find_seat_in_row(seats).map(|col| {
                    Seat {
                        row: self.min_row + 1 + row,
                        col,
                    }
                    .id()
                })
            })
            .expect("Cannot find available seat!")
    }
}

const LOG2: [usize; 255] = gen_log2();

const fn gen_log2() -> [usize; 255] {
    let mut pos = 0;
    let mut log2 = [0; 255];
    while pos < 8 {
        log2[1 << pos] = pos;
        pos += 1;
    }
    log2
}

fn find_seat_in_row(seats: u8) -> Option<usize> {
    if seats != !0 {
        Some(LOG2[(!seats) as usize])
    } else {
        None
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_test() -> Result<(), ()> {
        assert_eq!("FBFBBFFRLR".parse::<Seat>()?.id(), 357);
        assert_eq!("BFFFBBFRRR".parse::<Seat>()?.id(), 567);
        assert_eq!("FFFBBBFRRR".parse::<Seat>()?.id(), 119);
        assert_eq!("BBFFBBFRLL".parse::<Seat>()?.id(), 820);

        Ok(())
    }
}
