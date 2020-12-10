use std::collections::VecDeque;
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"), 25);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str, preamble_length: usize) -> isize {
    let numbers: Vec<isize> = input
        .lines()
        .map(|line| line.parse::<isize>().unwrap())
        .collect();

    let mut checker = Checker::new(&numbers[..preamble_length]);

    *numbers[preamble_length..]
        .iter()
        .find(|&&number| !checker.ingest(number))
        .unwrap()
}

struct Checker {
    queue: VecDeque<isize>,
}

impl Checker {
    fn new(preamble: &[isize]) -> Self {
        let mut queue = VecDeque::<isize>::with_capacity(preamble.len());
        preamble.iter().for_each(|&number| queue.push_back(number));

        Self { queue: queue }
    }

    fn ingest(&mut self, number: isize) -> bool {
        if self
            .queue
            .iter()
            .any(|n| self.queue.contains(&(number - n)))
        {
            self.queue.pop_front();
            self.queue.push_back(number);
            true
        } else {
            false
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576";

        assert_eq!(run(input, 5), 127)
    }
}
