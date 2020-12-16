use std::cmp::{max, min};
use std::env::args;
use std::time::Instant;

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

struct Field {
    pos_1: (usize, usize),
    pos_2: (usize, usize),
}

impl Field {
    fn invalid(&self, p: usize) -> bool {
        let (a, b) = self.pos_1;
        let (c, d) = self.pos_2;
        p < a || (p > b && p < c) || p > d
    }
}

struct IncomplBij {
    nb_field: usize,
    matrix: Vec<bool>,
}

impl std::ops::Index<(usize, usize)> for IncomplBij {
    type Output = bool;
    fn index(&self, (tf, field): (usize, usize)) -> &Self::Output {
        &self.matrix[self.nb_field * tf + field]
    }
}

impl std::ops::IndexMut<(usize, usize)> for IncomplBij {
    fn index_mut(&mut self, (tf, field): (usize, usize)) -> &mut Self::Output {
        &mut (self.matrix[self.nb_field * tf + field])
    }
}

impl std::fmt::Display for IncomplBij {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        for (idx, el) in self.matrix.iter().enumerate() {
            if idx % 20 == 0 {
                write!(f, "\n").unwrap()
            }
            write!(
                f,
                "{}",
                (|x| match x {
                    true => 1,
                    false => 0,
                })(*el)
            )
            .unwrap()
        }
        Ok(())
    }
}

impl IncomplBij {
    fn init(sz: usize) -> Self {
        IncomplBij {
            nb_field: sz,
            matrix: vec![true; sz * sz],
        }
    }

    fn simplify_from_lines(&mut self) -> bool {
        let mut changed_something = false;
        for tf in 0..self.nb_field {
            let mut idx = -1isize;
            for field in 0..self.nb_field {
                if self[(tf, field)] {
                    if idx >= 0 {
                        break;
                    }
                    idx = field as isize;
                }
            }
            for tfp in 0..self.nb_field {
                if tfp != tf {
                    changed_something = changed_something || self[(tfp, idx as usize)];
                    self[(tfp, idx as usize)] = false
                }
            }
        }
        changed_something
    }
    fn simplify_from_columns(&mut self) -> bool {
        let mut changed_somthing = false;
        for field in 0..self.nb_field {
            let mut idx = -1isize;
            let mut cont = false;
            for tf in 0..self.nb_field {
                if self[(tf, field)] {
                    if idx >= 0 {
                        cont = true;
                        break;
                    }
                    idx = tf as isize
                }
            }
            if cont {
                continue;
            }
            for fieldp in 0..self.nb_field {
                if fieldp != field {
                    changed_somthing = changed_somthing || self[(idx as usize, fieldp)];
                    self[(idx as usize, fieldp)] = false
                }
            }
        }
        changed_somthing
    }
    fn simplify(&mut self) {
        let mut cont = true;
        while cont {
            cont = self.simplify_from_columns() || self.simplify_from_lines()
        }
    }
    fn result(&self, my_ticket: &Vec<usize>) -> usize {
        let mut acc = 1;
        for i in 0..6 {
            for j in 0..self.nb_field {
                if self[(j, i)] {
                    acc *= my_ticket[j];
                    break;
                }
            }
        }
        acc
    }
}

trait IntvVec {
    fn push_intv(&mut self, intv: (usize, usize));
    fn invalid(&self, point: usize) -> bool;
}

impl IntvVec for Vec<(usize, usize)> {
    fn push_intv(&mut self, (l, h): (usize, usize)) {
        let mut i = 0;
        let len = self.len();
        while i < len {
            let (cl, ch) = self[i];
            if l > ch {
                i += 1;
                continue;
            }
            if h < cl {
                self.insert(i, (l, h));
                return;
            }
            if h <= ch {
                self[i] = (min(l, cl), ch);
                return;
            }
            let base = i;
            i += 1;
            let nmin = min(l, cl);
            let mut nmax = max(h, ch);
            while i < len {
                let (ncl, nch) = self[i];
                if nmax < ncl {
                    break;
                }
                nmax = max(nmax, nch);
                i += 1
            }
            self[base] = (nmin, nmax);
            self.drain(base + 1..i);
            return;
        }
        self.push((l, h))
    }
    fn invalid(&self, point: usize) -> bool {
        for (l, h) in self {
            if *l <= point && point <= *h {
                return false;
            }
        }
        return true;
    }
}

fn parse_field(line: &str) -> ((usize, usize), (usize, usize)) {
    let col = line.find(':').unwrap();
    let dash_1 = line[col..].find('-').unwrap() + col;
    let o = line[dash_1..].find('o').unwrap() + dash_1;
    let dash_2 = line[o..].find('-').unwrap() + o;
    let l1 = line[col + 2..dash_1].parse().unwrap();
    let h1 = line[dash_1 + 1..o - 1].parse().unwrap();
    let l2 = line[o + 3..dash_2].parse().unwrap();
    let h2 = line[dash_2 + 1..].parse().unwrap();
    ((l1, h1), (l2, h2))
}

enum State {
    ParsingFields,
    ParsingMyTicket,
    ParsingNearbyTickets,
}

fn run(input: &str) -> usize {
    let mut ignore = 0;
    let mut state = State::ParsingFields;
    let mut allowed_ranges = Vec::with_capacity(50);
    let mut my_ticket = Vec::with_capacity(50);
    let mut fields = Vec::with_capacity(50);
    let mut bij = IncomplBij::init(20);
    for line in input.split('\n') {
        if ignore > 0 {
            ignore -= 1;
            continue;
        }
        match state {
            State::ParsingFields => match line {
                "" => {
                    ignore = 1;
                    state = State::ParsingMyTicket
                }
                line => {
                    let (a, b) = parse_field(line);
                    allowed_ranges.push_intv(a);
                    allowed_ranges.push_intv(b);
                    fields.push(Field { pos_1: a, pos_2: b });
                }
            },
            State::ParsingMyTicket => {
                for n in line.split(',') {
                    my_ticket.push(n.parse::<usize>().unwrap())
                }
                for (tf, el) in my_ticket.iter().enumerate() {
                    for (field_idx, field) in fields.iter().enumerate() {
                        if field.invalid(*el) {
                            bij[(tf, field_idx)] = false
                        }
                    }
                }
                state = State::ParsingNearbyTickets;
                ignore = 2
            }
            State::ParsingNearbyTickets => {
                if line
                    .split(',')
                    .any(|x| allowed_ranges.invalid(x.parse().unwrap()))
                {
                    continue;
                }
                for (tf, el) in line
                    .split(',')
                    .map(|x| x.parse::<usize>().unwrap())
                    .enumerate()
                {
                    for (field_idx, field) in fields.iter().enumerate() {
                        if field.invalid(el) {
                            bij[(tf, field_idx)] = false
                        }
                    }
                }
            }
        }
    }
    bij.simplify();
    bij.result(&my_ticket)
}
