# pts
## Python Test Suite
A test suite based on YAML files.

## Motivation
Previously I have been using a bash script put together as an assignment for
CS 246, however that has left me with a few annoyances. This is meant to solve
those problems:

- Having one file instead of 3 files for each test, multiplied by however many
  test cases I have.
- Being easy to break (as comes with little experience in shell scripting)

## Contents
- `test.py` the testing script
- `Testfile` example test cases
- `ex.py` an example script to test against

## Usage
    $ test.py
    Testing: ['./ex.py'] ===========================================================
    Test failed: Failing test
      In: 1
      Expected: 0
      Out: 1
    ================================================================================
    5 tests run, with 4 successful and 1 failing

## Format
    ---

    program: [./ex.py]
    tests:
      - name: "Two plus two"
        in: "2 2"
        out: "4"

      - name: "Multiplication"
        in: "2 3"
        args: "-m"
        out: "6"

      - name: "Multiple addition"
        in: "1 2 3 4 5"
        out: "15"

      - name: "Failing test"
        in: "1"
        out: "0"

      - name: "Multiline test"
        in: |
         1
         2
         3
        out: "6"

    ...

