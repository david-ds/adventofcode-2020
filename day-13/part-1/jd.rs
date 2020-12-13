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
    let start = lines.next().unwrap().parse::<usize>().unwrap();

    let (closest_id, waiting_time) = lines
        .next()
        .unwrap()
        .split(',')
        .filter(|&item| item != "x")
        .map(|id| id.parse::<usize>().unwrap())
        .map(|id| (id, ((start / id) + (start % id != 0) as usize) * id - start))
        .min_by(|x, y| x.1.cmp(&y.1))
        .unwrap();

    closest_id * waiting_time
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "939
7,13,x,x,59,x,31,19";

        assert_eq!(run(input), 295)
    }
}
