#![feature(min_const_generics)]
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run::<25>(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run<const N: usize>(input: &str) -> usize {
    let mut buffer = Buffer::<N>::default();
    for (i, line) in input.lines().enumerate() {
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
    inner: [usize; N],
    end_range: usize,
}

impl<const N: usize> Buffer<N> {
    fn default() -> Self {
        Self {
            inner: [0; N],
            end_range: N - 1,
        }
    }

    fn push(&mut self, elem: usize) {
        self.end_range = (self.end_range + 1) % N;
        self.inner[self.end_range] = elem;
    }

    fn can_sum(&self, value: usize) -> bool {
        for (i, &v) in self.inner.iter().enumerate() {
            if v < value && self.inner[i + 1..].contains(&(value - v)) {
                return true;
            }
        }
        false
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
        assert_eq!(run::<5>(small_example), 127)
    }
}
