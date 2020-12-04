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
    find_couple_product(&mut parse_input(input), 2020) as isize
}

fn parse_input(input: &str) -> Vec<u64> {
    input
        .split("\n")
        .map(|line| line.parse::<u64>().expect("could not parse uint"))
        .collect()
}

fn find_couple_product(numbers: &mut [u64], goal: u64) -> u64 {
    // This enables O(log n) search using dichotomy.
    numbers.sort();

    for (index, entry) in numbers.iter().enumerate() {
        let remainder = goal.checked_sub(*entry);

        // Since the list has only positive numbers we can skip negative remainders
        if let Some(remainder) = remainder {
            if let Some(_) = dichotomy(&numbers[index + 1..], remainder) {
                return entry * remainder;
            }
        }
    }

    0
}

pub fn dichotomy<T: PartialEq + PartialOrd>(array: &[T], searched: T) -> Option<usize> {
    if array.is_empty() {
        return None;
    }

    let middle = array.len() / 2;

    if array[middle] == searched {
        return Some(middle);
    } else if array[middle] > searched {
        return dichotomy(&array[..middle], searched);
    } else {
        return dichotomy(&array[middle + 1..], searched);
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
