use std::time::Instant;
use std::{env::args, str::FromStr};

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
        .lines()
        .map(|s| s.parse::<Seat>().expect("cannot parse").id())
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
