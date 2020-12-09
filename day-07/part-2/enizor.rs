use std::time::Instant;
use std::{collections::HashMap, env::args};
fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut bags = BagList::default();
    for rule in input.lines() {
        if let Some(bag) = Bag::parse(rule) {
            bags.add_bag(bag);
        }
    }
    // bags.print_names();
    bags.propagate_ending()
}

#[derive(Default, Debug, Clone)]
struct Bag<'a> {
    name: &'a str,
    children: Vec<(usize, &'a str)>,
}

impl<'a> Bag<'a> {
    fn parse(input: &'a str) -> Option<Self> {
        let cur_name = input.find(" bags").expect("Cannot parse bag name");
        let name = &input[..cur_name];
        if input.contains("no other") {
            return None;
        }
        let mut start_cur = cur_name + 14;
        let mut color_cur = start_cur
            + 2
            + input[start_cur + 1..]
                .find(|c: char| !c.is_ascii_digit())
                .unwrap();
        let mut end_cur: usize;
        let mut number: usize;
        let mut children = Vec::new();
        while let Some(end_offset) = input[start_cur..].find(" bag") {
            number = input[start_cur..color_cur - 1].parse().unwrap();
            end_cur = start_cur + end_offset;
            let child = &input[color_cur..end_cur];
            children.push((number, child));
            if let Some(next_start) = input[end_cur..].find(", ") {
                start_cur = end_cur + next_start + 2;
                color_cur = start_cur
                    + 2
                    + input[start_cur + 1..]
                        .find(|c: char| !c.is_ascii_digit())
                        .unwrap();
            } else {
                break;
            }
        }
        Some(Bag { name, children })
    }
}

#[derive(Default)]
struct BagList<'a> {
    bags: HashMap<&'a str, Vec<(usize, &'a str)>>,
}

impl<'a> BagList<'a> {
    fn add_bag(&mut self, new_bag: Bag<'a>) {
        // self.propagate_children(&mut new_bag);
        // let name = new_bag.name.clone();
        // let should_propagate = new_bag.can_hold_shiny_gold;
        self.bags.insert(new_bag.name, new_bag.children);
    }

    fn propagate(&self, bag: &str) -> usize {
        let mut total_children = 0;
        if let Some(children) = self.bags.get(bag) {
            for (nb, child) in children {
                total_children += nb * (1 + self.propagate(&child));
            }
        }
        total_children
    }

    fn propagate_ending(&mut self) -> usize {
        let root = "shiny gold";
        self.propagate(root)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_example = r#"light red bags contain 17 bright white bag, 282 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."#;
        assert_eq!(run(small_example), 32);
        let second_example = r#"shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."#;
        assert_eq!(run(second_example), 126);
    }
}
