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
    let mut ship = Ship::new();

    input
        .lines()
        .map(|line| {
            (
                line.chars().next().unwrap(),
                line[1..].parse::<isize>().unwrap(),
            )
        })
        .for_each(|instruction| ship.next(instruction));

    ship.pos.0.abs() + ship.pos.1.abs()
}

struct Ship {
    pos: (isize, isize),
    orientation: (isize, isize),
}

impl Ship {
    fn new() -> Self {
        Self {
            pos: (0, 0),
            orientation: (1, 0),
        }
    }

    fn next(&mut self, instruction: (char, isize)) {
        match instruction.0 {
            'N' => {
                self.pos.1 += instruction.1;
            }
            'S' => {
                self.pos.1 -= instruction.1;
            }
            'W' => {
                self.pos.0 -= instruction.1;
            }
            'E' => {
                self.pos.0 += instruction.1;
            }
            'L' => {
                self.orientation = rotate(-instruction.1, self.orientation);
            }
            'R' => {
                self.orientation = rotate(instruction.1, self.orientation);
            }
            'F' => {
                self.pos.0 += instruction.1 * self.orientation.0;
                self.pos.1 += instruction.1 * self.orientation.1;
            }
            _ => {}
        };
    }
}

fn rotate(angle: isize, point: (isize, isize)) -> (isize, isize) {
    match angle {
        90 | -270 => (point.1, -point.0),
        180 | -180 => (-point.0, -point.1),
        270 | -90 => (-point.1, point.0),
        _ => point,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "F10
N3
F7
R90
F11";
        assert_eq!(run(input), 25)
    }
}
