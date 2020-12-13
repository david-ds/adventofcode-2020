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
    let mut lines = input.lines();
    let mut buses = Vec::new();
    let mut n = 1;
    for (i, s) in lines.nth(1).unwrap_or("").split(',').enumerate() {
        if let Ok(id) = s.parse() {
            n *= id;
            buses.push((-(i as isize), id));
        }
    }
    solve(buses, n)
}

fn solve(buses: Vec<(isize, isize)>, n: isize) -> isize {
    let mut x = 0;
    for (i, id) in buses {
        let (pgcd, u, _v) = euclid(n / id, id);
        // 1 = -35 + 12*3
        if pgcd != 1 {
            panic!()
        }
        x += i * u * (n / id);
    }
    ((x % n) + n) % n
}

fn euclid(a: isize, b: isize) -> (isize, isize, isize) {
    if b == 0 {
        (a, 1, 0)
    } else {
        let (pgcd, u, v) = euclid(b, a % b);
        (pgcd, v, u - (a / b) * v)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn euclid_test() {
        assert_eq!(euclid(35, 3), (1, 2, -23))
    }

    #[test]
    fn solve_test() {
        assert_eq!(solve(vec![(2, 3), (3, 5), (2, 7)], 3 * 5 * 7), 23);
    }

    #[test]
    fn run_test() {
        assert_eq!(
            run("
7,13,x,x,59,x,31,19"),
            1068781
        );
        assert_eq!(
            run("
17,x,13,19"),
            3417
        );
        assert_eq!(
            run("
67,7,59,61"),
            754018
        );
        assert_eq!(
            run("
67,x,7,59,61"),
            779210
        );
        assert_eq!(
            run("
67,7, x,59,61"),
            1261476
        );
        assert_eq!(
            run("
1789,37,47,1889"),
            1202161486
        );
    }
}
