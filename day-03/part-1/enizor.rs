use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const SLOPE_X: usize = 3;
const SLOPE_Y: usize = 1;
struct Toboggan<'a> {
    width: usize,
    pos_x: usize,
    pos_y: usize,
    chars: &'a [u8],
}

impl<'a> Toboggan<'a> {
    fn parse_input(s: &'a str) -> Self {
        let width = s.find('\n').expect("No EOL!");
        debug_assert!(width >= SLOPE_X);

        Toboggan {
            width,
            pos_x: 0,
            pos_y: 0,
            chars: s.as_bytes(),
        }
    }
}
impl<'a> Iterator for Toboggan<'a> {
    type Item = &'a u8;

    fn next(&mut self) -> Option<Self::Item> {
        self.pos_x = (self.pos_x + SLOPE_X) % self.width;
        self.pos_y += SLOPE_Y;
        self.chars.get(self.pos_x + self.pos_y * (self.width + 1))
    }
}

fn run(input: &str) -> isize {
    Toboggan::parse_input(input).filter(|&&c| c == b'#').count() as isize
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_input = r#"..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"#;
        assert_eq!(run(small_input), 7)
    }
}
