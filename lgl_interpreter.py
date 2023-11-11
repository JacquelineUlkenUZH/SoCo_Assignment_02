import argparse
import json
import os
import uuid
import datetime

###################
# Parse arguments #
###################

abspath = os.path.dirname(os.path.abspath(__file__))
os.chdir(abspath)

parser = argparse.ArgumentParser(
    prog="lgl_interpreter.py",
    description="Runs our little German programming language.",
    epilog="",
)
# nargs="+" means "at least one"
parser.add_argument("files", nargs="+", help="Specify lgl source files to run")
parser.add_argument(
    "--trace", help="Log details of start and end times to FILENAME"
)
cargs = parser.parse_args()

############
# Comments #
############
def do_kommentar(envs, args):
    """Ignore any instructions.

    Syntax:
        ["kommentar", "Dies ist ein Kommentar."]
    Returns:
        None
    """

    return None


############
# Printing #
############
def do_ausdrucken(envs, args):
    """Prints an expression to the console.

    Syntax:
        ["ausdrucken", expr]
        ["ausdrucken", expr, "nobr"] -> no linebreak at the end
        ["ausdrucken", expr, "title"] -> print in green
    Returns:
        None
    """
    assert len(args) > 0
    nobr = "nobr" in args
    title = "title" in args
    for arg in args:
        result = do(envs, arg)
        if title:
            args.remove("title")
            result = "\033[92m" + result + "\033[0m"  # Green
        if nobr:
            args.remove("nobr")
            print(result, end="")
        else:
            print(result)
    return None


##############
# Arithmetic #
##############
def do_addieren(envs, args):
    """Add two numbers.

    Syntax:
        ["addieren", a, b]
    Returns:
        a + b
    """

    assert len(args) == 2
    return do(envs, args[0]) + do(envs, args[1])


def do_subtrahieren(envs, args):
    """Subtract the second from the first number

    Syntax:
        ["subtrahieren", a, b]
    Returns:
        a - b
    """

    assert len(args) == 2
    return do(envs, args[0]) - do(envs, args[1])


def do_multiplizieren(envs, args):
    """Multiplies two numbers

    Syntax:
        ["multiplizieren", a, b]
    Returns:
        a * b
    """

    assert len(args) == 2
    return do(envs, args[0]) * do(envs, args[1])


def do_produkt(envs, args):
    """Calculates the product of the given numbers

    Syntax:
        ["produkt", a, b, c, ...]
    Returns:
        a * b * c * ...
    """

    assert len(args) > 1
    product = 1
    for arg in args:
        product *= do(envs, arg)
    return product


def do_dividieren(envs, args):
    """Divide the first number by the second number

    Syntax:
        ["dividieren", a, b]
    Returns:
        a / b
    """
    assert len(args) == 2
    return do(envs, args[0]) / do(envs, args[1])


def do_potenzieren(envs, args):
    """Raises the first number to the second number's power

    Syntax:
        ["potenzieren", a, b]
    Returns:
        a ** b
    """

    assert len(args) == 2
    return do(envs, args[0]) ** do(envs, args[1])


def do_absolutwert(envs, args):
    """Absolute value

    Syntax:
        ["absolutwert", a]
    Returns:
        abs(a)
    """

    assert len(args) == 1
    return abs(do(envs, args[0]))


##############
# Comparison #
##############
def do_gleich(envs, args):
    """Equates two expressions

    Syntax:
        ["gleich", a, b]
    Returns:
        a == b
    """

    assert len(args) == 2
    return do(envs, args[0]) == do(envs, args[1])


def do_kleiner_als(envs, args):
    """Smaller than

    Syntax:
        ["kleiner_als", a, b]
    Returns:
        a < b
    """

    assert len(args) == 2
    return do(envs, args[0]) < do(envs, args[1])


def do_groesser_als(envs, args):
    """Greater than

    Syntax:
        ["groesser_als", a, b]
    Returns:
        a > b
    """

    assert len(args) == 2
    return do(envs, args[0]) > do(envs, args[1])


#########
# Logic #
#########
def do_nicht(envs, args):
    """Logical not

    Syntax:
        ["nicht", a]
    Returns:
        not a
    """

    assert len(args) == 1
    return not do(envs, args[0])


