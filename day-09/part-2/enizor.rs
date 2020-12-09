#![feature(min_const_generics)]
use std::time::Instant;
use std::{env::args, str::Lines};

fn main() {
    let now = Instant::now();
    let output = run::<25>(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run<const N: usize>(input: &str) -> usize {
    let mut lines = input.lines();
    let mut buffer = Buffer::<N>::default(lines.size_hint().0);
    let invalid = find_invalid(&mut lines, &mut buffer);
    for line in lines {
        buffer.push(line.parse().expect("cannot parse input"));
    }
    buffer.find_contiguous(invalid)
}

fn find_invalid<const N: usize>(input: &mut Lines, buffer: &mut Buffer<N>) -> usize {
    for (i, line) in input.enumerate() {
        let value = line.parse().expect("cannot parse input");
        if i < N || buffer.can_sum(value) {
            buffer.push(value);
        } else {
            return value;
        }
    }
    0
}

struct Buffer<const N: usize> {
    inner: Vec<usize>,
    end_range: usize,
}

impl<const N: usize> Buffer<N> {
    fn default(capacity: usize) -> Self {
        Self {
            inner: Vec::with_capacity(capacity),
            end_range: 0,
        }
    }

    fn push(&mut self, elem: usize) {
        self.inner.push(elem);
        self.end_range += 1;
    }

    fn can_sum(&self, value: usize) -> bool {
        for (i, &v) in self.inner[self.end_range - N..self.end_range]
            .iter()
            .enumerate()
        {
            if v < value && self.inner[self.end_range - N + i + 1..].contains(&(value - v)) {
                return true;
            }
        }
        false
    }

    fn find_contiguous(&self, value: usize) -> usize {
        let mut start = 0;
        let mut end = 0;
        let mut sum = self.inner[start];
        while sum != value {
            if sum > value {
                sum -= self.inner[start];
                start += 1;
            } else {
                end += 1;
                sum += self.inner[end];
            }
        }
        let mut min = self.inner[start];
        let mut max = min;
        for &v in &self.inner[start + 1..=end] {
            if v < min {
                min = v
            } else if v > max {
                max = v
            }
        }
        min + max
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_example = r#"35
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
576"#;
        let mut lines = small_example.lines();
        let mut buffer = Buffer::<5>::default(lines.size_hint().0);
        assert_eq!(find_invalid(&mut lines, &mut buffer), 127);
        assert_eq!(run::<5>(small_example), 62)
    }
}
