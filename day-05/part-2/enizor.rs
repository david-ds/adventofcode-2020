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
    let mut plane = Plane::new();
    for bytes in input.as_bytes().split(|&c| c == b'\n') {
        let seat = Seat::from_str(bytes);
        plane.add_seat(seat);
    }
    plane.find_seat()
}

struct Seat {
    row: u8,
    col: u8,
}

impl Seat {
    fn id(&self) -> usize {
        8 * self.row as usize + self.col as usize
    }

    fn from_str(bytes: &[u8]) -> Self {
        debug_assert!(bytes.len() == 10);
        let mut row = 0;
        // let mut mask = 1 << 6;\
        for (i, &c) in bytes[..7].iter().enumerate() {
            // B = 0b01000010
            // F = 0b01000110
            row |= ((c ^ b'F') << 4) >> i;
        }
        let mut col = 0;
        for (i, &c) in bytes[7..10].iter().enumerate() {
            // R = 0b01010010
            // L = 0b01001100
            col |= ((c & 0b00000010) << 1) >> i;
        }
        Seat { row, col }
    }
}

const MAX_NB_ROW: u8 = 127;
struct Plane {
    min_row: u8,
    max_row: u8,
    seats: [u8; MAX_NB_ROW as usize],
}

impl Plane {
    fn new() -> Self {
        Self {
            min_row: MAX_NB_ROW,
            max_row: 0,
            seats: [0; MAX_NB_ROW as usize],
        }
    }

    fn add_seat(&mut self, seat: Seat) {
        let row = seat.row;
        self.min_row = self.min_row.min(row);
        self.max_row = self.max_row.max(row);
        self.seats[seat.row as usize] |= 1 << seat.col;
    }

    fn find_seat(&self) -> usize {
        self.seats[((self.min_row + 1) as usize)..self.max_row as usize]
            .iter()
            .enumerate()
            .map(|(row, &seats)| (self.min_row + 1 + row as u8, find_seat_in_row(seats)))
            .find(|&(_r, c)| c >= 0)
            .map(|(r, c)| {
                Seat {
                    row: r,
                    col: c as u8,
                }
                .id()
            })
            .expect("Cannot find available seat!")
    }
}

const LOG2: [i8; 255] = gen_log2();

const fn gen_log2() -> [i8; 255] {
    let mut pos = 0;
    let mut log2 = [0; 255];
    log2[0] = -1;
    while pos < 8 {
        log2[1 << pos] = pos;
        pos += 1;
    }
    log2
}

fn find_seat_in_row(seats: u8) -> i8 {
    LOG2[(!seats) as usize]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_test() {
        assert_eq!(Seat::from_str(b"FBFBBFFRLR").id(), 357);
        assert_eq!(Seat::from_str(b"BFFFBBFRRR").id(), 567);
        assert_eq!(Seat::from_str(b"FFFBBBFRRR").id(), 119);
        assert_eq!(Seat::from_str(b"BBFFBBFRLL").id(), 820);
    }
}
