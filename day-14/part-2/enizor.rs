#![feature(destructuring_assignment)]
use std::time::Instant;
use std::{collections::HashMap, env::args};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

type Pointer = [FloatingBit; 36];

#[derive(Copy, Clone, Eq, PartialEq, Debug)]
enum FloatingBit {
    Zero,
    One,
    X,
}
use FloatingBit::*;

fn run(input: &str) -> usize {
    let mut mask = [X; 36];
    let mut mem = HashMap::new();
    let mut sum = 0;
    for line in input.lines() {
        match &line[..4] {
            "mask" => mask = parse_mask(&line[7..]),
            "mem[" => {
                let bracket = line.find(']').unwrap();
                let pointer_int = line[4..bracket].parse().unwrap();
                let pointer = apply_mask(pointer_int, mask);
                let value: usize = line[bracket + 4..].parse().unwrap();
                let ptrs = iter_pointer(&pointer);
                for p in ptrs {
                    sum += value;
                    if let Some(v) = mem.insert(p, value) {
                        sum -= v;
                    }
                }
            }
            _ => panic!("Cannot parse input"),
        }
    }
    sum
}

fn parse_mask(input: &str) -> Pointer {
    let mut pointer = [X; 36];
    for (i, &b) in input.as_bytes().iter().enumerate() {
        pointer[i] = match b {
            b'0' => Zero,
            b'1' => One,
            b'X' => X,
            _ => panic!("Cannot parse mask"),
        }
    }
    pointer
}

fn apply_mask(pointer: usize, mask: Pointer) -> Pointer {
    let mut out = [Zero; 36];
    let p = to_pointer(pointer);
    for i in 0..36 {
        out[i] = match mask[i] {
            Zero => p[i],
            f_b => f_b,
        }
    }
    out
}

fn to_pointer(mut p: usize) -> Pointer {
    let mut pointer = [Zero; 36];
    for i in (0..36).rev() {
        pointer[i] = match p & 1 {
            0 => Zero,
            1 => One,
            _ => unreachable!(),
        };
        p >>= 1;
    }
    pointer
}

fn iter_pointer(ptr: &Pointer) -> Vec<usize> {
    let mut out = vec![0];
    for i in 0..36 {
        match ptr[35 - i] {
            Zero => (),
            One => {
                for v in out.iter_mut() {
                    *v += 1 << i;
                }
            }
            X => {
                let mut t = out.clone();
                for v in t.iter_mut() {
                    *v += 1 << i;
                }
                out.append(&mut t);
            }
        }
    }
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_program = "mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1";
        assert_eq!(run(small_program), 208)
    }
}
