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
    Memory::init(input).run_changes()
}

#[derive(Debug, Clone, Copy)]
enum InstructionSet {
    NOP(isize),
    ACC(isize),
    JMP(isize),
}

impl Default for InstructionSet {
    fn default() -> Self {
        Self::NOP(0)
    }
}

impl InstructionSet {
    fn parse(input: &str) -> Self {
        match &input[..3] {
            "nop" => Self::NOP(input[4..].parse().expect("cannot parse NOP value")),
            "acc" => Self::ACC(input[4..].parse().expect("cannot parse ACC value")),
            "jmp" => Self::JMP(input[4..].parse().expect("cannot parse JMP value")),
            _ => Default::default(),
        }
    }
}

#[derive(Default)]
struct Memory {
    accumulator: isize,
    // previous_ip: isize,
    ip: isize,
    instructions: Vec<InstructionSet>,
    visited: Vec<bool>,
}

enum RunState {
    Looped,
    Finished,
    Ok,
}

impl Memory {
    fn run_instruction(&mut self) -> RunState {
        if self.ip as usize == self.instructions.len() {
            return RunState::Finished;
        }
        if self.visited[self.ip as usize] {
            RunState::Looped
        } else {
            self.visited[self.ip as usize] = true;
            let ins = self.instructions[self.ip as usize];
            match ins {
                InstructionSet::NOP(_value) => {}
                InstructionSet::ACC(value) => self.accumulator += value,
                InstructionSet::JMP(value) => self.ip += value - 1,
            }
            self.ip += 1;
            RunState::Ok
        }
    }

    fn run(&mut self) -> Option<isize> {
        loop {
            match self.run_instruction() {
                RunState::Finished => return Some(self.accumulator),
                RunState::Looped => return None,
                RunState::Ok => {}
            }
        }
    }

    fn apply_change(&mut self, pos: usize) -> bool {
        let ins = &mut self.instructions[pos];
        match ins {
            InstructionSet::ACC(_) => false,
            InstructionSet::NOP(value) => {
                *ins = InstructionSet::JMP(*value);
                true
            }
            InstructionSet::JMP(value) => {
                *ins = InstructionSet::NOP(*value);
                true
            }
        }
    }

    fn run_changes(&mut self) -> isize {
        let mut change = 0;
        loop {
            if self.apply_change(change) {
                if let Some(acc) = self.run() {
                    return acc;
                }
                self.accumulator = 0;
                self.ip = 0;
                self.visited = vec![false; self.instructions.len()];
            }
            self.apply_change(change);
            change += 1;
        }
    }

    fn init(input: &str) -> Self {
        let lines = input.lines();
        let mut memory = Memory {
            accumulator: 0,
            visited: Vec::new(),
            ip: 0,
            instructions: Vec::with_capacity(lines.size_hint().0),
        };
        for ins in lines {
            memory.instructions.push(InstructionSet::parse(ins));
        }
        memory.visited = vec![false; memory.instructions.len()];
        memory
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_program = r#"nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"#;
        assert_eq!(run(small_program), 8)
    }
}
