use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"), 2020);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str, max: u16) -> u16 {
    let mut memory = [0u16; 2020];
    let mut i = 0;
    let mut last_spoken = 0;
    for s in input.split(',') {
        i += 1;
        let new_nb: u16 = s.parse().expect("cannot parse input");
        memory[new_nb as usize] = i;
        last_spoken = new_nb;
    }
    while i < max {
        let new_nb = match memory[last_spoken as usize] {
            0 => 0,
            x => i - x,
        };
        memory[last_spoken as usize] = i;
        i += 1;
        last_spoken = new_nb;
    }
    last_spoken
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("0,3,6", 9), 4)
    }
}
