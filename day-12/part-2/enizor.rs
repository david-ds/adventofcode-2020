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
    let mut pos = Waypoint::new();
    let mut ship = Ship::default();
    for ins in input.lines() {
        pos.consume_inst(ins, &mut ship);
    }
    ship.distance()
}

#[derive(Default)]
struct Ship {
    east: isize,
    north: isize,
}

impl Ship {
    fn distance(&self) -> isize {
        self.east.abs() + self.north.abs()
    }
}
struct Waypoint {
    east: isize,
    north: isize,
}

impl Waypoint {
    fn new() -> Self {
        Self { east: 10, north: 1 }
    }

    fn consume_inst(&mut self, ins: &str, ship: &mut Ship) {
        let value: isize = ins[1..].parse().expect("cannot parse value");
        let tmp = self.east;
        match ins.as_bytes()[0] {
            b'N' => self.north += value,
            b'S' => self.north -= value,
            b'E' => self.east += value,
            b'W' => self.east -= value,
            b'L' => match value {
                90 => {
                    self.east = -self.north;
                    self.north = tmp;
                }
                180 => {
                    self.north *= -1;
                    self.east *= -1;
                }
                270 => {
                    self.east = self.north;
                    self.north = -tmp;
                }
                _ => panic!(),
            },
            b'R' => match value {
                90 => {
                    self.east = self.north;
                    self.north = -tmp;
                }
                180 => {
                    self.north *= -1;
                    self.east *= -1;
                }
                270 => {
                    self.east = -self.north;
                    self.north = tmp;
                }
                _ => panic!(),
            },
            b'F' => {
                ship.east += value * self.east;
                ship.north += value * self.north;
            }
            _ => panic!(),
        }
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
            286
        )
    }
}
