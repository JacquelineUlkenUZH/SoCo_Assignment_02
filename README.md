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

Runs our Little German Language.

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
### Arithmetic
We implemented all the basic arithmetic operations. 

In addition to the normal `do_addieren` and `do_multiplizieren` operations, we also implemented `do_summe` and 
`do_produkt`, which accept a variable number of arguments and add, resp. multiply, all of these values.

### Print with `do_ausdrucken`
Our implementation can handle any number of arguments and will print them all.

Interesting implementation details:
- If a string "-nobr" is passed, we print without line-break at the end.
- If a string "-title" is passed, we colour printout green.

### While loop with `do_solange`
Our implementation expects two expressions (lists in Python):
- A condition
- An operation

Interesting implementation details:
- We implement repetition using recursive function calls.

### Arrays with `do_liste`
Arrays of fixed length are set by passing the length of the array as the first argument, and the elements of the array as the remaining arguments.

```json
["abfolge", 
    ["variable_setzen", "beispiel_liste",
        ["liste", 3, 1, "Wort", 3.14]
    ],
    ["ausdrucken",
        ["variable_abrufen", "beispiel_liste"]
    ]
]
```

The above prints `[1, 'Wort', 3.14]`.

### Object System
Classes and objects LGL are Python dictionaries:

Class:
```Python
example_class = {
    "_classname": "example_class",
    "_parent": None,
    "_new": ["konstrukteur", params, body],
    "method":  ["methode", params, body]}
```

Object:
```Python
example_object = {
    "_class": example_class,
    "attribute": attribute}
```

### Tracing
We implemented the tracing as a decorator `@trace` function that wraps the function `do()`. 

By default, **we use `time.perf_counter()` to measure performance**. If you wish to use `datetime.datetime.now()`, the option is available by setting an additional `--usedatetime` flag when using `lgl_interpreter.py` with `--trace`. 

When tracing, we **write output immediately to the file**. A more mature implementation should write the file at the end of the tracing, so as not to add extra execution time.

### Reporting
`reporting.py` automatically detects and properly handles either kind of timestamp.

