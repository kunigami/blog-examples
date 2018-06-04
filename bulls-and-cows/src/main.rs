extern crate clap;

use clap::Arg;
use std::cmp;
use std::collections::HashMap;

const N: usize = 4;
// Number of digits
const D: usize = 10;
const NN: usize = (N + 1)*(N + 1);

struct Tree {
    guess: [i32; N],
    children: [Option<Box<Tree>>; NN],
}

fn main() {

    let matches = clap::App::new("BullsAndCows")
        .version("0.1")
        .arg(
            Arg::with_name("output")
                .short("o")
                .help("Whether to output the decision tree as JSON")
                .takes_value(false)
        )
        .get_matches();

    let print_output: bool = matches.is_present("output");

    let initial_state = initialize_possibilities();
    let result = search(initial_state, 0, 0);

    if print_output {
        println!("{}", output_json(&result));
    } else {
        // Only print stats
        println!("Tree height {}", tree_height(&result));
        println!("Tree size {}", tree_size(&result));
    }
}

fn initialize_possibilities() -> Vec<[i32; N]> {
    let possibilities = initialize_possibilities_with_params(N as i32, 0);
    // Convert to array
    let mut new_possibilities = vec![];
    for possibility in possibilities {
        let mut possibility_arr = [0; N];
        for i in 0..possibility.len() {
            possibility_arr[i] = possibility[i];
        }
        new_possibilities.push(possibility_arr);
    }
    return new_possibilities;
}

fn initialize_possibilities_with_params(state_index: i32, mut visited: i32) -> Vec<Vec<i32>> {
    if state_index == 0 {
        let mut empty_vec = Vec::new();
        empty_vec.push(Vec::new());
        return empty_vec;
    }

    let mut new_possibilities = Vec::new();
    for digit in 0..D {
        // Avoid the same digit
        if visited & (1 << digit) != 0 {
            continue;
        }
        // Visit digits
        visited = visited | (1 << digit);
        let possibilities = initialize_possibilities_with_params(state_index - 1, visited);
        // Unvisit
        visited = visited & !(1 << digit);
        for possibility in possibilities {
            let mut new_possibility = possibility.to_vec();
            new_possibility.push(digit as i32);
            new_possibilities.push(new_possibility);
        }
    }
    return new_possibilities
}

fn compute_score(guess: &[i32; N], secret: &[i32; N]) -> (i32, i32) {
    let mut perfect_matches = 0;
    for i in 0..guess.len() {
        if guess[i] == secret[i] {
            perfect_matches += 1;
        }
    }

    let mut look_up_position: [bool; D] = [false; D];
    for i in 0..guess.len() {
        let position = guess[i] as usize;
        look_up_position[position] = true;
    }
    let mut any_matches = 0;
    for i in 0..secret.len() {
        let position = secret[i] as usize;
        if look_up_position[position] {
            any_matches += 1;
        }
    }
    let imperfect_matches = any_matches - perfect_matches;
    return (perfect_matches, imperfect_matches);
}

fn encode_score(score: (i32, i32)) -> usize {
    let n = (N + 1) as i32;
    return (score.0 * n + score.1) as usize;
}

fn decode_score(score_index: usize) -> (i32, i32) {
    let n = (N + 1) as i32;
    let encoded_score = score_index as i32;
    let perfect_matches = encoded_score / n;
    let imperfect_matches = encoded_score % n;
    return (perfect_matches, imperfect_matches);
}

fn score_to_string(score: (i32, i32)) -> String {
    return format!("({}, {})", score.0, score.1);
}

fn group_possibilities_by_score(
    guess: &[i32; N],
    possibilities: &Vec<[i32; N]>
) -> [Vec<[i32; N]>; NN] {
    let mut possibilities_by_score: [Vec<[i32; N]>; NN] = Default::default();
    for i in 0..NN {
        possibilities_by_score[i] = vec![];
    }

    for possibility in possibilities {
        let mut new_possibility = possibility.clone();
        let score = compute_score(&guess, &new_possibility);
        let score_index = encode_score(score);
        possibilities_by_score[score_index].push(new_possibility)
    }
    return possibilities_by_score;
}

