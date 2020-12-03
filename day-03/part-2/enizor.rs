use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

struct Toboggan<'a> {
    slope_x: usize,
    slope_y: usize,
    width: usize,
    pos_x: usize,
    pos_y: usize,
    chars: &'a [u8],
}

impl<'a> Toboggan<'a> {
    fn parse_input(s: &'a str, width: usize, slope_x: usize, slope_y: usize) -> Self {
        debug_assert!(width >= slope_x);
        Toboggan {
            slope_x,
            slope_y,
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
        self.pos_x = (self.pos_x + self.slope_x) % self.width;
        self.pos_y += self.slope_y;
        self.chars.get(self.pos_x + self.pos_y * (self.width + 1))
    }
}

fn run(input: &str) -> isize {
    let width = input.find('\n').expect("No EOL!");
    [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        .iter()
        .map(|&(x, y)| {
            Toboggan::parse_input(input, width, x, y)
                .filter(|&&c| c == b'#')
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
