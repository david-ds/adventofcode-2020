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
    let mut pos = Pos::new();
    for ins in input.lines() {
        pos.consume_inst(ins);
    }
    pos.distance()
}

struct Pos {
    east: isize,
    north: isize,
    direction: isize,
}

impl Pos {
    fn new() -> Self {
        Self {
            east: 0,
            north: 0,
            direction: 0,
        }
    }

    fn consume_inst(&mut self, ins: &str) {
        let value: isize = ins[1..].parse().expect("cannot parse value");
        match ins.as_bytes()[0] {
            b'N' => self.north += value,
            b'S' => self.north -= value,
            b'E' => self.east += value,
            b'W' => self.east -= value,
            b'L' => self.direction += value,
            b'R' => self.direction -= value,
            b'F' => match self.direction % 360 {
                0 => self.east += value,
                90 | -270 => self.north += value,
                180 | -180 => self.east -= value,
                270 | -90 => self.north -= value,
                _ => panic!(),
            },
            _ => panic!(),
        }
    }

    fn distance(&self) -> isize {
        self.east.abs() + self.north.abs()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("F10
N3
F7
R90
F11"),
            25
        )
    }
}