fn search(possibilities: Vec<[i32; N]>, level: i32, visited_bits: u32) -> Tree {
    // The secret was found!
    if possibilities.len() == 1 {
        let guess = possibilities[0].clone();
        return singleton_node(&guess);
    }

    let mut best_result = singleton_node(&[0; N]);
    let mut best_tree_size = 10000;
    let mut best_tree_height = 10000;

    // Optimization: avoid recurson on equivalent classes to reduce branching.
    let mut visited_classes = HashMap::new();

    for guess in &possibilities {

        let class_id = get_class(visited_bits, guess);
        // Same equivalence class. Won't yield new results
        if visited_classes.contains_key(&class_id) {
            continue;
        }

        visited_classes.insert(class_id, true);

        let possibilities_by_score = group_possibilities_by_score(&guess, &possibilities);

        let mut max_tree_size = 0;
        let mut max_tree_height = 0;
        let mut result = singleton_node(&guess);

        for score_index in 0..NN {
            let possibilities_for_score = &possibilities_by_score[score_index];
            if possibilities_for_score.len() == 0 {
                continue;
            }

            let mut new_visitied_bits = visited_bits;
            for digit in guess {
                new_visitied_bits |= 1u32 << digit;
            }

            let subtree = search(possibilities_for_score.to_vec(), level + 1, new_visitied_bits);

            max_tree_size = cmp::max(max_tree_size, tree_size(&subtree));
            max_tree_height = cmp::max(max_tree_height, tree_height(&subtree));

            // Optimization: there is no way we will find a shorter/smaller tree
            // if these conditions happen.
            if max_tree_height > best_tree_height {
                break;
            }
            if max_tree_height == best_tree_height &&
               max_tree_size >= best_tree_size {
                break;
             }

            result.children[score_index] = Some(Box::new(subtree));
        }

        // Get the best height. Break ties by smallest size
        if max_tree_height < best_tree_height || (
            max_tree_height == best_tree_height && max_tree_size < best_tree_size
        ) {
            best_tree_height = max_tree_height;
            best_tree_size = max_tree_size;
            best_result = result;
        }
    }
    return best_result;
}

fn singleton_node(guess: &[i32; N]) -> Tree {
    let mut children: [Option<Box<Tree>>; NN] = Default::default();
    for i in 0..NN {
        children[i] = None;
    }
    return Tree {
        guess: guess.clone(),
        children: children,
    };
}

fn guess_to_string(xs: &[i32; N]) -> String {
    let vec_of_strings: Vec<String> = xs.iter().map(|&x| x.to_string()).collect();
    return format!("[{}]", vec_of_strings.join(", "));
}

/**
 * Output a JSON in a format that can be consumed by the application.
 */
fn tree_to_string(tree: &Tree) -> String {
    let subtree = &tree.children;
    let mut subtrees_as_strings = vec![];
    for score_index in 0..NN {
        let maybe_child = &subtree[score_index];
        match maybe_child {
            &Some(ref child) => {
                let score_as_string = score_to_string(decode_score(score_index));
                subtrees_as_strings.push(
                    format!("'{}': {}", score_as_string, tree_to_string(&child))
                );
            },
            &None => continue,
        }
    }
    let guess_as_string = guess_to_string(&tree.guess);
    let subtrees_as_string = format!("{{{}}}", subtrees_as_strings.join(", "));
    return format!("{{'guess': {}, 'subtree': {}}}", guess_as_string, subtrees_as_string);
}

fn output_json(tree: &Tree) -> String {
    return format!("const decisionTree = {};", tree_to_string(tree));
}

fn tree_size(tree: &Tree) -> usize {

    let subtree = &tree.children;
    let mut size = 0;
    for maybe_child in subtree {
        match maybe_child {
            &Some(ref child) => {
                size += tree_size(&child);
            },
            &None => continue,
        }
    }
    return size + 1;
}

fn tree_height(tree: &Tree) -> usize {
    let subtree = &tree.children;
    let mut height = 0;
    for maybe_child in subtree {
        match maybe_child {
            &Some(ref child) => {
                height = cmp::max(height, tree_height(&child));
            },
            &None => continue,
        }
    }
    return height + 1;
}

// The class of equivalence of a guess d1,d2,...,dN is given by a list
// of (p_i, f_i), where f_i belongs to visited bits. The list is sorted by p_i
fn get_class(visited_bits: u32, guess: &[i32; N]) -> i32 {
    let mut class_id = 0;
    let mut multiplier: i32 = 1;
    let d = (D + 1) as i32;
    for pos in 0..guess.len() {
        let digit = guess[pos];
        if visited_bits & (1 << digit) != 0 {
            class_id += multiplier * (digit + 1);
        }
        multiplier *= d;
    }
    return class_id;
}
