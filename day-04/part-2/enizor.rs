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

fn validate_byr(value: &str) -> Validation {
    if value.len() != 4 {
        Validation::Invalid
    } else {
        let v = value.parse().unwrap_or(0);
        if (1920..=2002).contains(&v) {
            Validation::Valid(0)
        } else {
            Validation::Invalid
        }
    }
}

fn validate_iyr(value: &str) -> Validation {
    if value.len() != 4 {
        Validation::Invalid
    } else {
        let v = value.parse().unwrap_or(0);
        if (2010..=2020).contains(&v) {
            Validation::Valid(1)
        } else {
            Validation::Invalid
        }
    }
}

fn validate_eyr(value: &str) -> Validation {
    if value.len() != 4 {
        Validation::Invalid
    } else {
        let v = value.parse().unwrap_or(0);
        if (2020..=2030).contains(&v) {
            Validation::Valid(2)
        } else {
            Validation::Invalid
        }
    }
}

fn validate_hgt(value: &str) -> Validation {
    let n = value.len();
    if n <= 2 {
        Validation::Invalid
    } else {
        let v = value[..n - 2].parse().unwrap_or(0);
        if (&value[n - 2..] == "cm" && v >= 150 && v <= 193)
            || (&value[n - 2..] == "in" && v >= 59 && v <= 76)
        {
            Validation::Valid(3)
        } else {
            Validation::Invalid
        }
    }
}

fn validate_hcl(value: &str) -> Validation {
    let n = value.len();
    if n != 7 || value.as_bytes()[0] != b'#' {
        Validation::Invalid
    } else if value[1..]
        .chars()
        .all(|c| matches!(c, 'a'..='f' | '0'..='9'))
    {
        Validation::Valid(4)
    } else {
        Validation::Invalid
    }
}

fn validate_ecl(value: &str) -> Validation {
    if matches!(value, "amb" | "blu" | "brn" | "gry" | "grn" | "hzl" | "oth") {
        Validation::Valid(5)
    } else {
        Validation::Invalid
    }
}

fn validate_pid(value: &str) -> Validation {
    if value.len() != 9 {
        Validation::Invalid
    } else if value.chars().all(|c| matches!(c, '0'..='9')) {
        Validation::Valid(6)
    } else {
        Validation::Invalid
    }
}

enum Validation {
    Valid(usize),
    Invalid,
    Unvalidated,
}

fn validate_field(line: &str) -> Validation {
    if let Some(pos) = line.find(':') {
        let (field, colon_value) = line.split_at(pos);
        let value = &colon_value[1..];
        match field {
            "byr" => validate_byr(value),
            "iyr" => validate_iyr(value),
            "eyr" => validate_eyr(value),
            "hgt" => validate_hgt(value),
            "hcl" => validate_hcl(value),
            "ecl" => validate_ecl(value),
            "pid" => validate_pid(value),
            _ => Validation::Unvalidated,
        }
    } else {
        Validation::Unvalidated
    }
}

fn validate(passport: &str) -> bool {
    let mut bitset = SimpleBitSet::init(FIELDS_NB);
    for line in passport.split_whitespace() {
        match validate_field(line) {
            Validation::Valid(flag) => bitset.set(flag),
            Validation::Invalid => return false,
            Validation::Unvalidated => {}
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
        let invalid_input = r#"eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"#;

        let valid_input = r#"pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719"#;
        assert_eq!(run(invalid_input), 0);
        assert_eq!(run(valid_input), 4)
    }
}
