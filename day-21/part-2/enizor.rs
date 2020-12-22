use std::time::Instant;
use std::{collections::HashMap, env::args};

fn main() {
    let now = Instant::now();
    let output = run(&args().nth(1).expect("Please provide an input"));
    let elapsed = now.elapsed();
    println!("_duration:{}", elapsed.as_secs_f64() * 1000.);
    println!("{}", output);
}

fn run(input: &str) -> String {
    let mut allergens = Vec::new();
    let mut ingredients = HashMap::new();
    let mut parsed = Vec::new();
    let input_bytes = input.as_bytes();
    for line in input_bytes.split(|&b| b == b'\n') {
        parsed.push((Vec::new(), Vec::new()));
        let mut on_allergens = false;
        if line.is_empty() {
            break;
        }
        for word in line.split(|&b| b == b' ') {
            if word[0] == b'(' {
                on_allergens = true;
            } else if on_allergens {
                let name = &word[..word.len() - 1];
                parsed.last_mut().unwrap().1.push(name);
                if allergens.iter().find(|&&n| n == name).is_none() {
                    allergens.push(name);
                }
            } else {
                let name = Name::from_bytes(word);
                ingredients.entry(name).or_insert(usize::MAX);
                parsed.last_mut().unwrap().0.push(name);
            }
        }
    }
    allergens.sort_unstable();
    let nb_allergens = allergens.len();
    for v in ingredients.values_mut() {
        *v = usize::MAX - ((1 << nb_allergens) - 1);
    }
    for (ing, all) in &parsed {
        for (&k, v) in ingredients.iter_mut() {
            if ing.iter().all(|&name| name != k) {
                for &a in all.iter() {
                    let pos = allergens
                        .iter()
                        .enumerate()
                        .find(|(_, &n)| n == a)
                        .unwrap()
                        .0;
                    *v |= 1 << pos;
                }
            }
        }
    }
    let mut dangerous = Vec::new();
    for (&k, &v) in ingredients.iter() {
        if v != usize::MAX {
            dangerous.push(k);
        }
    }
    let mut count = 0;
    while count < nb_allergens {
        count = 0;
        for k in &dangerous {
            let set = !ingredients[k];
            if set & (set - 1) == 0 {
                count += 1;
                for (k2, v) in ingredients.iter_mut() {
                    if k2 != k {
                        *v |= set;
                    }
                }
            }
        }
    }
    let mut out = Vec::new();
    for (i, a) in allergens.iter().enumerate() {
        let mask = !(1 << i);
        for (&k, &v) in ingredients.iter() {
            if v == mask {
                out.push(k.to_str());
            }
        }
    }
    out.join(",")
}

#[derive(Clone, Copy, PartialEq, Eq, Hash)]
struct Name(u64);

impl Name {
    fn from_bytes(input: &[u8]) -> Self {
        let mut bytes = [0; 8];
        bytes[..input.len()].copy_from_slice(input);
        Self(u64::from_le_bytes(bytes))
    }

    fn to_str(&self) -> String {
        let bytes = self.0.to_le_bytes();
        let pos = bytes
            .iter()
            .enumerate()
            .find(|(_, b)| **b == 0)
            .map(|(i, _)| i)
            .unwrap_or(8);
        std::str::from_utf8(&bytes[..pos]).unwrap().to_owned()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn run_test() {
        assert_eq!(
            run("mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"),
            "mxmxvkd,sqjhc,fvjkl"
        )
    }
}
