use consistent_hash;
use consistent_hash::ConsistentHashTable;

#[cfg(test)]
extern crate mocktopus;

fn run_command<'a>(hash_table: &'a mut ConsistentHashTable, command: &str) -> Option<&'a str> {
    if command.starts_with("add s") { // Captures add s<x>
        let server = &command[4..]; // s<x>
        hash_table.add_container(server.to_owned());
        return None;
    }

    if command.starts_with("remove s") { // Captures remove s<x>
        let server = &command[7..]; // s<x>
        hash_table.remove_container(server.to_owned());
        return None;
    }

    if command.starts_with("add k") { // Captures add k<x>
        let key = &command[4..]; // k<x>
        hash_table.add_entry(key.to_owned());
        return None;
    }

    if command.starts_with("query k") {
        let key = &command[6..];
        let result = hash_table.get_container_id_for_entry(key.to_owned());
        let id = match result {
            Ok(id) => id,
            Err(error) => panic!("Invalid")
        };
        return Some(id);
    }

    print!("command not recognized: {}\n", command);
    return None;
}

#[test]
fn test_commands() {

    // Simplified command parsing to allow writing test cases in a concise and readable way
    //
    // add s<x> - represents adding a server
    // remove s<x> - represents deleting a server
    // add k<x> - represents add a key
    // query k<x> - represents querying the server to which k<x> is assigned to
    let data: Vec<(Vec<&str>, Vec<&str>)> = vec![
        // Case 1: inserting a key with a bunch of pre-existing servers
        (vec!["add s10", "add s20", "add s30", "add k9", "query k9"], vec!["s10"]),
        // Case 2: inserting a key with a bunch of pre-existing servers then removing a server
        (
            vec![
                "add s10",
                "add s20",
                "add s30",
                "add k9",
                "query k9",
                "remove s10",
                "query k9",
                "remove s20",
                "query k9"
            ],
            vec!["s10", "s20", "s30"]
        ),
        // Case 3: all containers are smaller than the queried value
        (
            vec![
                "add s10",
                "add s20",
                "add k100",
                "add s30",
                "query k100",
            ],
            vec!["s10"]
        ),
    ];

    for instance in &data {
        let commands = &instance.0;
        let query_results = &instance.1;

        let mut hash_table = consistent_hash::new_hash_table();
        hash_table.set_hash_function(predictable_hash);

        let mut query_results_index = 0;

        for &command in commands {

            let result = run_command(&mut hash_table, command);
            match result {
                None => continue,
                Some(actual_server) => {
                    let expected_server = query_results[query_results_index];
                    query_results_index += 1;
                    assert_eq!(actual_server, expected_server);
                }
            }
        }
    }
}

/*
 * A hash function that dummily maps the numeric part of the key to a value
 */
fn predictable_hash(value: &String) -> u32 {
    let numeric_part = &value[1..];
    return numeric_part.parse::<u32>().unwrap();
}
