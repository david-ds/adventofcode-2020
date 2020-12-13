use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> isize {
    let constraints: Vec<(isize, isize)> = input
        .lines()
        .nth(1)
        .unwrap()
        .split(',')
        .enumerate()
        .filter(|(_, item)| *item != "x")
        .map(|(idx, id)| (idx as isize, id.parse::<isize>().unwrap()))
        .collect();

    let n = constraints.iter().fold(1, |acc, (_, id)| acc * id);

    let t = constraints.iter().fold(0, |acc, (idx, id)| {
        acc - idx * inverse(n / id, *id) * n / id
    }) % n;

    if t < 0 {
        t + n
    } else {
        t
    }
}

fn inverse(x: isize, n: isize) -> isize {
    bezout(x, n).1
}

fn bezout(a: isize, b: isize) -> (isize, isize, isize) {
    if b == 0 {
        (a, 1, 0)
    } else {
        let (pgcd, u, v) = bezout(b, a % b);
        (pgcd, v, u - (a / b) * v)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(run("\n7,13,x,x,59,x,31,19"), 1068781);

        assert_eq!(run("\n17,x,13,19"), 3417);

        assert_eq!(run("\n67,7,59,61"), 754018);

        assert_eq!(run("\n67,x,7,59,61"), 779210);

        assert_eq!(run("\n67,7,x,59,61"), 1261476);

        assert_eq!(run("\n1789,37,47,1889"), 1202161486);
    }
}
