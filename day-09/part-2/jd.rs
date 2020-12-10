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

    let target = *numbers[preamble_length..]
        .iter()
        .find(|&&number| !checker.ingest(number))
        .unwrap();

    let (start, end) = find_range(&numbers, target);

    min_plus_max(&numbers[start..end + 1])
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

fn find_range(numbers: &[isize], target: isize) -> (usize, usize) {
    let mut sums = Vec::<isize>::with_capacity(numbers.len());

    numbers
        .iter()
        .for_each(|&number| sums.push(sums.last().unwrap_or(&0) + number));

    for (i, s) in sums.iter().enumerate() {
        if let Some(res) = dichotomy(&sums[i + 1..], s + target) {
            return (i + 1, i + res + 1);
        }
    }

    (0, 0)
}

fn dichotomy<T: PartialEq + PartialOrd>(array: &[T], searched: T) -> Option<usize> {
    if array.is_empty() {
        return None;
    }

    let middle = array.len() / 2;

    if array[middle] == searched {
        Some(middle)
    } else if array[middle] > searched {
        dichotomy(&array[..middle], searched)
    } else {
        if let Some(i) = dichotomy(&array[middle + 1..], searched) {
            Some(middle + i + 1)
        } else {
            None
        }
    }
}

fn min_plus_max(numbers: &[isize]) -> isize {
    let mut min = isize::MAX;
    let mut max = 0;

    for n in numbers.iter() {
        if *n > max {
            max = *n;
        }

        if *n < min {
            min = *n;
        }
    }

    max + min
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

        assert_eq!(run(input, 5), 62)
    }
}
