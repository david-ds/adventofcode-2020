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
    let mut res = 0;
    for line in input.as_bytes().split(|&b| b == b'\n') {
        res += evaluate(line);
    }
    res
}

fn evaluate(bytes: &[u8]) -> usize {
    let mut result = 0;
    let mut reg = 0;
    let mut op = Op::Plus;
    let mut ev = false;
    let mut i = 0;
    while i < bytes.len() {
        match bytes[i] {
            b' ' => (),
            b'+' => op = Op::Plus,
            b'*' => op = Op::Mult,
            b'(' => {
                let j = i + 1 + next_parenthesis(&bytes[i + 1..]).unwrap();
                reg = evaluate(&bytes[i + 1..j]);
                i = j;
                ev = true;
            }
            b => {
                reg = (b - b'0') as usize;
                ev = true
            }
        }
        if ev {
            match op {
                Op::Plus => result += reg,
                Op::Mult => result *= reg,
            }
            ev = false;
        }
        i += 1;
    }
    result
}

fn next_parenthesis(bytes: &[u8]) -> Option<usize> {
    let mut count = 1;
    let mut pos = 0;
    while pos < bytes.len() {
        match bytes[pos] {
            b'(' => count += 1,
            b')' => count -= 1,
            _ => (),
        }
        if count == 0 {
            return Some(pos);
        }
        pos += 1;
    }
    None
}

enum Op {
    Plus,
    Mult,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(evaluate(&"1 + 2 * 3 + 4 * 5 + 6".as_bytes()), 71);
        assert_eq!(evaluate(&"2 * 3 + (4 * 5)".as_bytes()), 26);
        assert_eq!(evaluate(&"5 + (8 * 3 + 9 + 3 * 4 * 3)".as_bytes()), 437);
        assert_eq!(
            evaluate(&"5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))".as_bytes()),
            12240
        );
        assert_eq!(
            evaluate(&"((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2".as_bytes()),
            13632
        );
    }
}
