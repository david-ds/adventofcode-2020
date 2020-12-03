use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

struct Toboggan<T> {
    slope_x: usize,
    slope_y: usize,
    width: usize,
    counter: usize,
    chars: T,
}

fn parse_input<'a>(
    s: &'a str,
    width: usize,
    slope_x: usize,
    slope_y: usize,
) -> Toboggan<impl Iterator<Item = char> + 'a> {
    debug_assert!(width >= slope_x);
    let chars = s.chars().filter(|&c| c != '\n').skip(1);

    Toboggan {
        slope_x,
        slope_y,
        width,
        counter: 0,
        chars,
    }
}
impl<T: Iterator<Item = char>> Iterator for Toboggan<T> {
    type Item = char;

    fn next(&mut self) -> Option<Self::Item> {
        let vertical = self.slope_y + (self.counter / self.width)
            - ((self.counter + self.slope_x) / self.width);
        self.counter += self.slope_x;
        self.chars.nth(self.slope_x + vertical * self.width - 1)
    }
}

fn run(input: &str) -> isize {
    let width = input.find('\n').expect("No EOL!");
    [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        .iter()
        .map(|&(x, y)| {
            parse_input(input, width, x, y)
                .filter(|&c| c == '#')
                .count()
        })
        .product::<usize>() as isize
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
        assert_eq!(run(small_input), 336)
    }
}
