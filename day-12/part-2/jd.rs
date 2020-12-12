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

    ship.x.abs() + ship.y.abs()
}

struct Ship {
    x: isize,
    y: isize,
    wx: isize,
    wy: isize,
}

impl Ship {
    fn new() -> Self {
        Self {
            x: 0,
            y: 0,
            wx: 10,
            wy: 1,
        }
    }

    fn next(&mut self, instruction: (char, isize)) {
        match instruction.0 {
            'N' => {
                self.wy += instruction.1;
            }
            'S' => {
                self.wy -= instruction.1;
            }
            'W' => {
                self.wx -= instruction.1;
            }
            'E' => {
                self.wx += instruction.1;
            }
            'L' => {
                let (new_wx, new_wy) = rotate(-instruction.1, (self.wx, self.wy));
                self.wx = new_wx;
                self.wy = new_wy;
            }
            'R' => {
                let (new_wx, new_wy) = rotate(instruction.1, (self.wx, self.wy));
                self.wx = new_wx;
                self.wy = new_wy;
            }
            'F' => {
                self.x += instruction.1 * self.wx;
                self.y += instruction.1 * self.wy;
            }
            _ => {}
        }
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
        assert_eq!(run(input), 286)
    }
}
