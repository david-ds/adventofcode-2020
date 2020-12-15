use std::time::Instant;
use std::{collections::HashMap, env::args};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"), 30000000);
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

const CACHE_SIZE: usize = 2048 * 64 * 8;
fn run(input: &str, max: u32) -> u32 {
    let mut memory = HashMap::new();
    let mut cache = [0u32; CACHE_SIZE];
    let mut i = 0;
    let mut last_spoken = 0;
    for s in input.split(',') {
        i += 1;
        let new_nb: u32 = s.parse().expect("cannot parse input");
        if (new_nb as usize) < CACHE_SIZE {
            cache[new_nb as usize] = i;
        } else {
            memory.insert(new_nb, i);
        };
        last_spoken = new_nb;
    }
    while i < max {
        let new_nb = if (last_spoken as usize) < CACHE_SIZE {
            let v = match cache[last_spoken as usize] {
                0 => 0,
                x => i - x,
            };
            cache[last_spoken as usize] = i;
            v
        } else {
            let v = match memory.get(&last_spoken) {
                None => 0,
                Some(&x) => i - x,
            };
            memory.insert(last_spoken, i);
            v
        };
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
        assert_eq!(run("0,3,6", 30000000), 175594)
    }
}
