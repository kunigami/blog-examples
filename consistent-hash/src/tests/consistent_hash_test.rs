use consistent_hash;
use consistent_hash::ConsistentHashTable;

fn run_command<'a>(hash_table: &'a mut ConsistentHashTable, command: &str) -> Option<&'a str> {
    if command.starts_with("add s") { // Captures add s<x>
        let server = &command[4..]; // k<x>
        print!("insert entry: {}\n", server);
        hash_table.add_container(server.to_owned());
        return None;
    }

    if command.starts_with("remove s") { // Captures remove s<x>
        let server = &command[7..]; // s<x>
        print!("removing entry: {}\n", server);
        hash_table.remove_container(server.to_owned());
        return None;
    }

    if command.starts_with("add k") { // Captures add k<x>
        let key = &command[4..]; // k<x>
        print!("adding key: {}\n", key);
        hash_table.add_entry(key.to_owned());
        return None;
    }

    if command.starts_with("query k") {
        let key = &command[6..];
        print!("query: {}\n", key);
        let query_id = &command[0..1];
        let result = hash_table.get_container_id_for_entry("k1".to_owned());
        let id = match result {
            Ok(id) => id,
            Err(error) => panic!("Invalid")
        };
        print!("Got server: {}\n", id);
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
        (vec!["add s1", "add s2", "add s3", "add k1", "query k1"], vec!["s1"]),
        // Case 2: inserting a key with a bunch of pre-existing servers then removing a server
        (
            vec![
                "add s1",
                "add s2",
                "add s3",
                "add k1",
                "query k1",
                "remove s1",
                "query k1"
            ],
            vec!["s1", "s2"]
        ),
    ];

    for instance in &data {
        let commands = &instance.0;
        let query_results = &instance.1;

        let mut hash_table = consistent_hash::new_hash_table();

        let mut query_results_index = 0;

        for &command in commands {

            let result = run_command(&mut hash_table, command);
            match result {
                None => continue,
                Some(actual_server) => {
                    let expected_server = query_results[query_results_index];
                    query_results_index += 1;

                    print!("Got server: {}, expected {}\n", actual_server, expected_server);
                    assert_eq!(actual_server, expected_server);
                }
            }
        }
    }
}
