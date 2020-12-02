use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

#[derive(Default)]
struct Policy {
    min: usize,
    max: usize,
    letter: char,
}

impl Policy {
    fn parse(input: &str) -> bool {
        let mut out = Policy::default();
        let dash = input.find('-').expect("No dash");
        out.min = input[..dash].parse().expect("cannot parse min value");
        let space = input.find(' ').expect("No space");
        out.max = input[dash + 1..space]
            .parse()
            .expect("cannot parse max value");
        out.letter = input[space + 1..].chars().next().unwrap();
        out.validate(&input[space + 4..])
    }
    fn validate(&self, password: &str) -> bool {
        let mut it = password.chars().filter(|&c| c == self.letter);
        it.nth(self.min - 1).is_some()
            && it.take(self.max - self.min + 1).count() < self.max - self.min + 1
    }
}

fn run(input: &str) -> isize {
    input.lines().filter(|&line| Policy::parse(line)).count() as isize
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_input = "1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc";
        assert_eq!(run(small_input), 2)
    }
}
