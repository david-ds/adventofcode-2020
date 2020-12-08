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
    VM::new(input).run()
}

#[derive(Debug, Copy, Clone)]
enum Operation {
    Acc(isize),
    Jmp(isize),
    Nop,
}

impl Operation {
    fn from(string: &str) -> Self {
        let mut tokens = string.split(' ');
        match tokens.next().unwrap() {
            "jmp" => Operation::Jmp(tokens.next().unwrap().parse::<isize>().unwrap()),
            "acc" => Operation::Acc(tokens.next().unwrap().parse::<isize>().unwrap()),
            _ => Operation::Nop,
        }
    }
}

#[derive(Default, Debug)]
struct VM {
    code: Vec<(Operation, bool)>,
    cursor: isize,
    acc: isize,
}

impl VM {
    fn new(input: &str) -> Self {
        VM {
            cursor: 0,
            acc: 0,
            code: input
                .lines()
                .map(|line| (Operation::from(line), false))
                .collect(),
        }
    }

    fn run(&mut self) -> isize {
        self.count();
        self.acc
    }
}

impl Iterator for VM {
    type Item = ();

    fn next(&mut self) -> Option<()> {
        let (op, seen) = self.code[self.cursor as usize];
        if seen {
            None
        } else {
            self.code[self.cursor as usize].1 = true;
            match op {
                Operation::Nop => {
                    self.cursor += 1;
                    Some(())
                }
                Operation::Acc(amount) => {
                    self.acc += amount;
                    self.cursor += 1;
                    Some(())
                }
                Operation::Jmp(gap) => {
                    self.cursor += gap;
                    Some(())
                }
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6";

        assert_eq!(run(input), 5)
    }
}
