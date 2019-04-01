extern crate farmhash;
use std::collections::HashSet;
use std::result::Result;

struct Entry {
    hash: u32,
    id: String,
}

pub struct ConsistentHashTable {
    container_entries: Vec<Entry>,
    entries_map: HashSet<u32>,
}

impl ConsistentHashTable {
    /**
     * Adds a container entry to the hash table.
     */
    pub fn add_container(&mut self, id: String) {
        let h = hashfn(&id);
        self.container_entries.push(Entry {hash: h, id: id});
    }

    pub fn remove_container(&mut self, id: String) {
        self.container_entries.retain(|entry| {
            return entry.id != id;
        });
    }

    pub fn add_entry(&mut self, key: String) {
        let h = hashfn(&key);
        self.entries_map.insert(h);
    }

    pub fn get_container_id_for_entry(&self, entry_key: String) -> Result<&str, &str> {
        let entry_hash = hashfn(&entry_key);
        let mut container_id = "";
        let mut smallest_valid_hash = 0;

        if (self.container_entries.len() == 0) {
            return Err("No containers added.");
        }

        for item in self.container_entries.iter() {
            // let Entry {hash, id} = item;
            if item.hash > entry_hash && (container_id == "" || item.hash < smallest_valid_hash) {
                smallest_valid_hash = item.hash;
                container_id = &item.id;
            }
        }

        if container_id == "" {
            panic!("Container not found. This should never happen.")
        }

        return Ok(container_id);
    }
}

pub fn new_hash_table() -> ConsistentHashTable {
    return ConsistentHashTable {
        container_entries: vec![],
        entries_map: HashSet::new(),
    };
}

fn hashfn(value: &String) -> u32 {
    return farmhash::hash32(&value.as_bytes());
}
