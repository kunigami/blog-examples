function expensive() {
    // Some expensive operation
    let s = 0;
    for (i = 0; i < 100000000; i++) {
        s += Math.random();
    }

    const content = document.getElementById('content');
    content.innerText = 'Result: ' + s;
}

const button = document.getElementById('button');
button.onclick = () => {
    expensive();
}
