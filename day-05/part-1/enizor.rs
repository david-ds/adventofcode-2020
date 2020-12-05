use std::env::args;
use std::time::Instant;

fn main() -> Result<(), ()> {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"))?;
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
    Ok(())
}

fn run(input: &str) -> Result<usize, ()> {
    input
        .as_bytes()
        .split(|&c| c == b'\n')
        .map(|s| Seat::from_str(s).expect("cannot parse").id())
        .max()
        .ok_or(())
}

struct Seat {
    row: usize,
    col: usize,
}

impl Seat {
    fn id(&self) -> usize {
        8 * self.row + self.col
    }

    fn from_str(bytes: &[u8]) -> Option<Self> {
        debug_assert!(bytes.len() == 10);
        let mut row = 0;
        let mut mask = 1 << 6;
        for &c in &bytes[..7] {
            match c {
                b'B' => row |= mask,
                b'F' => {}
                _ => return None,
            }
            mask >>= 1;
        }
        let mut col = 0;
        let mut mask = 1 << 2;
        for &c in &bytes[7..10] {
            match c {
                b'R' => col |= mask,
                b'L' => {}
                _ => return None,
            }
            mask >>= 1;
        }
        Some(Seat { row, col })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_test() -> Result<(), ()> {
        assert_eq!(Seat::from_str(b"FBFBBFFRLR").ok_or(())?.id(), 357);
        assert_eq!(Seat::from_str(b"BFFFBBFRRR").ok_or(())?.id(), 567);
        assert_eq!(Seat::from_str(b"FFFBBBFRRR").ok_or(())?.id(), 119);
        assert_eq!(Seat::from_str(b"BBFFBBFRLL").ok_or(())?.id(), 820);

        Ok(())
    }
}
