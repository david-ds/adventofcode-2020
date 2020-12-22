use std::collections::HashMap;
use std::env::args;
use std::time::Instant;

#[derive(Debug)]
enum Rule {
    Letter(char),
    Seq(Vec<usize>),
    Choice(Box<Rule>, Box<Rule>),
}

impl Rule {
    fn seq(seq: &mut Vec<usize>) -> Self {
        let mut vec = Vec::with_capacity(seq.len());
        for i in seq.drain(..) {
            vec.push(i)
        }
        Self::Seq(vec)
    }

    fn letter(letter: char) -> Self {
        Self::Letter(letter)
    }

    fn choice(left: &mut Vec<usize>, right: &mut Vec<usize>) -> Self {
        let left_rule = Self::seq(left);
        let right_rule = Self::seq(right);
        Self::Choice(Box::new(left_rule), Box::new(right_rule))
    }
}

fn decode_line(text: &[u8], rules: &HashMap<usize, Rule>) -> bool {
    let mut pos = 0;
    let mut amount_of_42 = 0;
    loop {
        match decode_with_rule_index(pos, text, 42, rules) {
            None => return false,
            Some(new_pos) => {
                if new_pos >= text.len() {
                    return false;
                } else {
                    pos = new_pos
                }
            }
        }
        amount_of_42 += 1;
        if amount_of_42 > 1 && try_n_31(amount_of_42, pos, text, rules) {
            return true;
        }
    }
}

fn try_n_31(n: i32, pos: usize, text: &[u8], rules: &HashMap<usize, Rule>) -> bool {
    let mut cur_pos = pos;
    for _ in 0..(n - 1) {
        match decode_with_rule_index(cur_pos, text, 31, rules) {
            None => return false,
            Some(new_pos) => {
                cur_pos = new_pos;
                if new_pos >= text.len() {
                    return true;
                }
            }
        }
    }
    false
}

fn decode_with_rule_index(
    pos: usize,
    text: &[u8],
    rule_idx: usize,
    rules: &HashMap<usize, Rule>,
) -> Option<usize> {
    let rule = rules.get(&rule_idx).unwrap();
    decode_with_rule(pos, text, rule, rules)
}

fn decode_with_rule(
    pos: usize,
    text: &[u8],
    rule: &Rule,
    rules: &HashMap<usize, Rule>,
) -> Option<usize> {
    match rule {
        Rule::Letter(c) => {
            if (pos < text.len()) && (*c == text[pos] as char) {
                Some(pos + 1)
            } else {
                None
            }
        }
        Rule::Seq(seq_rules) => {
            let mut cur_pos = pos;
            for rule in seq_rules {
                match decode_with_rule_index(cur_pos, text, *rule, rules) {
                    None => return None,
                    Some(new_pos) => cur_pos = new_pos,
                }
            }
            Some(cur_pos)
        }
        Rule::Choice(left, right) => match decode_with_rule(pos, text, left, rules) {
            Some(i) => Some(i),
            None => decode_with_rule(pos, text, right, rules),
        },
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
    let mut rules: HashMap<usize, Rule> = HashMap::with_capacity(300);
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
                let rule = Rule::letter(char);
                rules.insert(cur_idx, rule);
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
                    let rule = Rule::seq(&mut seq);
                    rules.insert(cur_idx, rule);
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
                    let rule = Rule::choice(&mut seq, &mut right);
                    rules.insert(cur_idx, rule);
                    cur_idx = 0;
                }
                _ => panic!("Invalid input: {} at {}", char, idx),
            },
        }
    }
    let mut acc = 0;
    for line in input[text_idx..].lines() {
        if decode_line(line.as_bytes(), &rules) {
            acc += 1
        }
    }
    acc
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run(r#"42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"#),
            12
        )
    }
}
