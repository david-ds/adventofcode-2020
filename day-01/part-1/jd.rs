use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> u64 {
    find_couple_product(&mut parse_input(input), 2020)
}

fn parse_input(input: &str) -> Vec<u64> {
    input
        .lines()
        .map(|line| line.parse::<u64>().expect("could not parse uint"))
        .collect()
}

fn find_couple_product(numbers: &mut [u64], goal: u64) -> u64 {
    // This enables O(log n) search using dichotomy.
    numbers.sort_unstable();

    for (index, entry) in numbers.iter().enumerate() {
        let remainder = goal.checked_sub(*entry);

        // Since the list has only positive numbers we can skip negative remainders
        if let Some(remainder) = remainder {
            if dichotomy(&numbers[index + 1..], remainder).is_some() {
                return entry * remainder;
            }
        }
    }

    0
}

fn dichotomy<T: PartialEq + PartialOrd>(array: &[T], searched: T) -> Option<usize> {
    if array.is_empty() {
        return None;
    }

    let middle = array.len() / 2;

    if array[middle] == searched {
        Some(middle)
    } else if array[middle] > searched {
        dichotomy(&array[..middle], searched)
    } else if let Some(i) = dichotomy(&array[middle + 1..], searched) {
        Some(middle + i + 1)
    } else {
        None
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "1721
979
366
299
675
1456";
        assert_eq!(run(input), 514579)
    }
}
