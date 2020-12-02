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
    pos1: usize,
    pos2: usize,
    letter: char,
}

impl Policy {
    fn parse(input: &str) -> bool {
        let mut out = Policy::default();
        let dash = input.find('-').expect("No dash");
        out.pos1 = input[..dash].parse().expect("cannot parse min value");
        let space = input.find(' ').expect("No space");
        out.pos2 = input[dash + 1..space]
            .parse()
            .expect("cannot parse max value");
        out.letter = input[space + 1..].chars().next().unwrap();
        out.validate(&input[space + 4..])
    }
    fn validate(&self, password: &str) -> bool {
        let mut res = false;
        for (pos, c) in password[..self.pos2].chars().enumerate() {
            if pos == self.pos1 || pos == self.pos2 {
                res ^= c == self.letter;
            }
        }
        res
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
        assert_eq!(run(small_input), 1)
    }
}
