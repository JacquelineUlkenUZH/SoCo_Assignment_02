import argparse
import json
import os
import uuid
from datetime import datetime
import time

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
    """Creates a list of the given length with the given elements.

    Syntax:
        ["liste", length, element_1, element_2, ...]
    Returns:
        ["liste", length, element_1, element_2, ...]
    """

    assert len(args) > 1
    length = do(envs, args[0])
    elements = args[1:]
    assert len(elements) == length, f"Angegebene Länge stimmt nicht mit der Anzahl Elemente überein!"
    for element in elements:
        do(envs, element)
    return ["liste", length] + elements


def do_element_abrufen(envs, args):
    """Get the element at the given index of a liste.

    Syntax:
        ["element_abrufen", liste, index]
    Returns:
        liste[idx]
    """

    assert len(args) == 2
    lst = do(envs, args[0])
    idx = do(envs, args[1])
    assert isinstance(lst, list), f"{lst} ist keine Liste"
    assert lst[0] == "liste", f"{lst} ist keine Liste"
    assert 0 <= idx <= len(lst) - 2, f"Ungültiger index {idx}."

    return lst[2 + idx]


def do_element_setzen(envs, args):
    """Set the element at the given index of a list.

    Syntax:
        ["element_setzen", liste, index, element]
    Returns:
        None
    """

    assert len(args) == 3
    lst = do(envs, args[0])
    idx = do(envs, args[1])
    assert isinstance(lst, list), f"{lst} ist keine Liste"
    assert lst[0] == "liste", f"{lst} ist keine Liste"
    element = do(envs, args[2])
    lst[2 + idx] = element

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
        key = do(envs, arg[0])
        value = do(envs, arg[1])
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


def do_lexika_vereinen(envs, args):
    """Merge two dictionaries.

    Syntax:
        ["lexika_vereinen", lexikon1, lexikon2]
    Returns:
        lexikon1 | lexikon2
    """

    dict1 = do(envs, args[0])
    dict2 = do(envs, args[1])

    return dict1 | dict2


#############
# Functions #
#############
def do_funktion(envs, args):
    """Create a new function

    Syntax:
        ["funktion", params, body]
    Returns:
        ["funktion", params, body]
    """
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["funktion", params, body]


def do_funktion_aufrufen(envs, args):
    assert len(args) >= 1
    name = args[0]
    arguments = args[1:]
    values = [do(envs, arg) for arg in arguments]

    func = get_envs(envs, name)
    assert isinstance(func, list)
    assert func[0] == "funktion"
    params, body = func[1], func[2]
    assert len(params) == len(values)

    envs.append(dict(zip(params, values)))
    result = do(envs, body)
    envs.pop()

    return result


###########
# Objects #
###########
def do_leer(envs, args):
    return None


def do_klasse(envs, args):
    """Creates a new class

    Syntax:
        ["klasse", name, vorfahre, ["funktion", params, body], {"methode1": methode1, "methode2": methode2, ...}]
    Returns:
        {"_classname": name,
        "_parent": vorfahre,
        "_new": ["funktion", params, body],
        "methode1": methode1,
        "method2": methode2,
        ...}
    """

    assert len(args) == 4
    classname = do(envs, args[0])
    parent = do(envs, args[1])
    new = args[2]
    methods = do(envs, args[3])
    assert isinstance(methods, dict), f"{methods} muss ein Lexikon sein"

    cls_base = {
        "_classname": classname,
        "_parent": parent,
        "_new": new
    }

    return cls_base | methods


def do_objekt(envs, args):
    """Creates an instance of a class

    Syntax:
        ["objekt", klasse, eigenschaft1, eigenschaft2, ...]
    Returns:
        {"_class": klasse,
        "eigenschaft1": eigenschaft1,
        "eigenschaft2": eigenschaft2,
        ...}
    """
    assert len(args) >= 1
    cls = do(envs, args[0])
    assert isinstance(cls, dict), f"{cls} muss eine Klasse sein"
    arguments = args[1:]
    new = cls["_new"]
    assert isinstance(new, list)
    assert new[0] == "konstrukteur"
    params = new[1].copy()
    body = new[2].copy()
    values = [do(envs, arg) for arg in arguments]
    assert len(params) == len(values)

    envs.append(dict(zip(params, values)))
    obj = do(envs, body)
    obj["_class"] = cls
    envs.pop()

    return obj


def do_konstrukteur(envs, args):
    """Create a constructor for a class.

    Syntax:
        ["konstrukteur", params, body]
    Returns:
        ["konstrukteur", params, body]
    """
    assert len(args) == 2
    params = args[0]
    body = args[1]
    assert body[0] == "lexikon", f"Konstrukteur muss ein Lexikon mit Klassenattributen zurückgeben."
    return ["konstrukteur", params, body]


def do_methode(envs, args):
    """Create a new method for a class. The body has access to the object by using the variable "instanz"

    Syntax:
        ["methode", params, body]
    Returns:
        ["methode", params, body]
    """
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["methode", params, body]


def do_methode_aufrufen(envs, args):
    """Call a method on a given instance.

    Syntax:
        ["methode", instance, method_name, argument1, argument2, ...]
    Returns:
        result of the method call
    """
    assert len(args) >= 2
    instance = do(envs, args[0])
    assert isinstance(instance, dict)
    method_name = do(envs, args[1])
    assert isinstance(method_name, str)
    arguments = args[2:]

    method = find_method(instance["_class"], method_name)
    assert isinstance(method, list)
    assert method[0] == "methode"

    params = method[1].copy()
    params.append("instanz")
    body = method[2].copy()

    values = [do(envs, arg) for arg in arguments]
    values.append(instance)

    assert len(params) == len(values)

    envs.append(dict(zip(params, values)))
    result = do(envs, body)
    envs.pop()

    return result


def find_method(cls, method_name):
    assert isinstance(cls, dict), f"{cls} ist keine Klasse."

    if method_name in cls:
        return cls[method_name]
    else:
        assert cls["_parent"], f"{method_name} ist nicht implementiert."
        return find_method(cls["_parent"], method_name)


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
        uid = str(uuid.uuid4().fields[0])[:6]
        functionname = expr[0]
        # time_start = datetime.now()
        time_start = time.perf_counter()
        with open(cargs.trace, "a") as logfile:
            logfile.write(f"{uid},{functionname},start,{time_start}\n")
        result = func(envs, expr)
        # time_stop = datetime.now()
        time_stop = time.perf_counter()
        with open(cargs.trace, "a") as logfile:
            logfile.write(f"{uid},{functionname},stop,{time_stop}\n")
        return result

    return wrapper


@trace
def do(envs, expr):
    # Lists trigger function calls
    if isinstance(expr, list):
        assert expr[0] in OPS, f"Unknown operation '{expr[0]}'."
        func = OPS[expr[0]]
        result = func(envs, expr[1:])
        return result
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


########### MAIN EXECUTION #############

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
