use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u16 {
    let mut fields = Vec::new();
    let mut lines = input.lines();
    for line in &mut lines {
        if line.is_empty() {
            break;
        }
        let field = Field::from_str(line).expect("Cannot parse field");
        fields.push(field);
    }
    for line in &mut lines {
        if line.is_empty() {
            break;
        }
    }
    let mut rate = 0;
    // drop "nearby tickets: "
    for line in lines.skip(1) {
        for value in line.split(',') {
            let nb = value.parse().expect("cannot parse ticket");
            if fields.iter().all(|f| !f.validate(nb)) {
                rate += nb;
            }
        }
    }
    rate
}

#[derive(Debug)]
struct Field {
    min1: u16,
    max1: u16,
    min2: u16,
    max2: u16,
}

impl Field {
    fn from_str(s: &str) -> Option<Self> {
        let p1 = s.find(": ")?;
        let p2 = p1 + s[p1..].find('-')?;
        let min1 = s[p1 + 2..p2].parse().ok()?;
        let p3 = p2 + s[p2..].find(' ')?;
        let max1 = s[p2 + 1..p3].parse().ok()?;
        let p4 = p3 + s[p3..].find('-')?;
        let min2 = s[p3 + 4..p4].parse().ok()?;
        let max2 = s[p4 + 1..].parse().ok()?;

        Some(Self {
            min1,
            max1,
            min2,
            max2,
        })
    }
    fn validate(&self, nb: u16) -> bool {
        (self.min1 <= nb && nb <= self.max1) || (self.min2 <= nb && nb <= self.max2)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let example = "class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12";
        assert_eq!(run(example), 71)
    }
}
