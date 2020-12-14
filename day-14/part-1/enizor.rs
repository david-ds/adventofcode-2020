#![feature(destructuring_assignment)]

use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u64 {
    let mut mask_or: u64 = 0;
    let mut mask_and: u64 = u64::MAX;
    let mut sum: u64 = 0;
    let mut values: Vec<(u64, u64)> = Vec::new();
    for line in input.lines() {
        match &line[..4] {
            "mask" => (mask_and, mask_or) = parse_mask(&line[7..]),
            "mem[" => {
                let (pointer, mut value) = parse_value(&line[4..]);
                value |= mask_or;
                value &= mask_and;
                sum += value;
                let mut found = false;
                for (p, v) in values.iter_mut() {
                    if pointer == *p {
                        sum -= *v;
                        *v = value;
                        found = true;
                        break;
                    }
                }
                if !found {
                    values.push((pointer, value));
                }
            }
            _ => panic!("Cannot parse input"),
        }
    }
    sum
}

fn parse_mask(input: &str) -> (u64, u64) {
    let mut mask_and: u64 = u64::MAX;
    let mut mask_or: u64 = 0;
    for &b in input.as_bytes() {
        mask_and <<= 1;
        mask_and += 1;
        mask_or <<= 1;
        match b {
            b'0' => mask_and &= u64::MAX - 1,
            b'1' => mask_or += 1,
            b'X' => (),
            _ => panic!("Cannot parse mask"),
        }
    }
    (mask_and, mask_or)
}

fn parse_value(input: &str) -> (u64, u64) {
    let bracket = input.find(']').unwrap();
    let pointer = input[..bracket].parse().unwrap();
    let value = input[bracket + 4..].parse().unwrap();
    (pointer, value)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_program = "mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0";
        assert_eq!(run(small_program), 165)
    }
}
