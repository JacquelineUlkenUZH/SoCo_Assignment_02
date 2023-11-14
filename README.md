# SoCo Assignment 02
Assignment 2 for the course Software Construction 23HS 22BI0004. 

These are the files we hand in:
- `lgl_interpreter.py` interprets our implementation of the Little German Language, LGL.
- `example_operations.gsc` a rather beautifully formatted showcase of our lovely programming language.
- `example_class.gsc` showcases classes, objects, methods.
- `example_trace.gsc` showcases tracing execution times to a logfile.
- `reporting.py` consumes said logfile and reports execution time deltas in tabular form.

## Getting started
### Interpreter
usage: lgl_interpreter.py \[-h\] \[--trace TRACE\] \[--perf\] files \[files ...\]

Runs our Little German Language.

positional arguments:
  files          Specify lgl source files to run

options:
  -h, --help            show this help message and exit
  -t TRACE, --trace TRACE
                        Log details of start and end times to FILENAME
  -p, --perf     Use the superior perf_counter to trace execution times (recommended)

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
- A condition that will be evaluation each time
- An operation that will be executed if the condition is met.

We implement repetition using recursive function calls.

### Variables with `variable_setzen` and `variable_abrufen`
Variables are stored in the topmost environment dictionary using the helper function `set_envs()`.

Variables are retrieved by searching through the whole stack of environments in reversed order using the helper function `get_envs()`.

### Functions with `do_funktion`
Functions in LGL are a normal named variable set with `variable_setzen` whose value is a function.

A function is a list of three items:
- A string "funktion" declaring this to be a function.
- A single parameter or a list of parameters.
- A body of properly formatted LGL code.

Functions are executed using `funktion_aufrufen` providing the relevant arguments.

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

### Dictionaries with `do_lexikon`
Dictionaries are created and edited by passing a list as the argument where the first element is the key and the second is the value. If the key already exists, the new value will just overwrite the existing value.

```json
["abfolge", 
    ["variable_setzen", "person",
        ["lexikon", ["Name", "Alice"], ["Alter", "25"], ["Beruf", "Lehrerin"]]
    ],
    ["ausdrucken", "person = ", ["variable_abrufen", "person"]]
]
```

The above prints `person = {'Name': 'Alice', 'Alter': '25', 'Beruf': 'Lehrerin'}`.

### Object System
Classes and objects in LGL are Python dictionaries:

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

The user can define a new class with `do_klasse`, which takes a name, parent, constructor and a dictionary of methods.
The parent can either be `None` (written as `["leer"]` in LGL) or another class. We have implemented a helper function to check if the user provided a valid class as a parent. We chose to implement a special `do_konstrukteur` function, with an additional assert to check
that the user defined constructor returns a dictionary of attributes. Another perk of this is that this makes a class 
declaration more readable:

```json
["klasse", "Shape", ["leer"],
    ["konstrukteur", ["name"],
        ["lexikon",
            ["name", ["variable_abrufen", "name"]]
        ]
    ],
    ["lexikon",
        ["density",
            ["methode", ["weight"],
                ["dividieren", ["variable_abrufen", "weight"], ["methode_aufrufen", ["variable_abrufen", "instanz"], "area"]]
            ]
        ]
    ]
]
```
The `do_objekt` function calls the constructor of the given class to create an instance of it.

Similarily, we have a special `do_methode` function. If an expression is marked as a method, the `do_methode_aufrufen` 
automatically adds the parameter `instanz` containing the given object to the environment. This way users don't have to 
include this parameter in their method declaration, and any method will always have access to their respective object.

### Tracing
We implemented tracing of custom functions and methods using a function `trace()` that wraps `do_funktion_aufrufen()` and `do_methode_aufrufen()` using a decorator (`@trace`).

By default, we use `datetime.datetime.now()` to measure performance. If you wish to use the superior `time.perf_counter()`, the option is available by setting an additional `--perf` flag when using `lgl_interpreter.py` with `--trace`. 

When tracing, we write output immediately to the file. A more mature implementation could write the file at the end of the tracing, so as not to add extra execution time.

### Reporting
`reporting.py` automatically detects and properly handles either kind of timestamp and prints a summary as a table.

