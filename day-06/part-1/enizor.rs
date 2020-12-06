use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u32 {
    let mut answered: u32 = 0;
    let mut total = 0;
    let mut found_newline = false;
    for &b in input.as_bytes().iter().chain(&[b'\n', b'\n']) {
        if b == b'\n' {
            if found_newline {
                total += answered.count_ones();
                answered = 0;
            }
            found_newline = !found_newline;
        } else {
            found_newline = false;
            let c = b - b'a';
            answered |= 1 << c;
        }
    }
    total
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_input = r#"abc

a
b
c

ab
ac

a
a
a
a

b"#;
        assert_eq!(run(small_input), 11)
    }
}
