console.log('test');

const js = import("./node_modules/@kunigami/hello-wasm/hello_wasm.js");
js.then(js => {
  js.greet("WebAssembly");
});
