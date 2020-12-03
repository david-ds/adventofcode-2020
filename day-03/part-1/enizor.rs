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
struct Toboggan<T> {
    width: usize,
    counter: usize,
    chars: T,
}

fn parse_input<'a>(s: &'a str) -> Toboggan<impl Iterator<Item = char> + 'a> {
    let width = s.find('\n').expect("No EOL!");
    debug_assert!(width >= SLOPE_X);
    let chars = s.chars().filter(|&c| c != '\n').skip(1);

    Toboggan {
        width,
        counter: 0,
        chars,
    }
}
impl<T: Iterator<Item = char>> Iterator for Toboggan<T> {
    type Item = char;

    fn next(&mut self) -> Option<Self::Item> {
        let vertical =
            SLOPE_Y + (self.counter / self.width) - ((self.counter + SLOPE_X) / self.width);
        self.counter += SLOPE_X;
        self.chars.nth(SLOPE_X + vertical * self.width - 1)
    }
}

fn run(input: &str) -> isize {
    parse_input(input).filter(|&c| c == '#').count() as isize
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
