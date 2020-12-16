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
    let mut fields = Vec::new();
    let mut lines = input.lines();
    for line in &mut lines {
        if line.is_empty() {
            break;
        }
        let field = Field::from_str(line).expect("Cannot parse field");
        fields.push(field);
    }
    let nb_fields = fields.len();
    let self_ticket: Vec<u16> = (&mut lines)
        .nth(1)
        .unwrap()
        .split(',')
        .map(|s| s.parse().expect("Cannot parse own ticket"))
        .collect();
    let mut impossibilities: Vec<u32> = vec![0; nb_fields];
    // drop "nearby tickets: "
    for line in lines.skip(2) {
        let mut valid_ticket = true;
        let mut heh = Vec::with_capacity(nb_fields);
        for value in line.split(',') {
            let nb = value.parse().expect("cannot parse ticket");
            let mut validated: u32 = 0;
            for (j, f) in fields.iter().enumerate() {
                if f.validate(nb) {
                    validated |= 1 << j;
                }
            }
            if validated == 0 {
                valid_ticket = false;
                break;
            } else {
                heh.push(validated);
            }
        }
        if valid_ticket {
            // dbg!(&heh);
            for i in 0..nb_fields {
                impossibilities[i] |= !heh[i];
            }
        }
    }
    let mut count = 0;
    while count != nb_fields {
        count = 0;
        for i in 0..nb_fields {
            let n = !impossibilities[i];
            if (n & (n - 1)) == 0 {
                // pos i is restricted to a single field
                count += 1;
                for (j, bits) in impossibilities.iter_mut().enumerate() {
                    if j != i {
                        *bits |= n;
                    }
                }
            }
        }
    }
    let mut res: usize = 1;
    for (i, f) in fields.iter().enumerate() {
        if f.name.starts_with("departure") {
            let index = impossibilities
                .iter()
                .enumerate()
                .find(|(_i, &x)| !x == 1 << i)
                .unwrap()
                .0;
            res *= self_ticket[index] as usize;
        }
    }
    res
}

#[derive(Debug)]
struct Field<'a> {
    name: &'a str,
    min1: u16,
    max1: u16,
    min2: u16,
    max2: u16,
}

impl<'a> Field<'a> {
    fn from_str(s: &'a str) -> Option<Self> {
        let p1 = s.find(": ")?;
        let p2 = p1 + s[p1..].find('-')?;
        let min1 = s[p1 + 2..p2].parse().ok()?;
        let p3 = p2 + s[p2..].find(' ')?;
        let max1 = s[p2 + 1..p3].parse().ok()?;
        let p4 = p3 + s[p3..].find('-')?;
        let min2 = s[p3 + 4..p4].parse().ok()?;
        let max2 = s[p4 + 1..].parse().ok()?;

        Some(Self {
            name: &s[..p1],
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
        let example = "class: 0-1 or 4-19
departure_row: 0-5 or 8-19
departure_seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9";
        assert_eq!(run(example), 11 * 13)
    }
}
