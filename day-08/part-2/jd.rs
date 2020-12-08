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
    let mut vm = VM::new(input);

    for i in 0..vm.code.len() {
        if vm.code[i].0 == Operation::Acc {
            continue;
        } else {
            vm.swap(i);
        }

        vm.run();

        if vm.cursor as usize >= vm.code.len() {
            return vm.acc;
        } else {
            vm.reset();
        }
    }

    0
}

#[derive(Debug, Copy, Clone, PartialEq)]
enum Operation {
    Acc,
    Jmp,
    Nop,
}

impl Operation {
    fn from(string: &str) -> Self {
        match string {
            "jmp" => Operation::Jmp,
            "acc" => Operation::Acc,
            "nop" => Operation::Nop,
            _ => Operation::Nop,
        }
    }
}

#[derive(Default, Debug)]
struct VM {
    code: Vec<(Operation, isize, bool)>,
    cursor: isize,
    acc: isize,
    swap_cursor: usize,
}

impl VM {
    fn new(input: &str) -> Self {
        VM {
            cursor: 0,
            swap_cursor: 0,
            acc: 0,
            code: input
                .lines()
                .map(|line| {
                    let mut tokens = line.split(' ');
                    (
                        Operation::from(tokens.next().unwrap()),
                        tokens.next().unwrap().parse::<isize>().unwrap(),
                        false,
                    )
                })
                .collect(),
        }
    }

    fn run(&mut self) -> isize {
        self.count();
        self.acc
    }

    fn reset(&mut self) {
        self.acc = 0;
        self.cursor = 0;
        self.swap(self.swap_cursor);
        self.swap_cursor = 0;
        for i in 0..self.code.len() {
            self.code[i].2 = false;
        }
    }

    fn swap(&mut self, i: usize) {
        self.swap_cursor = i;

        match self.code[i].0 {
            Operation::Jmp => {
                self.code[i].0 = Operation::Nop;
            }
            Operation::Nop => {
                self.code[i].0 = Operation::Jmp;
            }
            Operation::Acc => {}
        };
    }
}

impl Iterator for VM {
    type Item = ();

    fn next(&mut self) -> Option<()> {
        if self.cursor as usize >= self.code.len() {
            None
        } else {
            let (op, arg, seen) = self.code[self.cursor as usize];
            if seen {
                None
            } else {
                self.code[self.cursor as usize].2 = true;
                match op {
                    Operation::Nop => {
                        self.cursor += 1;
                        Some(())
                    }
                    Operation::Acc => {
                        self.acc += arg;
                        self.cursor += 1;
                        Some(())
                    }
                    Operation::Jmp => {
                        self.cursor += arg;
                        Some(())
                    }
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

        assert_eq!(run(input), 8)
    }
}
