use std::env::args;
use std::time::Instant;

#[derive(Debug)]
enum RuleKind {
    Letter(char),
    Seq(Vec<usize>),
    Choice(Box<Rule>, Box<Rule>),
}

#[derive(Debug)]
struct Rule {
    kind: RuleKind,
    idx: usize,
}

impl Rule {
    fn seq(idx: usize, seq: &mut Vec<usize>) -> Self {
        let mut vec = Vec::with_capacity(seq.len());
        for i in seq.drain(..) {
            vec.push(i)
        }
        Self {
            kind: RuleKind::Seq(vec),
            idx,
        }
    }

    fn letter(idx: usize, letter: char) -> Self {
        Self {
            idx,
            kind: RuleKind::Letter(letter),
        }
    }

    fn choice(idx: usize, left: &mut Vec<usize>, right: &mut Vec<usize>) -> Self {
        let left_rule = Self::seq(idx, left);
        let right_rule = Self::seq(idx, right);
        Self {
            idx,
            kind: RuleKind::Choice(Box::new(left_rule), Box::new(right_rule)),
        }
    }
}

struct Decoder<'a> {
    pos: usize,
    acc: u16,
    rules: &'a [Rule],
    string: &'a [u8],
    len: usize,
}

impl<'a> Decoder<'a> {
    fn new(rules: &'a [Rule], string: &'a [u8]) -> Self {
        Decoder {
            pos: 0,
            acc: 0,
            rules,
            string,
            len: string.len(),
        }
    }

    fn goto_next(&mut self) {
        while self.pos < self.len && self.string[self.pos] as char != '\n' {
            self.pos += 1
        }
        self.pos += 1;
    }

    fn decode(&mut self) -> u16 {
        while self.pos < self.len {
            if self.decode_line() {
                self.acc += 1
            }
        }
        self.acc
    }

    fn decode_line(&mut self) -> bool {
        if self.decode_with_rule_index(0) {
            if self.pos >= self.len || self.string[self.pos] as char == '\n' {
                self.pos += 1;
                true
            } else {
                self.goto_next();
                false
            }
        } else {
            self.goto_next();
            false
        }
    }

    fn decode_with_rule_index(&mut self, rule_idx: usize) -> bool {
        let rule = &self.rules[rule_idx];
        self.decode_with_rule(rule)
    }

    fn decode_with_rule(&mut self, rule: &Rule) -> bool {
        match &rule.kind {
            RuleKind::Letter(c) => {
                if *c == self.string[self.pos] as char {
                    self.pos += 1;
                    true
                } else {
                    false
                }
            }
            RuleKind::Seq(rules) => {
                for rule in rules.iter() {
                    if !self.decode_with_rule_index(*rule) {
                        return false;
                    }
                }
                true
            }
            RuleKind::Choice(left, right) => {
                let saved = self.pos;
                self.decode_with_rule(left)
                    || {
                        self.pos = saved;
                        self.decode_with_rule(right)
                    }
                    || {
                        self.pos = saved;
                        false
                    }
            }
        }
    }
}

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

enum ParseState {
    Idx,
    UnkownRule,
    NextIsLetter,
    NextLine,
    SeqRule,
    OrRule,
}

fn run(input: &str) -> u16 {
    let mut rules: Vec<Rule> = Vec::with_capacity(300);
    let mut text_idx = 0;
    let mut state = ParseState::Idx;
    let mut cur_n = 0;
    let mut cur_idx = 0;
    let mut skip = 0;
    let mut right: Vec<usize> = Vec::with_capacity(10);
    let mut seq: Vec<usize> = Vec::with_capacity(10);
    for (idx, char) in input.chars().enumerate() {
        if skip > 0 {
            skip -= 1;
            continue;
        }
        match state {
            ParseState::NextLine => {
                if let '\n' = char {
                    state = ParseState::Idx
                }
            }
            ParseState::Idx => match char {
                '0'..='9' => cur_idx = cur_idx * 10 + (char.to_digit(10).unwrap() as usize),
                ':' => {
                    skip = 1;
                    state = ParseState::UnkownRule
                }
                '\n' => {
                    text_idx = idx + 1;
                    break;
                }
                _ => panic!("Invalid input: {} at {}", char, idx),
            },
            ParseState::NextIsLetter => {
                let rule = Rule::letter(cur_idx, char);
                rules.push(rule);
                cur_idx = 0;
                state = ParseState::NextLine
            }
            ParseState::UnkownRule => match char {
                '"' => state = ParseState::NextIsLetter,
                '0'..='9' => {
                    cur_n = char.to_digit(10).unwrap() as usize;
                    state = ParseState::SeqRule
                }
                _ => panic!("Invalid input: {} at {}", char, idx),
            },
            ParseState::SeqRule => match char {
                '0'..='9' => cur_n = 10 * cur_n + (char.to_digit(10).unwrap() as usize),
                ' ' => {
                    seq.push(cur_n);
                    cur_n = 0
                }
                '\n' => {
                    state = ParseState::Idx;
                    seq.push(cur_n);
                    cur_n = 0;
                    let rule = Rule::seq(cur_idx, &mut seq);
                    rules.push(rule);
                    cur_idx = 0;
                }
                '|' => {
                    skip = 1;
                    state = ParseState::OrRule;
                }
                _ => panic!("Invalid input: {} at {}", char, idx),
            },
            ParseState::OrRule => match char {
                '0'..='9' => cur_n = 10 * cur_n + (char.to_digit(10).unwrap() as usize),
                ' ' => {
                    right.push(cur_n);
                    cur_n = 0;
                }
                '\n' => {
                    state = ParseState::Idx;
                    right.push(cur_n);
                    cur_n = 0;
                    let rule = Rule::choice(cur_idx, &mut seq, &mut right);
                    rules.push(rule);
                    cur_idx = 0;
                }
                _ => panic!("Invalid input: {} at {}", char, idx),
            },
        }
    }
    rules.sort_by_key(|rule| rule.idx);
    let mut decoder = Decoder::new(&rules, input[text_idx..].as_bytes());
    decoder.decode()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run(r#"0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"#),
            2
        )
    }
}
