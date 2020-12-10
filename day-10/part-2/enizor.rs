#![feature(min_const_generics)]
use std::time::Instant;
use std::{env::args, fmt::Debug};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut adapters = SimpleBitSet::init(MAX_ADAPTER);
    let mut max_adapter = 0;
    for line in input.lines() {
        let adapter = line.parse().expect("Cannot parse input");
        adapters.set(adapter);
        max_adapter = max_adapter.max(adapter);
    }
    adapters.set(max_adapter + 3);
    let mut buffer = Buffer::<usize, 3>::default();
    buffer.push(1);
    buffer.push(0);
    buffer.push(0);
    let mut jolt = 0;
    while jolt <= max_adapter {
        let multiplier = buffer.get(0);
        buffer.push(0);
        for i in 1..=3 {
            if adapters.get(jolt + i) {
                *buffer.get_mut(i - 1) += multiplier;
            }
        }
        jolt += 1;
    }
    buffer.get(2)
}

type Internal = usize;

const MAX_ADAPTER: usize = std::u8::MAX as usize;
const BITSET_INTERNAL_SIZE: usize = std::mem::size_of::<Internal>() * 8;
const BITSET_SIZE: usize = 1 + MAX_ADAPTER / BITSET_INTERNAL_SIZE;

struct SimpleBitSet {
    bits: [Internal; BITSET_SIZE],
}

impl SimpleBitSet {
    const fn init(n: usize) -> Self {
        let leftover_bits = n % BITSET_INTERNAL_SIZE;
        let mut bits = [0; BITSET_SIZE];

        bits[BITSET_SIZE - 1] =
            ((1 << (BITSET_INTERNAL_SIZE - leftover_bits)) - 1) << leftover_bits;
        Self { bits }
    }

    fn set(&mut self, index: usize) {
        let cur = index / BITSET_INTERNAL_SIZE;
        if cur >= self.bits.len() {
            panic!();
        } else {
            let mask = 1 << (index % BITSET_INTERNAL_SIZE);
            self.bits[cur] |= mask;
        }
    }

    fn get(&mut self, index: usize) -> bool {
        let cur = index / BITSET_INTERNAL_SIZE;
        if cur >= self.bits.len() {
            panic!();
        } else {
            let mask = 1 << (index % BITSET_INTERNAL_SIZE);
            self.bits[cur] & mask != 0
        }
    }
}

#[derive(Debug)]
struct Buffer<T: Default + Sized + Copy + Debug, const N: usize> {
    inner: [T; N],
    end_range: usize,
}

impl<T: Default + Sized + Copy + Debug, const N: usize> Buffer<T, N> {
    fn default() -> Self {
        Self {
            inner: [T::default(); N],
            end_range: 0,
        }
    }

    fn push(&mut self, elem: T) {
        self.inner[self.end_range] = elem;
        self.end_range = (self.end_range + 1) % N;
    }

    fn get(&self, index: usize) -> T {
        self.inner[(self.end_range + index) % N]
    }

    fn get_mut(&mut self, index: usize) -> &mut T {
        &mut self.inner[(self.end_range + index) % N]
    }

    fn debug(&self) {
        dbg!(self.inner[self.end_range..N]
            .iter()
            .chain(self.inner[..self.end_range].iter())
            .collect::<Vec<&T>>());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_example = r#"16
10
15
5
1
11
7
19
6
12
4"#;
        let big_example = r#"28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3"#;
        assert_eq!(run(small_example), 8);
        assert_eq!(run(big_example), 19208);
    }
}
