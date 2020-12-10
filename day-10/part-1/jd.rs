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
    let mut numbers: Vec<usize> = input
        .lines()
        .map(|line| line.parse::<usize>().unwrap())
        .collect();
    numbers.sort_unstable();
    numbers.insert(0, 0);
    numbers.push(numbers.last().unwrap() + 3);

    let mut one_gap = 0;
    let mut three_gap = 0;

    for i in 1..numbers.len() {
        let diff = numbers[i] - numbers[i - 1];
        if diff == 1 {
            one_gap += 1;
        } else if diff == 3 {
            three_gap += 1;
        }
    }

    one_gap * three_gap
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3";
        assert_eq!(run(input), 220)
    }
}
