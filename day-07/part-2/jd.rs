use std::env::args;
use std::time::Instant;

use std::collections::HashMap;

const SEPARATOR: &str = " bags contain ";
const TARGET: &str = "shiny gold";
const NULL: &str = "no other bags";

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> usize {
    let mut graph = Graph::from(input);
    let bag_id = graph.id(TARGET);
    graph.count(bag_id) - 1
}

#[derive(Default, Debug)]
struct Graph<'a> {
    ids: HashMap<&'a str, usize>,
    next_given_id: usize,
    nodes: Vec<Node>,
}

#[derive(Default, Debug)]
struct Node {
    children: Vec<(usize, usize)>,
}

impl<'a> Graph<'a> {
    fn from(input: &'a str) -> Self {
        let mut graph = Graph::default();

        input.lines().for_each(|line| graph.ingest_line(line));

        graph
    }

    fn ingest_line(&mut self, line: &'a str) {
        let line = &line[..line.len() - 1]; // get rid of final dot.
        let separator_index = line.find(SEPARATOR).unwrap();
        let container_id = self.id(&line[..separator_index]);

        line[separator_index + SEPARATOR.len()..]
            .split(", ")
            .filter(|bag| *bag != NULL)
            .for_each(|bag| {
                let bag = bag[..bag.len() - 4].trim();
                let start_index = bag.find(' ').unwrap();
                let bag_id = self.id(&bag[start_index + 1..]);

                self.nodes[container_id]
                    .children
                    .push((bag_id, bag[..start_index].parse::<usize>().unwrap()));
            });
    }

    fn id(&mut self, bag: &'a str) -> usize {
        if let Some(id) = self.ids.get(bag) {
            *id
        } else {
            let current_id = self.next_given_id;
            self.nodes.push(Node::default());
            self.ids.insert(bag, current_id);
            self.next_given_id += 1;
            current_id
        }
    }

    fn count(&self, id: usize) -> usize {
        self.nodes[id]
            .children
            .iter()
            .fold(1, |acc, (child, count)| acc + count * self.count(*child))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        let input = "light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.";

        assert_eq!(run(input), 32)
    }
}
