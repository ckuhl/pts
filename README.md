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

In addition, I figured it would be a good learning experience for building
command-line programs using Python.

## Getting started
You'll need the PyYAML module installed, and then simply add the script to
your path to use it wherever.

If you have python3.5 and virtualenv installed, you can test it locally
instead. All you have to do is run:
`make setup` to set up a virtualenvironment and then

`make demo`

## Usage
```
$ pts.py -vvvv
Testing: ['./ex.py'] ===========================================================
Test failed: Failing test
In: 1
Expected: 0
Out: 1
================================================================================
4 tests run, with 3 successful and 1 failing
```

## Format
```YAML
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
```

## Generally

```YAML
---
program: [<list of arguments>]
pipe_to: [<program to pull output from>]
file_in: <optional file to feed into stdin before each test>
name: <human readable name>
tags: [<list of tags to run using>]
tests:
  - name: "Human readable name"
    in: "input to program"
    args: [<optional>]
    out: "expected output from program"
    stderr: "<optional>"
...
```

## Up next
- Membership tests
	- e.g. `test: ... in_stdout: "SUCCESS"`
- Arbitrary piping (e.g. a -> b -> ... -> y -> z)
	- combine "program" and "pipe_to" into one list of commands
- Clean up code a little
	- make main script fairly clean
	- refactor to remove directory arg from Suite.run()
- Add colour to the logging
- Fix up logging levels
- allow <C-c> cancelling without complaining

