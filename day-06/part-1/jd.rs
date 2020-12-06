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
        .split("\n\n")
        .map(|group| {
            let mut map = [false; 26];
            group
                .as_bytes()
                .iter()
                .filter(|c| **c != 10)
                .fold(0, |total, c| {
                    let idx = (c - 97) as usize;
                    if map[idx] {
                        total
                    } else {
                        map[idx] = true;
                        total + 1
                    }
                })
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "abc

a
b
c

ab
ac

a
a
a
a

b";
        assert_eq!(run(input), 11)
    }
}
