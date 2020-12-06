use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    input
        .lines()
        .map(|line| {
            let (row, col) = line.chars().fold((0, 0), |(row, col), c| match c {
                'F' => (row << 1, col),
                'B' => ((row << 1) + 1, col),
                'R' => (row, (col << 1) + 1),
                'L' => (row, col << 1),
                _ => (row, col),
            });
            8 * row + col
        })
        .max()
        .unwrap_or(0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL";

        assert_eq!(run(input), 820)
    }
}
