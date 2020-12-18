use std::cmp::{max, min};
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

trait IntvVec {
    fn push_intv(&mut self, intv: (u16, u16));
    fn invalid(&self, point: u16) -> bool;
}

impl IntvVec for Vec<(u16, u16)> {
    fn push_intv(&mut self, (l, h): (u16, u16)) {
        let mut i = 0;
        let len = self.len();
        while i < len {
            let (cl, ch) = self[i];
            if l > ch {
                i += 1;
                continue;
            }
            if h < cl {
                self.insert(i, (l, h));
                return;
            }
            if h <= ch {
                self[i] = (min(l, cl), ch);
                return;
            }
            let base = i;
            i += 1;
            let nmin = min(l, cl);
            let mut nmax = max(h, ch);
            while i < len {
                let (ncl, nch) = self[i];
                if nmax < ncl {
                    break;
                }
                nmax = max(nmax, nch);
                i += 1
            }
            self[base] = (nmin, nmax);
            self.drain(base + 1..i);
            return;
        }
        self.push((l, h))
    }
    fn invalid(&self, point: u16) -> bool {
        for (l, h) in self {
            if *l <= point && point <= *h {
                return false;
            }
        }
        true
    }
}

fn parse_field(line: &str) -> ((u16, u16), (u16, u16)) {
    let col = line.find(':').unwrap();
    let dash_1 = line[col..].find('-').unwrap() + col;
    let o = line[dash_1..].find('o').unwrap() + dash_1;
    let dash_2 = line[o..].find('-').unwrap() + o;
    let l1 = line[col + 2..dash_1].parse().unwrap();
    let h1 = line[dash_1 + 1..o - 1].parse().unwrap();
    let l2 = line[o + 3..dash_2].parse().unwrap();
    let h2 = line[dash_2 + 1..].parse().unwrap();
    ((l1, h1), (l2, h2))
}

fn run(input: &str) -> u16 {
    let mut ignore = 0;
    let mut parsing_fields = true;
    let mut allowed_ranges = Vec::with_capacity(50);
    let mut acc = 0u16;
    for line in input.split('\n') {
        if ignore > 0 {
            ignore -= 1
        } else if parsing_fields {
            match line {
                "" => {
                    ignore = 4;
                    parsing_fields = false
                }
                line => {
                    let (a, b) = parse_field(line);
                    allowed_ranges.push_intv(a);
                    allowed_ranges.push_intv(b);
                }
            }
        } else {
            for n in line.split(',') {
                let point: u16 = n.parse().unwrap();
                if allowed_ranges.invalid(point) {
                    acc += point
                }
            }
        }
    }
    acc
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn giltho_day16_p1() {
        let input = r#"class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"#;
        assert_eq!(run(input), 71)
    }
}
