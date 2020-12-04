use std::env::args;
use std::time::Instant;

use regex::Regex;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> isize {
    input
        .split("\n\n")
        .collect::<Vec<&str>>()
        .iter()
        .map(|doc| Document::from(doc))
        .fold(0, |acc, doc| acc + (doc.is_passport() as isize))
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
    _country_id: String,
}

impl Document {
    fn from(string: &str) -> Self {
        let mut doc = Document::default();

        for token in string
            .split("\n")
            .collect::<Vec<&str>>()
            .iter()
            .map(|line| line.split(" ").collect::<Vec<&str>>())
            .flatten()
            .collect::<Vec<&str>>()
            .iter()
        {
            let tokens = token.split(":").collect::<Vec<&str>>();
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
    if let Some(year) = string.parse::<u32>().ok() {
        return year <= max && year >= min;
    }

    false
}

fn assert_id(string: &str) -> bool {
    Regex::new(r"^\d{9}$").unwrap().is_match(string)
}

fn assert_color(string: &str) -> bool {
    match string {
        "amb" | "blu" | "brn" | "gry" | "grn" | "hzl" | "oth" => true,
        _ => false,
    }
}

fn assert_hex_color(string: &str) -> bool {
    Regex::new(r"#[0-9a-fA-F]{6}").unwrap().is_match(string)
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
        let input = "ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in";

        assert_eq!(run(input), 2)
    }
}
