use std::time::Instant;
use std::{collections::HashSet, env::args};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> isize {
    const GOAL: isize = 2020;
    let map: HashSet<isize> = input
        .split_whitespace()
        .map(|x| x.parse().expect("cannot parse input"))
        .collect();
    map.iter()
        .find_map(|&value1| map.get(&(GOAL - value1)).map(|&value2| value1 * value2))
        .unwrap_or(0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_input = "1721
979
366
299
675
1456";
        assert_eq!(run(small_input), 514579)
    }
}
