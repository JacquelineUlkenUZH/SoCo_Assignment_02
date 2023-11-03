import argparse
import json
import os

abspath = os.path.dirname(os.path.abspath(__file__))
os.chdir(abspath)

###################################
# From here we add do_ operations #
###################################


# Arithmetic
def do_addieren(envs, args):
    assert len(args) == 2
    left = do(envs, args[0])
    right = do(envs, args[1])
    return left + right


def do_subtrahieren(envs, args):
    assert len(args) == 2
    left = do(envs, args[0])
    right = do(envs, args[1])
    return left - right


def do_dividieren(envs, args):
    assert len(args) == 2
    left = do(envs, args[0])
    right = do(envs, args[1])
    return left / right


def do_potenzieren(envs, args):
    assert len(args) == 2
    left = do(envs, args[0])
    right = do(envs, args[1])
    return left**right


def do_multiplizieren(envs, args):
    assert len(args) >= 2
    product = 1
    for arg in args:
        product *= do(envs, arg)
    return product


def do_absolutwert(envs, args):
    assert len(args) == 1
    value = do(envs, args[0])
    return abs(value)


# Variables
def do_varsetzen(envs, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    var_name = args[0]
    value = do(envs, args[1])
    envs_set(envs, var_name, value)
    return value


def do_varabrufen(envs, args):
    assert len(args) == 1
    return envs_get(envs, args[0])


# Functions
def do_funktion(envs, args):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["funktion", params, body]


def do_funkaufrufen(envs, args):
    assert len(args) >= 1
    name = args[0]
    arguments = args[1:]
    # eager evaluation
    values = [do(envs, arg) for arg in arguments]

    func = envs_get(envs, name)
    assert isinstance(func, list)
    assert func[0] == "funktion"
    func_params = func[1]
    assert len(func_params) == len(values)

    local_frame = dict(zip(func_params, values))
    envs.append(local_frame)
    body = func[2]
    result = do(envs, body)
    envs.pop()

    return result


###############################################
# From here we add our calling infrastructure #
###############################################


def do(envs, expr):
    # Lists trigger function calls.
    if isinstance(expr, list):
        assert expr[0] in OPS, f"Unknown operation {expr[0]}"
        func = OPS[expr[0]]
        return func(envs, expr[1:])
    # Everything else returns itself
    else:
        return expr


def do_abfolge(envs, args):
    assert len(args) > 0
    for operation in args:
        result = do(envs, operation)
    return result


def do_ausdrucken(envs, args):
    assert len(args) > 0
    for arg in args:
        result = do(envs, arg)
        print(result)
    return result


def do_solange(envs, args, previousresult = None):
    # arg[0] = [Wert1] oder [Wert1, Vergleich, Wert2]
    # arg[1] = Liste der Abfolge
    assert len(args) == 2
    assert len(args[0]) == 1 or len(args[0]) == 3

    teststr = f"{do(envs, args[0][0])}"
    if len(args[0]) == 3:
        assert isinstance(args[0][1], str)
        teststr += f" {do(envs, args[0][1])} {do(envs, args[0][2])}"
    
    if eval(teststr):
        previousresult = do_abfolge(envs, args[1])
        return do_solange(envs, args, previousresult) # passing result because otherwise it would be None
    else:
        return previousresult

OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}

# Environment
def envs_get(envs, name):
    assert isinstance(name, str)
    for e in reversed(envs):
        if name in e:
            return e[name]
    assert False, f"Unknown variable name {name}"


def envs_set(envs, name, value):
    assert isinstance(name, str)
    envs[-1][name] = value


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(
        prog="lgl_interpreter.py",
        description="Runs our little germal programming language.",
        epilog="",
    )
    # nargs="+" means "at least one"
    parser.add_argument("files", nargs="+", help="Specify lgl source files to run")
    parser.add_argument(
        "--trace", help="Log details of start and end times to FILENAME"
    )
    args = parser.parse_args()

    # Run all files in order
    for file in args.files:
        file = os.path.join(abspath, file)
        assert os.path.exists(file), f"File {file} does not exist"
        with open(file, "r") as source_file:
            program = json.load(source_file)
        assert isinstance(program, list)
        envs = [{}]
        result = do(envs, program)
        print(result)


if __name__ == "__main__":
    main()
