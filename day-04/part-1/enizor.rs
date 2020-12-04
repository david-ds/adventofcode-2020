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
    input.split("\n\n").filter(|&p| validate(p)).count() as isize
}

const FIELDS_NB: usize = 7;
const FIELDS_STR: [&str; FIELDS_NB] = ["ecl", "pid", "eyr", "hcl", "byr", "iyr", "hgt"];

fn validate(passport: &str) -> bool {
    let mut bitset = SimpleBitSet::init(FIELDS_NB);
    for line in passport.split_whitespace() {
        if let Some(field) = line.split(':').next() {
            for (i, &f) in FIELDS_STR.iter().enumerate() {
                if field == f {
                    bitset.set(i)
                }
            }
        }
    }
    bitset.is_full()
}

const BITSET_INTERNAL_SIZE: usize = std::mem::size_of::<u8>() * 8;
const BITSET_SIZE: usize = 1 + FIELDS_NB / BITSET_INTERNAL_SIZE;

struct SimpleBitSet {
    bits: [u8; BITSET_SIZE],
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

    fn is_full(&self) -> bool {
        for &x in &self.bits {
            if x != !0 {
                return false;
            }
        }
        true
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_input = r#"ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"#;
        assert_eq!(run(small_input), 2)
    }
}
