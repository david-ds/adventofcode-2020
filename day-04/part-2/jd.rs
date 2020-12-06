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
        .split("\n\n")
        .map(|doc| Document::from(doc))
        .fold(0, |acc, doc| acc + (doc.is_passport() as usize))
}

#[derive(Default)]
struct Document {
    birth_year: String,
    issue_year: String,
    expiration_year: String,
    height: String,
    hair_color: String,
    eye_color: String,
    passport_id: String,
}

impl Document {
    fn from(string: &str) -> Self {
        let mut doc = Document::default();

        for token in string.split('\n').map(|line| line.split(' ')).flatten() {
            let tokens = token.split(':').collect::<Vec<&str>>();
            let value = tokens[1].to_string();
            match tokens[0] {
                "byr" => {
                    doc.birth_year = value;
                }
                "iyr" => {
                    doc.issue_year = value;
                }
                "eyr" => {
                    doc.expiration_year = value;
                }
                "hgt" => {
                    doc.height = value;
                }
                "hcl" => {
                    doc.hair_color = value;
                }
                "ecl" => {
                    doc.eye_color = value;
                }
                "pid" => {
                    doc.passport_id = value;
                }
                _ => {}
            };
        }

        doc
    }

    fn is_passport(&self) -> bool {
        assert_int(&self.birth_year, 1920, 2002)
            && assert_int(&self.issue_year, 2010, 2020)
            && assert_int(&self.expiration_year, 2020, 2030)
            && assert_id(&self.passport_id)
            && assert_color(&self.eye_color)
            && assert_hex_color(&self.hair_color)
            && assert_height(&self.height)
    }
}

fn assert_int(string: &str, min: u32, max: u32) -> bool {
    if let Ok(year) = string.parse::<u32>() {
        return year <= max && year >= min;
    }

    false
}

fn assert_id(string: &str) -> bool {
    if string.len() == 9 {
        string.chars().all(|c| matches!(c, '0'..='9'))
    } else {
        false
    }
}

fn assert_color(string: &str) -> bool {
    matches!(string, "amb" | "blu" | "brn" | "gry" | "grn" | "hzl" | "oth")
}

fn assert_hex_color(string: &str) -> bool {
    if string.len() == 7 {
        if string.as_bytes()[0] == b'#' {
            string[1..]
                .chars()
                .all(|c| matches!(c, '0'..='9' |'a'..='f'))
        } else {
            false
        }
    } else {
        false
    }
}

fn assert_height(string: &str) -> bool {
    if string.len() > 2 {
        match &string[string.len() - 2..] {
            "cm" => assert_int(&string[..string.len() - 2], 150, 193),
            "in" => assert_int(&string[..string.len() - 2], 59, 76),
            _ => false,
        }
    } else {
        false
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let valid_input = "pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719";

        let invalid_input = "eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007";

        assert_eq!(run(valid_input), 4);
        assert_eq!(run(invalid_input), 0)
    }
}
