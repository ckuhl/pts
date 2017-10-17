# pts
## Python Test Suite
A test suite built on YAML

## Motivation
Previously I have been using a bash script put together as an assignment for
CS 246, however that has left me with a few annoyances. This is meant to
solve those problems:

- having one file instead of 3 files for each test, multiplied by however
  many test cases I have
- being more resistant to breakage (something about me and shell scripting
  does not mix)
- more easily extensible (in the future)

In addition, I have not used python to build a shell program like this
before, so I figured it would be a good learning experience.

## Getting started
You'll need the PyYAML module installed, and then simply add the script to
your path to use it wherever.

## Usage
    $ pts.py -vvvv
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
    program: the command to run
    pipe_to: (optional) command(s) to pipe the output to
    name: (optional) human-readable program name
    tags: (optional) list of tags to run tests by
    tests:
      - name: human-readable test name
        in: input (or empty)
        args: (optional) program arguments
        out: expected output (or empty)
        stderr: (optional) expected standard error
    ...

## Up next
- Membership tests
	- e.g. `test: ... in_stdout: "SUCCESS"`
- Arbitrary piping (e.g. a -> b -> ... -> y -> z)
	- combine "program" and "pipe_to" into one list of commands
- Clean up code a little
	- make main script fairly clean
- Add colour to the logging
- Fix up logging levels

