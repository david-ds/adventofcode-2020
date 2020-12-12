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
    orientation: char,
}

impl Ship {
    fn new() -> Self {
        Self {
            x: 0,
            y: 0,
            orientation: 'E',
        }
    }

    fn next(&mut self, instruction: (char, isize)) {
        match instruction.0 {
            'N' => {
                self.y += instruction.1;
            }
            'S' => {
                self.y -= instruction.1;
            }
            'W' => {
                self.x -= instruction.1;
            }
            'E' => {
                self.x += instruction.1;
            }
            'F' => {
                self.forward(instruction.1);
            }
            'L' => {
                self.rotate(false, instruction.1);
            }
            'R' => {
                self.rotate(true, instruction.1);
            }
            _ => {}
        };
    }

    fn forward(&mut self, moves: isize) {
        match self.orientation {
            'N' => {
                self.y += moves;
            }
            'S' => {
                self.y -= moves;
            }
            'W' => {
                self.x -= moves;
            }
            'E' => {
                self.x += moves;
            }
            _ => {}
        }
    }

    fn rotate(&mut self, direction: bool, degrees: isize) {
        if direction {
            match self.orientation {
                'N' => match degrees {
                    90 => {
                        self.orientation = 'E';
                    }
                    180 => {
                        self.orientation = 'S';
                    }
                    270 => {
                        self.orientation = 'W';
                    }
                    _ => {}
                },
                'S' => match degrees {
                    90 => {
                        self.orientation = 'W';
                    }
                    180 => {
                        self.orientation = 'N';
                    }
                    270 => {
                        self.orientation = 'E';
                    }
                    _ => {}
                },
                'W' => match degrees {
                    90 => {
                        self.orientation = 'N';
                    }
                    180 => {
                        self.orientation = 'E';
                    }
                    270 => {
                        self.orientation = 'S';
                    }
                    _ => {}
                },
                'E' => match degrees {
                    90 => {
                        self.orientation = 'S';
                    }
                    180 => {
                        self.orientation = 'W';
                    }
                    270 => {
                        self.orientation = 'N';
                    }
                    _ => {}
                },
                _ => {}
            }
        } else {
            match self.orientation {
                'N' => match degrees {
                    90 => {
                        self.orientation = 'W';
                    }
                    180 => {
                        self.orientation = 'S';
                    }
                    270 => {
                        self.orientation = 'E';
                    }
                    _ => {}
                },
                'S' => match degrees {
                    90 => {
                        self.orientation = 'E';
                    }
                    180 => {
                        self.orientation = 'N';
                    }
                    270 => {
                        self.orientation = 'W';
                    }
                    _ => {}
                },
                'W' => match degrees {
                    90 => {
                        self.orientation = 'S';
                    }
                    180 => {
                        self.orientation = 'E';
                    }
                    270 => {
                        self.orientation = 'N';
                    }
                    _ => {}
                },
                'E' => match degrees {
                    90 => {
                        self.orientation = 'N';
                    }
                    180 => {
                        self.orientation = 'W';
                    }
                    270 => {
                        self.orientation = 'S';
                    }
                    _ => {}
                },
                _ => {}
            }
        }
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
