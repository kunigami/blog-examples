function random_array() {
    a = []
    for (let i = 0; i < 10000000; i++) {
        a.push(Math.random());
    }
    return a;
}

function for_loop(a) {
    let s = 0;
    for (let i = 0; i < a.length; i++) {
        s += a[i];
    }
    return s;
}

function foreach(a) {
    let s = 0;
    a.forEach(v => s += v);
    return s;
}

function reduce(a) {
    return a.reduce((acc, v) => acc + v, 0);
}

function benchmark(fn, runs = 10) {
    let durations = 0;
    let r = 0;
    for (let i = 0; i < runs; i++) {
        a = random_array();
        start = performance.now();
        r += fn(a);
        durations += performance.now() - start;
    }
    return durations / runs;
}


let start;

const for_loop_duration = benchmark(for_loop);
console.log(`for loop ${for_loop_duration}ms`);

const reduce_duration = benchmark(reduce);
console.log(`reduce ${reduce_duration}ms`);

const foreach_duration = benchmark(foreach);
console.log(`foreach ${foreach_duration}ms`);
