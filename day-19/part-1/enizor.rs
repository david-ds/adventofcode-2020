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
    let mut lines = input.as_bytes().split(|&b| b == b'\n');
    let mut rules = Vec::new();
    while let Some(l) = lines.next() {
        if l.is_empty() {
            break;
        } else {
            parse_rule(l, &mut rules);
        }
    }
    let mut count = 0;
    for l in lines {
        let mut pos = 0;
        if rules[0].validate(&rules, l, &mut pos) && pos == l.len() {
            count += 1;
        }
    }
    count
}

fn parse_rule(input: &[u8], rules: &mut Vec<Rule>) {
    let mut pos = 0;
    let num = stoi(input, &mut pos);
    pos += 2;
    if input[pos] == b'"' {
        let c = input[pos + 1];
        if rules.len() <= num as usize {
            rules.resize(num as usize + 1, Rule::default());
        }
        rules[num as usize] = Rule::Char(c);
    } else {
        let mut opt1 = Vec::new();
        let mut opt2 = Vec::new();
        let mut choice = 1;
        while pos < input.len() {
            if input[pos] == b'|' {
                choice += 1;
                pos += 2;
            }
            if choice == 1 {
                opt1.push(stoi(input, &mut pos));
            } else {
                opt2.push(stoi(input, &mut pos));
            }
            pos += 1;
        }
        let r = RuleRef { opt1, opt2 };
        if rules.len() <= num as usize {
            rules.resize(num as usize + 1, Rule::default());
        }
        rules[num as usize] = Rule::Ref(r);
    }
}

fn stoi(input: &[u8], pos: &mut usize) -> u8 {
    let mut res = 0;
    while *pos < input.len() {
        let c = input[*pos];
        if (b'0'..=b'9').contains(&c) {
            res *= 10;
            res += c - b'0';
            *pos += 1;
        } else {
            return res;
        }
    }
    res
}

#[derive(Debug, Clone)]
enum Rule {
    Char(u8),
    Ref(RuleRef),
}

impl Default for Rule {
    fn default() -> Self {
        Self::Char(0)
    }
}

impl Rule {
    fn validate(&self, rules: &[Rule], input: &[u8], pos: &mut usize) -> bool {
        match self {
            Self::Char(c) => {
                if input.len() > *pos {
                    *pos += 1;
                    *c == input[*pos - 1]
                } else {
                    false
                }
            }
            Self::Ref(r) => r.validate(rules, input, pos),
        }
    }
}

#[derive(Debug, Clone)]
struct RuleRef {
    opt1: Vec<u8>,
    opt2: Vec<u8>,
}

impl RuleRef {
    fn validate(&self, rules: &[Rule], input: &[u8], pos: &mut usize) -> bool {
        let mut res = true;
        let mut pos_copy = *pos;
        for &r in &self.opt1 {
            if !rules[r as usize].validate(rules, input, &mut pos_copy) {
                res = false;
                break;
            }
        }
        if res {
            *pos = pos_copy;
            return true;
        }
        pos_copy = *pos;
        for &r in &self.opt2 {
            res = true;
            if !rules[r as usize].validate(rules, input, &mut pos_copy) {
                return false;
            }
        }
        *pos = pos_copy;
        res
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run(r#"0: 4 | 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

aaaabb
aaabab
abbabb
abbbab
aabaab
aabbbb
abaaab
a
b
ab
ababbb"#),
            2
        )
    }
}