def do_und(envs, args):
    """Logical and

    Syntax:
        ["und", a, b]
    Returns:
        a and b
    """

    assert len(args) == 2
    return do(envs, args[0]) and do(envs, args[1])


def do_oder(envs, args):
    """Logical or

    Syntax:
        ["oder", a, b]
    Returns:
        a oder b
    """

    assert len(args) == 2
    return do(envs, args[0]) or do(envs, args[1])


#############
# Variables #
#############
def do_variable_setzen(envs, args):
    assert len(args) == 2 or len(args) == 3
    assert isinstance(args[0], str)
    var_name = args[0]
    value = do(envs, args[1])
    if isinstance(value, str) and value.startswith("[") and value.endswith("]"):
        value = eval(value)  # Convert string to list
    if len(args) == 3:
        assert isinstance(args[2], int)
        liste = get_envs(envs, var_name)
        index = args[2]
        liste[index] = value
        return value
    set_envs(envs, var_name, value)
    return value


def do_variable_abrufen(envs, args):
    assert len(args) == 1 or len(args) == 2
    if len(args) == 2:
        assert isinstance(args[1], int)
        liste = get_envs(envs, args[0])
        index = args[1]
        return liste[index]
    return get_envs(envs, args[0])


##########
# Arrays #
##########
def do_liste(envs, args):
    """Creates a list of the given length with the given elements. We surround the list with a tuple, to not trigger function calls.

    Syntax:
        ["liste", a, element_1, element_2, ...]
    Returns:
        [element_1, element_2, ... ]
    """

    assert len(args) > 1
    length = do(envs, args[0])
    elements = args[1:]
    assert len(elements) == length, f"Angegebene Länge stimmt nicht mit der Anzahl Elemente überein!"
    for element in elements:
        do(envs, element)
    return elements


def do_element_abrufen(envs, args):
    """Get the element at the given index of a liste.

    Syntax:
        ["element_abrufen", liste, index]
    Returns:
        liste[0][idx]
    """

    assert len(args) == 2
    lst = do(envs, args[0])
    idx = do(envs, args[1])
    assert isinstance(lst, tuple) and isinstance(lst[0], list), f"{lst} ist keine Liste"
    assert 0 <= idx <= len(lst[0]) - 1, f"Ungültiger index {idx}."

    return lst[0][idx]


def do_element_setzen(envs, args):
    """Set the element at the given index of a liste.

    Syntax:
        ["element_setzen", liste, index, element]
    Returns:
        None
    """

    assert len(args) == 3
    lst = do(envs, args[0])
    idx = do(envs, args[1])
    element = do(envs, args[2])
    assert isinstance(lst, tuple) and isinstance(lst[0], list), f"{lst} ist keine Liste."
    assert 0 <= idx <= len(lst[0]) - 1, f"Ungültiger index {idx}."
    lst[0][idx] = element
    return None


################
# Dictionaries #
################


def do_lexikon(envs, args):
    """Creates a lexikon.
    Input example: [["a", 1], ["b", 2]]
    Output: {"a": 1, "b": 2}
    """
    assert len(args) >= 1, "Zu wenig Argumente für das Lexikon"
    assert all([len(arg) == 2 for arg in args]), "Alle Argumente müssen Länge 2 haben: [key, value]"
    d = {}
    for arg in args:
        key = arg[0]
        value = arg[1]
        d[key] = value
    return d


def do_eintrag_abrufen(envs, args):
    """Get the entry at the given key of a lexikon.

    Syntax:
        ["element_abrufen", lexikon, etikett]
    Returns:
        entry at the given key
    """

    assert len(args) == 2
    lexikon = do(envs, args[0])
    key = do(envs, args[1])
    assert isinstance(lexikon, dict), f"{lexikon} ist kein Lexikon."
    return lexikon[key]


def do_eintrag_setzen(envs, args):
    """Set the entry at the given index of a lexikon.

    Syntax:
        ["eintrag_setzen", lexikon, etikett, eintrag]
    Returns:
        None
    """

    assert len(args) == 3
    lexikon = do(envs, args[0])
    key = do(envs, args[1])
    entry = do(envs, args[2])
    assert isinstance(lexikon, dict), f"{lexikon} ist kein Lexikon."
    assert key in lexikon, f"{key} existiert nicht im Lexikon."
    lexikon[key] = entry


