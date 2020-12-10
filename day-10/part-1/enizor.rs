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
    let mut set = SimpleBitSet::init(MAX_ADAPTER);
    let mut max_adapter = 0;
    for line in input.lines() {
        let adapter = line.parse().expect("Cannot parse input");
        set.set(adapter);
        max_adapter = max_adapter.max(adapter);
    }
    let mut jolt = 0;
    let mut t = [0; 3];
    t[2] = 1;
    for value in 0..=max_adapter {
        if set.get(value) {
            t[value - jolt - 1] += 1;
            jolt = value;
        }
    }
    t[0] * t[2]
}

const MAX_ADAPTER: usize = std::u8::MAX as usize;
const BITSET_INTERNAL_SIZE: usize = std::mem::size_of::<Internal>() * 8;
const BITSET_SIZE: usize = 1 + MAX_ADAPTER / BITSET_INTERNAL_SIZE;

type Internal = usize;
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
        assert_eq!(run(small_example), 35);
        assert_eq!(run(big_example), 220);
    }
}
