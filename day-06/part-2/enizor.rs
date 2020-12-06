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
    const NEWLINE_MASK: u32 = 0xfffffffe;
    let mut answered: u32 = 0; // First bit is used to tell if we just me a newline\
    let mut previous_person: u32 = 0xfffffffe;
    let mut total = 0;
    for &b in input.as_bytes().iter().chain(&[b'\n', b'\n']) {
        if b == b'\n' {
            if (answered & 1) == 1 {
                total += previous_person.count_ones();
                answered = 0;
                previous_person = 0xfffffffe;
            } else {
                previous_person &= answered;
                answered = 1;
            }
        } else {
            answered &= NEWLINE_MASK;
            let c = b - 96;
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
        assert_eq!(run(small_input), 6)
    }
}
