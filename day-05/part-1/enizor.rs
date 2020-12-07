use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u16 {
    let bytes = input
        .as_bytes();
    let mut cur = 0;
    let mut max = 0;
    while cur < bytes.len()-10 {
        max = max.max(parse_seat(&bytes[cur..cur+10]));
        cur += 11;
    }
    max
}

fn parse_seat(bytes: &[u8]) -> u16 {
    debug_assert!(bytes.len() == 10);
    let mut id : u16 = 0;
    for (i, &c) in bytes[..7].iter().enumerate() {
        // B = 0b01000010
        // F = 0b01000110
        id |= (((c ^ b'F') as u16) << 7) >> i;
    }
    for (i, &c) in bytes[7..10].iter().enumerate() {
        // R = 0b01010010
        // L = 0b01001100
        id |= (((c & 0b00000010)as u16) << 1) >> i;
    }
    id
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parse_test() -> Result<(), ()> {
        assert_eq!(parse_seat(b"FBFBBFFRLR"), 357);
        assert_eq!(parse_seat(b"BFFFBBFRRR"), 567);
        assert_eq!(parse_seat(b"FFFBBBFRRR"), 119);
        assert_eq!(parse_seat(b"BBFFBBFRLL"), 820);

        Ok(())
    }
}
