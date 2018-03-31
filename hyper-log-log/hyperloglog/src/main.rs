extern crate clap;
extern crate farmhash;
extern crate rand;

use rand::Rng;
use std::cmp;
use std::vec::Vec;
use clap::Arg;

const TWO_TO_32: f64 = 4294967296.0; // 2^32

/**
 * This program estimates the number of disctinct values from a given stream, using a probabilistic
 * algorithm called HyperLogLog (HLL).
 */
fn main() {
    let matches = clap::App::new("HyperLogLog")
        .version("0.1")
        .arg(
            Arg::with_name("num_elems")
                .short("n")
                .help("Number of elements to generate")
                .takes_value(true)
        )
        .arg(
            Arg::with_name("range")
                .short("r")
                .help("Sample values from [0-r]")
                .takes_value(true)
        )
        .get_matches();

    let num_elements: usize = matches.value_of("num_elems").unwrap_or("1000").parse().unwrap();
    let range_upper_bound: u32 = matches.value_of("range").unwrap_or("2500").parse().unwrap();
    println!("Number of elements {}, range {}", num_elements, range_upper_bound);

    let mut elements = Vec::new();
    for _ in 0..num_elements {
        let element = rand::thread_rng().gen_range(1, range_upper_bound).to_string();
        elements.push(element);
    }

    let estimate: u32 = hll(&elements, Options {b: 5});
    println!("Distinct values estimate {}", estimate);

    // Compare with deterministic algorithm
    let distinct = count_distinct(&elements);
    println!("Distinct values {}", distinct);
    println!(
        "Relative error {}",
        ((distinct as f64) - (estimate as f64)).abs()/(distinct as f64) * 100.0
    );
}

struct Options {
    // b in [4-16]. There are 2^b buckets
    b: i32
}

/**
 * Estimates the number of distinct values from the stream.
 */
fn hll(elements: &Vec<String>, options: Options) -> u32 {
    let Options {b} = options;

    // Validate input values
    assert!(b >= 4 && b <= 16);

    // m = 2^b
    let m: u32 = 1 << b;

    const LARGE_ESTIMATE_THRESHOLD: f64 = 143165576.53333333;
    let alpha: f64 = match b {
        4 => 0.673,
        5 => 0.697,
        6 => 0.709,
        // b >= 7
        _ => 0.7213/(1.0 + 1.079/(m as f64))
    };

    let first_b_bits_mask = m - 1;
    let mut first_non_zero_by_experiment: Vec<u32> = vec![0 as u32; m as usize];
    for element in elements {
        let hash_value = hash(&element);

        // Extracts the first b bits from hash_value to determine the bucket
        let experiment_index: usize = (hash_value & first_b_bits_mask) as usize;
        // Finds the position of the first 1 bit in the remaining bits
        let mut first_non_zero: u32 = first_non_zero_bit_position(hash_value >> b);

        first_non_zero_by_experiment[experiment_index] = cmp::max(
            first_non_zero_by_experiment[experiment_index],
            first_non_zero
        );
    }

    // Compute estimate
    let mut indicator: f64 = 0.0;
    let base: f64 = 2.0;
    for first_non_zero in &first_non_zero_by_experiment {
        indicator += base.powf(-(*first_non_zero as f64));
    }
    let m_multiplier = m as f64;
    let mut estimate: f64 = (m_multiplier * m_multiplier * alpha) / indicator;

    // Correction
    if estimate <= 2.5 * m_multiplier {
        // Small range correction
        let mut buckets_with_zero = 0;
        for first_non_zero in first_non_zero_by_experiment {
            if first_non_zero == 0 {
                buckets_with_zero += 1;
            }
        }
        if buckets_with_zero > 0 {
            estimate = m_multiplier * (m_multiplier / (buckets_with_zero as f64)).log2();
        }
    } else if estimate > LARGE_ESTIMATE_THRESHOLD {
        // Large range correction
        estimate = -TWO_TO_32 * (1.0 - estimate/TWO_TO_32).log2();
    }
    estimate as u32
}

fn count_distinct(elements: &Vec<String>) -> u32 {
    let mut sorted_values = elements.to_vec();
    sorted_values.sort();
    let mut distinct_count = 1;
    for i in 1..sorted_values.len() {
        if sorted_values[i] != sorted_values[i - 1] {
            distinct_count += 1
        }
    }
    distinct_count
}

fn to_binary(value: u32) -> String {
    let mut result = String::new();
    let mut temp = value;
    while temp > 0 {
        result.push_str(&(temp % 2).to_string());
        temp /= 2;
    }
    return result;
}

fn hash(value: &String) -> u32 {
    farmhash::hash32(&value.as_bytes())
}

fn first_non_zero_bit_position(input: u32) -> u32 {
    let mut remaining: u32 = input;
    let mut first_non_zero: u32 = 1;
    while (remaining & 1) == 0 && remaining > 1 {
        remaining /= 2;
        first_non_zero += 1;
    }
    first_non_zero
}
