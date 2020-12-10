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

    let mut combinations: Vec<usize> = vec![0; numbers.len()];
    let n = combinations.len();
    combinations[n - 1] = 1;

    (0..n - 1).rev().for_each(|i| {
        numbers[i..]
            .iter()
            .enumerate()
            .take_while(|(j, _)| numbers[*j + i] as isize - numbers[i] as isize <= 3)
            .for_each(|(j, _)| combinations[i] += combinations[j + i]);
    });

    combinations[0]
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
        assert_eq!(run(input), 19208)
    }
}
