# SoCo Assignment 02
Assignment 2 for the course Software Construction 23HS 22BI0004. 

These are the files we hand in:
- `lgl_interpreter.py` interprets our implementation of the Little German Language, LGL.
- `example_operations.gsc` a rather beautifully formatted showcase of our lovely programming language.
- `example_class.gsc` showcases classes and objects
- `example_trace.gsc` showcases tracing execution times to a logfile.
- `reporting.py` consumes said logfile and reports execution time deltas in tabular form.

## Getting started
### Interpreter
usage: lgl_interpreter.py \[-h\] \[--trace TRACE\] \[--usedatetime\] files \[files ...\]

Runs our little germal programming language.

positional arguments:
  files          Specify lgl source files to run

options:
  -h, --help            show this help message and exit
  -t TRACE, --trace TRACE
                        Log details of start and end times to FILENAME
  -d, --usedatetime     Use datetime instead of perf_counter to trace
                        execution times (not recommended)

### Reporting

usage: reporting.py \[-h\] file

Takes tracing from lgl_interpreter.py and generates a report

positional arguments:
  file        Specify lgl log files to report on

options:
  -h, --help  show this help message and exit

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

### Arrays

Arrays of fixed length are set by setting a variable with the list as content. The first argument is the length, then the content of the elements.

```json
["variable_setzen", "beispiel_liste",
    ["liste", 3, 1, "Wort", 3.14]
]

["ausdrucken",
    ["variable_abrufen", "beispiel_liste"]
]
# prints ['liste', 3, 1, 'Wort', 3.14]
```

### Tracing

We implemented the tracing as a decorator `@trace` function that wraps the function `do()`. 

By default, **we use `time.perf_counter()` to measure performance**. If you wish to use `datetime.datetime.now()`, the option is available by setting an additional `--usedatetime` flag when using `lgl_interpreter.py` with `--trace`. 

When tracing, we **write output immediately to the file**. A more mature implementation should write the file at the end of the tracing, so as not to add extra execution time.

`reporting.py` automatically detects and properly handles either kind of timestamp.

