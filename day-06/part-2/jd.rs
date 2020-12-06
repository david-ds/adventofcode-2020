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
        .split("\n\n")
        .map(|group| {
            let mut map: [usize; 26] = [0; 26];

            let n = group.split('\n').fold(0, |count, person| {
                person.as_bytes().iter().for_each(|c| {
                    map[(c - 97) as usize] += 1;
                });

                count + 1
            });

            map.iter().filter(|t| **t == n).count()
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "abc

a
b
c

ab
ac

a
a
a
a

b";
        assert_eq!(run(input), 6)
    }
}