#############
# Functions #
#############
def do_funktion(envs, args):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["funktion", params, body]


def do_funktion_aufrufen(envs, args):
    assert len(args) >= 1
    name = args[0]
    arguments = args[1:]
    # eager evaluation
    values = [do(envs, arg) for arg in arguments]

    func = get_envs(envs, name)
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


################
# Control Flow #
################
def do_abfolge(envs, args):
    for operation in args:
        do(envs, operation)
    return None


def do_solange(envs, args, previousresult=None):
    # Passing previousresult recursively because otherwise last iteration would be None
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
        return do_solange(envs, args, previousresult)
    else:
        return previousresult


def do_solange_alt(envs, args):
    assert len(args) == 2
    condition = args[0]
    operation = args[1]
    if do(envs, condition):
        do(envs, operation)
        do_solange_alt(envs, [condition, operation])
    return None


OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}

def trace(func):
    def wrapper(envs, expr):
        if not cargs.trace: return func(envs, expr)
        if not isinstance(expr, list): return func(envs, expr)
        with open(cargs.trace, "a") as logfile:
            uid = str(uuid.uuid4().fields[0])[:6]
            functionname = expr[0]
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            logfile.write(f"{uid},{functionname},start,{timestamp}\n")
            result = func(envs, expr)
            logfile.write(f"{uid},{functionname},stop,{timestamp}\n")
            return result
    return wrapper

@trace
def do(envs, expr):
    # Lists trigger function calls
    if isinstance(expr, list):
        assert expr[0] in OPS, f"Unknown operation {expr[0]}"
        func = OPS[expr[0]]
        return func(envs, expr[1:])
    # Everything else returns itself
    else:
        return expr


###############
# Environment #
###############
def get_envs(envs, name):
    assert isinstance(name, str)
    for e in reversed(envs):
        if name in e:
            return e[name]
    assert False, f"Unknown variable name {name}"


def set_envs(envs, name, value):
    assert isinstance(name, str)
    envs[-1][name] = value


### OOP ###


def shape_new(name):
    pass


def shape_density(thing, weight):
    area = call(thing, "area")
    return weight / area


Shape = {
    "density": shape_density,
    "_classname": "Shape",
    "_parent": None
}


############## SQUARE #################


def square_area(instance):
    return instance["side"] ** 2


Square = {
    "area": square_area,
    "_classname": "Square",
    "_parent": Shape
}


def square_new(name, side):
    square_obj = {
        "name": name,
        "side": side,
        "_class": Square
    }
    return square_obj


############## CIRCLE #################

def circle_area(instance):
    return instance['radius_length'] ** 2 * 3.14


Circle = {
    "area": circle_area,
    "_classname": "Circle",
    "_parent": Shape
}


def circle_new(name, radius):
    circle_obj = {
        "name": name,
        "radius_length": radius,
        "_class": Circle
    }
    return circle_obj


########### HELPER FUNCTION #############
def call(instance, method_name, *args):
    method = find(instance["_class"], method_name)
    return method(instance, *args)


def find(cls, method_name):
    if method_name in cls:
        return cls[method_name]
    else:
        if cls["_parent"] == None:
            raise NotImplementedError(f" {method_name} is not implemented")
        else:
            return find(cls["_parent"], method_name)


########### MAIN EXECUTION #############

# square = square_new("sq", 3)
# circle = circle_new("ci", 2)
# square_density = call(square, "density", 5)
# circle_density = call(circle, "density", 5)
# sum_of_shapes = square_density + circle_density
# print(f"sum of density is {sum_of_shapes}")


def main():
    
    if cargs.trace:
        assert isinstance(cargs.trace, str)
        with open(cargs.trace, "w") as logfile:
            logfile.write("id,function_name,event,timestamp\n")
    
    # Run all files in order
    for file in cargs.files:
        file = os.path.join(abspath, file)
        assert os.path.exists(file), f"File {file} does not exist"
        with open(file, "r") as source_file:
            program = json.load(source_file)
        assert isinstance(program, list)
        envs = [{}]
        result = do(envs, program)
        return result


if __name__ == "__main__":
    main()
