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
        .lines()
        .fold(0, |acc, entry| acc + is_valid_entry(entry) as usize)
}

fn is_valid_entry(entry: &str) -> bool {
    let mut tokens = entry.split(": ");
    Rule::from(tokens.next().unwrap()).check(tokens.next().unwrap())
}

struct Rule {
    character: char,
    first: usize,
    second: usize,
}

impl Rule {
    fn from(entry: &str) -> Self {
        let tokens: Vec<&str> = entry.split(" ").collect();
        let numbers: Vec<&str> = tokens[0].split("-").collect();

        Self {
            character: tokens[1].chars().next().unwrap(),
            first: numbers[0].parse::<usize>().unwrap(),
            second: numbers[1].parse::<usize>().unwrap(),
        }
    }

    fn check(&self, password: &str) -> bool {
        let password = password.as_bytes();
        return (password[self.first - 1] == self.character as u8)
            ^ (password[self.second - 1] == self.character as u8);
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
        assert_eq!(run(input), 1)
    }
}
