# pts
## Python Test Suite
A test suite that uses YAML files as tests.

## Motivation
Previously I have been using a bash script put together as an assignment for
CS 246, however that has left me with a few annoyances. This is meant to solve
those problems:

- Having one file instead of 3 per test, for however many test cases there are.
- Being difficult to extend

## Contents
- `test.py` the testing script
- `Testfile` the test cases
- `ex.py` an example script to test against

## Format
    ---
    program: ./ex.py
    tests:
      - name: "Two plus two"
        in: "2 2"
        out: "4"
      - name: "Two times two"
        in: "2 2"
        args: "-m"
        out: "4"
    ...

