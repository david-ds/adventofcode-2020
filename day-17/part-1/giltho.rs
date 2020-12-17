use std::env::args;
use std::time::Instant;

mod automata {
    use std::cmp::{max, min};
    use std::collections::{HashMap, HashSet};
    use std::fmt;
    pub struct AC3D {
        use_state_a: bool,
        state_a: HashSet<(i8, i8, i8)>,
        state_b: HashSet<(i8, i8, i8)>,
        neighbours: HashMap<(i8, i8, i8), i8>,
    }
    impl fmt::Display for AC3D {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            let mut xymin = i8::MAX;
            let mut zmin = i8::MAX;
            let mut xymax = i8::MIN;
            let mut zmax = i8::MIN;
            let state = if self.use_state_a {
                &self.state_a
            } else {
                &self.state_b
            };
            for &(x, y, z) in state {
                xymin = min(xymin, min(x, y));
                zmin = min(zmin, z);
                xymax = max(xymax, max(x, y));
                zmax = max(zmax, z);
            }
            for z in zmin..zmax + 1 {
                write!(f, "\nz = {}", z)?;
                for x in xymin..xymax + 1 {
                    write!(f, "\n")?;
                    for y in xymin..xymax + 1 {
                        if state.contains(&(x, y, z)) {
                            write!(f, "#")?
                        } else {
                            write!(f, ".")?
                        }
                    }
                }
            }
            Ok(())
        }
    }

    impl AC3D {
        pub fn new() -> Self {
            Self {
                use_state_a: true,
                state_a: HashSet::with_capacity(1000),
                state_b: HashSet::with_capacity(1000),
                neighbours: HashMap::with_capacity(1000),
            }
        }
        fn swap_state(&mut self) {
            self.use_state_a = !self.use_state_a
        }
        fn compute_neighbours(&mut self) {
            self.neighbours.clear();
            let cur_state = if self.use_state_a {
                &mut self.state_a
            } else {
                &mut self.state_b
            };
            for (a, b, c) in cur_state.iter() {
                for x in a - 1..a + 2 {
                    for y in b - 1..b + 2 {
                        for z in c - 1..c + 2 {
                            if (a, b, c) != (&x, &y, &z) {
                                let mut changed = false;
                                match self.neighbours.get_mut(&(x, y, z)) {
                                    None => (),
                                    Some(p) => {
                                        *p = (*p) + 1;
                                        changed = true
                                    }
                                }
                                if !changed {
                                    self.neighbours.insert((x, y, z), 1);
                                }
                            }
                        }
                    }
                }
            }
        }
        fn compute_state(&mut self) {
            self.swap_state();
            let (cur_state, other_state) = if self.use_state_a {
                (&mut self.state_a, &mut self.state_b)
            } else {
                (&mut self.state_b, &mut self.state_a)
            };
            cur_state.clear();
            for (&key, &val) in self.neighbours.iter() {
                if other_state.contains(&key) {
                    if val == 2 || val == 3 {
                        cur_state.insert(key);
                    }
                } else {
                    if val == 3 {
                        cur_state.insert(key);
                    }
                }
            }
        }
        pub fn step(&mut self) {
            self.compute_neighbours();
            self.compute_state()
        }
        pub fn n_step(&mut self, n: u8) {
            for _ in 0..n {
                self.step()
            }
        }
        pub fn count_alive(&self) -> usize {
            if self.use_state_a {
                self.state_a.len()
            } else {
                self.state_b.len()
            }
        }
        pub fn set_alive(&mut self, x: i8, y: i8, z: i8) {
            let state = if self.use_state_a {
                &mut self.state_a
            } else {
                &mut self.state_b
            };
            state.insert((x, y, z));
        }
    }
}

use automata::AC3D;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut auto = AC3D::new();
    let mut x = 0;
    let mut y = 0;
    for c in input.chars() {
        match c {
            '#' => {
                auto.set_alive(x, y, 0);
                y += 1
            }
            '\n' => {
                x += 1;
                y = 0
            }
            '.' => y += 1,
            _ => panic!("Wrong input"),
        }
    }
    auto.n_step(6u8);
    auto.count_alive()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run(r#".#.
..#
###"#),
            112
        )
    }
}
