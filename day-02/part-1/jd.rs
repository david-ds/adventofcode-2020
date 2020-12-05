use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> isize {
    validate_entries(&parse_input(input)) as isize
}

fn parse_input(input: &str) -> Vec<&str> {
    input.split("\n").collect()
}

fn validate_entries(entries: &[&str]) -> usize {
    entries
        .iter()
        .fold(0, |acc, entry| acc + is_valid_entry(entry) as usize)
}

fn is_valid_entry(entry: &str) -> bool {
    let tokens: Vec<&str> = entry.split(": ").collect();
    Rule::from(tokens[0]).check(tokens[1])
}

struct Rule {
    character: char,
    min: usize,
    max: usize,
}

impl Rule {
    fn from(entry: &str) -> Self {
        let tokens: Vec<&str> = entry.split(" ").collect();
        let numbers: Vec<&str> = tokens[0].split("-").collect();

        Self {
            character: tokens[1].chars().next().unwrap(),
            min: numbers[0].parse::<usize>().unwrap(),
            max: numbers[1].parse::<usize>().unwrap(),
        }
    }

    fn check(&self, password: &str) -> bool {
        let count = password
            .chars()
            .fold(0, |acc, c| acc + (c == self.character) as usize);

        self.max >= count && self.min <= count
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc";
        assert_eq!(run(input), 2)
    }
}
