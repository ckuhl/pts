# pts
## Python Test Suite
A test suite based on YAML files.

## Motivation
Previously I have been using a bash script put together as an assignment for
CS 246, however that has left me with a few annoyances. This is meant to solve
those problems:

- having one file instead of 3 files for each test, multiplied by however many
  test cases I have
- being more resistant to breakage (something about me and shell scripting
  does not mix)
- more easily extensible (in the future)

In addition, I have not used python to build a shell program like this before,
so I figured it would be a good learning experience.

## Getting started
You'll need the PyYAML module installed, and then simply add the script to your
path to use it wherever.

## Usage
    $ test.py
    Testing: ['./ex.py'] ===========================================================
    Test failed: Failing test
      In: 1
      Expected: 0
      Out: 1
    ================================================================================
    4 tests run, with 3 successful and 1 failing

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

      - name: "Failing test"
        in: "1"
        out: "0"

      - name: "Multiline test"
        in: |+
         1
         2
         3
        out: "6"

    ...

## Generally

    ---
    program: REQUIRED - command to run
    name: OPTIONAL - human-readable program name
    tags: OPTIONAL - tags to run tests by
    tests: REQUIRED
      - name: REQUIRED
        in: REQUIRED
        args: OPTIONAL
        out: REQUIRED
        stdout: OPTIONAL
...

