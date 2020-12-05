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
    input
        .as_bytes()
        .split(|&c| c == b'\n')
        .map(|s| Seat::from_str(s).id())
        .max()
        .expect("Parsing error")
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

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_test() -> Result<(), ()> {
        assert_eq!(Seat::from_str(b"FBFBBFFRLR").id(), 357);
        assert_eq!(Seat::from_str(b"BFFFBBFRRR").id(), 567);
        assert_eq!(Seat::from_str(b"FFFBBBFRRR").id(), 119);
        assert_eq!(Seat::from_str(b"BBFFBBFRLL").id(), 820);

        Ok(())
    }
}
