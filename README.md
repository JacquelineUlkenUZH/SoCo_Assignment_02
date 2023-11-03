# SoCo Assignment 02
Assignment 2 for the course Software Construction 23HS 22BI0004. 

These are the files we hand in:
- `lgl_interpreter.py` interprets our implementation of the Little German Language, LGL.
- `example_operations.gsc` a rather beautifully formatted showcase of our lovely programming language.
- `example_class.gsc`
- `example_trace.gsc`
- `reporting.py`

## Getting started
usage: lgl_interpreter.py \[-h\] \[--trace TRACE\] files \[files ...\]

Runs our little germal programming language.

positional arguments:
  files          Specify lgl source files to run

options:
  -h, --help     show this help message and exit
  --trace TRACE  Log details of start and end times to FILENAME

Command-line arguments are parsed using `argparse`.

## Decisions

### Print with `do_ausdrucken`
Our implementation expects one or more arguments and prints them all.

Interesting implementation details:
- If a string "nobr" is passed, we print without line-break.
- If a string "title" is passed, we colour printout green.

### While loop with `do_solange`
Our implementation expects two lists:
- A list of length 1 or 3 containing a truth test.
- A list of instructions that `do_abfolge()` can handle

Interesting implementation details:
- We implemented the truth test by constructing a testing string that Python then evaluates using `eval()`.
- We implement repetition using recursive function calls.
- We pass results recursively, because otherwise the last iteration would return None (because it doesn't run).

### Arrays with `do_varsetzen` and `do_varabrufen`
We implemented arrays as normal variables. That means both `do_varsetzen` and `do_varabrufen` now accept an additional **optional parameter to specify the index** of an array.

We detect arrays by checking whether we were given a string starting with "\[" and ending with "\]". We then convert that string to an array using `eval()`.