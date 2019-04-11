extern crate farmhash;

use std::collections::HashSet;
use std::result::Result;
use rbtree;

struct Entry {
    hash: u32,
    id: String,
}

/**
 * The table can contain two types of elements: container or entries. Everey entry belong to a
 * container. We say that an entry e belongs to a container c if the hash of c, h(c), is the
 * smallest value greater than h(e).
 *
 * This structure allows adding and removing containers and entries.
 *
 * It can determine the container of a given entry in O(log n) time.
 */
pub struct ConsistentHashTable {
    containers: rbtree::RBTree<u32, Entry>,
    entries: HashSet<u32>,
    // The hash function must have the property of mapping strings to
    // the space of u32 numbers with uniform probability.
    hash_function: fn (&String) -> u32
}

impl ConsistentHashTable {

    pub fn set_hash_function(&mut self, f: fn (&String) -> u32) {
        self.hash_function = f;
    }

    pub fn add_container(&mut self, id: String) {
        let h = (self.hash_function)(&id);
        self.containers.insert(h, Entry {hash: h, id: id});
    }

    pub fn remove_container(&mut self, id: String) {
        let h = (self.hash_function)(&id);
        self.containers.remove(&h);
    }

    pub fn add_entry(&mut self, key: String) {
        let h = (self.hash_function)(&key);
        self.entries.insert(h);
    }

    pub fn get_container_id_for_entry(&self, entry_key: String) -> Result<&str, &str> {
        let target_key = (self.hash_function)(&entry_key);
        let mut container_id = "";
        let mut smallest_valid_hash = 0;

        if (self.containers.len() == 0) {
            return Err("No containers added.");
        }

        let mut closest_key: u32 = std::u32::MAX;
        self.containers.get_with_visitor(
            &target_key,
            |node_key| {
                if (
                    distance(closest_key, target_key) >
                    distance(*node_key, target_key) &&
                    *node_key > target_key
                ) {
                    closest_key = *node_key;
                }
            }
        );

        // Every container key is smaller than the target_key. In this case we 'wrap around' the
        // table and select the first element.
        if (closest_key == std::u32::MAX) {
            let result = self.containers.get_first();
            match result {
                None => {
                    return Err("Did not find first entry.");
                }
                Some((_, entry)) => {
                    let container_id = &entry.id;
                    return Ok(container_id);
                }
            }
        }

        let result = self.containers.get(&closest_key);
        match result {
            None => {
                return Err("Closest key was incorrectly returned.");
            }
            Some(entry) => {
                let container_id = &entry.id;
                return Ok(container_id);
            }
        }
    }
}

pub fn new_hash_table() -> ConsistentHashTable {
    return ConsistentHashTable {
        containers: rbtree::RBTree::new(),
        entries: HashSet::new(),
        hash_function: hash_function,
    };
}

fn hash_function(value: &String) -> u32 {
    return farmhash::hash32(&value.as_bytes());
}

/**
 * Distance between 2 unsigned numbers (always positive)
 *
 * NOTE: We cannot use (numA - numB).abs() since u32 doesn't have negatives.
 */
fn distance(numA: u32, numB: u32) -> u32 {
    if numA > numB {
        return numA - numB;
    }
    return numB - numA;
}
