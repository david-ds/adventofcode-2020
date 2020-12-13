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
    let mut lines = input.lines();
    let start: usize = lines.next().unwrap().parse().unwrap();
    let bus: (usize, usize) = lines
        .next()
        .unwrap_or("")
        .split(',')
        .filter_map(|s| s.parse().ok().map(|t| (t - (start % t), t)))
        .min()
        .unwrap();
    bus.0 * bus.1
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("939
7,13,x,x,59,x,31,19"),
            295
        )
    }
}
