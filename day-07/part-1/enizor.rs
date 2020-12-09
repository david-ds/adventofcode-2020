use std::time::Instant;
use std::{
    collections::{HashMap, HashSet},
    env::args,
};
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
    children: Vec<&'a str>,
}

impl<'a> Bag<'a> {
    fn parse(input: &'a str) -> Option<Self> {
        let cur_name = input.find(" bags").expect("Cannot parse bag name");
        let name = &input[..cur_name];
        let mut start_cur = cur_name + 14;
        start_cur += 1 + input[start_cur..]
            .find(|c: char| !c.is_ascii_digit())
            .unwrap();
        let mut end_cur: usize;
        if input[start_cur..].contains("other") {
            return None;
        }
        let mut children = Vec::new();
        while let Some(end_offset) = input[start_cur..].find(" bag") {
            end_cur = start_cur + end_offset;
            let child = &input[start_cur..end_cur];
            children.push(child);
            if let Some(next_start) = input[end_cur..].find(", ") {
                start_cur = end_cur
                    + next_start
                    + 3
                    + input[end_cur + next_start + 2..]
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
    parents: HashMap<&'a str, Vec<&'a str>>,
}

impl<'a> BagList<'a> {
    fn add_bag<'b: 'a>(&mut self, new_bag: Bag<'b>) {
        for child in new_bag.children {
            let var_name = self.parents.entry(child).or_default();
            var_name.push(new_bag.name);
        }
    }

    fn propagate<'b>(&'a self, bag: &'a str, set: &'b mut HashSet<&'a str>) {
        if let Some(parents) = self.parents.get(bag) {
            for parent in parents {
                if set.insert(parent.as_ref()) {
                    self.propagate(parent.as_ref(), set);
                }
            }
        }
    }

    fn propagate_ending(&mut self) -> usize {
        let mut holders = HashSet::new();
        let root = "shiny gold";
        self.propagate(root, &mut holders);
        holders.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let small_example = r#"light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 32 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 1232 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 124 dotted black bags.
vibrant plum bags contain 315 faded blue bags, 6 dotted black bags.
shiny red bags contain 1 bright white bag, 2 muted yellow bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."#;
        assert_eq!(run(small_example), 5)
    }
}
