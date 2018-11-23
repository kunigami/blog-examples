BIN_DIR := bin
SRC_DIR := src

# Execute code
run: $(BIN_DIR)/eulerian_circuit.js typecheck
	node $(BIN_DIR)/eulerian_circuit.js

# When file changes, re-run babel
$(BIN_DIR)/eulerian_circuit.js: $(SRC_DIR)/eulerian_circuit.js
	./node_modules/.bin/babel src --out-dir $(BIN_DIR)

.flowconfig:
	flow init

# Make sure the code passes typechecking
typecheck: .flowconfig
	./node_modules/.bin/flow
