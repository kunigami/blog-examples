# NOTE: trie.ml must be obtained from https://github.com/kunigami/ocaml-data-structures/blob/master/trie/trie.ml
# TODO: automate

all: test
run:
	export OCAMLRUNPARAM="l=1000000000"
	@echo $(OCAMLRUNPARAM)
	ocamlfind ocamlc -o subsequence -package oUnit -package batteries -linkpkg -g  trie.ml subsequence.ml
	./subsequence
test: test_subsequence
test_subsequence:
	ocamlc -o subsequence_test -package oUnit -package batteries -linkpkg -g  trie.ml subsequence.ml subsequence_test.ml
	./subsequence_test
clean:
	rm -f *.cmi *.cmo ./subsequence_test ./subsequence
