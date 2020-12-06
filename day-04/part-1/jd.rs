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
        .fold(0, |acc, doc| acc + (doc.is_passport()) as usize)
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
        !self.birth_year.is_empty()
            && !self.issue_year.is_empty()
            && !self.expiration_year.is_empty()
            && !self.height.is_empty()
            && !self.hair_color.is_empty()
            && !self.eye_color.is_empty()
            && !self.passport_id.is_empty()
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
