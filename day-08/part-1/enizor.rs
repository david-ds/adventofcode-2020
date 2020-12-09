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
    Memory::init(input).run()
}

#[derive(Debug, Clone, Copy)]
enum InstructionSet {
    NOP,
    ACC(isize),
    JMP(isize),
}

impl Default for InstructionSet {
    fn default() -> Self {
        InstructionSet::NOP
    }
}

impl InstructionSet {
    fn parse(input: &str) -> Self {
        match &input[..3] {
            "nop" => Self::NOP,
            "acc" => Self::ACC(input[4..].parse().expect("cannot parse ACC value")),
            "jmp" => Self::JMP(input[4..].parse().expect("cannot parse JMP value")),
            _ => Self::NOP,
        }
    }
}

#[derive(Default, Clone, Copy, Debug)]
struct InstructionMemory {
    instruction: InstructionSet,
    visited: bool,
}

#[derive(Default)]
struct Memory {
    accumulator: isize,
    ip: isize,
    instructions: Vec<InstructionMemory>,
}

impl Memory {
    fn run_instruction(&mut self) -> Result<(), ()> {
        if self.ip as usize >= self.instructions.len() {
            return Err(());
        }
        let todo = &mut self.instructions[self.ip as usize];
        if todo.visited {
            Err(())
        } else {
            match todo.instruction {
                InstructionSet::NOP => {}
                InstructionSet::ACC(value) => self.accumulator += value,
                InstructionSet::JMP(value) => self.ip += value - 1,
            }
            self.ip += 1;
            todo.visited = true;
            Ok(())
        }
    }

    fn run(&mut self) -> isize {
        while self.run_instruction().is_ok() {}
        self.accumulator
    }

    fn init(input: &str) -> Self {
        let lines = input.lines();
        let mut memory = Memory {
            accumulator: 0,
            ip: 0,
            instructions: Vec::with_capacity(lines.size_hint().0),
        };
        for ins in lines {
            memory.instructions.push(InstructionMemory {
                visited: false,
                instruction: InstructionSet::parse(ins),
            })
        }
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
        assert_eq!(run(small_program), 5)
    }
}
