use std::env::args;
use std::time::Instant;
use std::vec::Vec;
fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut mem: Vec<Option<usize>> = vec![None; 2020];
    let mut last_spoken = 0;
    let mut number_spoken = 0;
    for (i, x) in input
        .split(',')
        .enumerate()
        .map(|(i, x)| (i, x.parse::<usize>().unwrap()))
    {
        if number_spoken >= 1 {
            mem[last_spoken] = Some(i);
        };
        last_spoken = x;
        number_spoken += 1;
    }
    for i in (number_spoken)..2020 {
        let prev_spoken = last_spoken;
        match mem[prev_spoken] {
            None => {
                last_spoken = 0;
            }
            Some(v) => {
                last_spoken = i - v;
            }
        }
        mem[prev_spoken] = Some(i);
    }
    last_spoken
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn giltho_d15_p2_1() {
        assert_eq!(run("0,3,6"), 175594)
    }
    #[test]
    fn giltho_d15_p2_2() {
        assert_eq!(run("1,3,2"), 2578)
    }
    #[test]
    fn giltho_d15_p2_3() {
        assert_eq!(run("2,1,3"), 3544142)
    }
    #[test]
    fn giltho_d15_p2_4() {
        assert_eq!(run("1,2,3"), 261214)
    }
}
