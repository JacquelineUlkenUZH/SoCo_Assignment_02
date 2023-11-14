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
    "-t", "--trace", help="Log details of start and end times to FILENAME"
)
parser.add_argument("-p", "--perf", action="store_true",
                    help="Use the superior perf_counter to trace execution times (recommended)")
cargs = parser.parse_args()


############
# Comments #
############
def do_kommentar(envs, args):
    """Ignores any instructions.

    Syntax:
        ["kommentar", "Dies ist ein Kommentar."]
    Returns:
        None
    """

    return None


#############
# None Type #
#############
def do_leer(envs, args):
    """None

    Syntax:
        ["leer"]
    Returns:
        None
    """
    assert len(args) == 0, f"Ungültige Anzahl Argumente. Erwartet: 0, Gegeben: {len(args)}."

    return None


########################
# Printing and tracing #
########################
def trace(func):
    """Wraps a function to log its start and end times to a file.

    Syntax:
        Use decorator: @trace
    Behaviour:
        Wraps timer around the function call and writes a file.
    """

    def wrapper(envs, expr):
        if not cargs.trace: return func(envs, expr)
        if not isinstance(expr, list): return func(envs, expr)
        uid = str(uuid.uuid4().fields[0])[:6]
        # Functions are in expr[0], methods in expr[1], hence:
        function_name = expr[0] if not isinstance(expr[0], list) else expr[1]
        time_start = datetime.now() if not cargs.perf else time.perf_counter()
        with open(cargs.trace, "a") as logfile:
            logfile.write(f"{uid},{function_name},start,{time_start}\n")
        result = func(envs, expr)
        time_stop = datetime.now() if not cargs.perf else time.perf_counter()
        with open(cargs.trace, "a") as logfile:
            logfile.write(f"{uid},{function_name},stop,{time_stop}\n")
        return result

    return wrapper


def do_ausdrucken(envs, args):
    """Prints an expression to the console.

    Syntax:
        ["ausdrucken"]
            - prints a linebreak.
        ["ausdrucken", expr1, expr2, ...]
            -> print(expr1, expr2, ...)
        ["ausdrucken", expr1, expr2, ..., "nobr"]
            -> print(expr1, expr2, ..., end="")
            - no linebreak at the end.
        ["ausdrucken", expr1, expr2, ..., "title"]
            -> print(expr1, expr2, ...)
            - prints in green
    Returns:
        None
    """

    nobr = "-nobr" in args
    try:
        args.remove("-nobr")
    except ValueError:
        pass
    title = "-title" in args
    try:
        args.remove("-title")
    except ValueError:
        pass
    result = ""
    for arg in args:
        expr = do(envs, arg)
        # Special printing for lists
        if isinstance(expr, list) and expr[0] == "liste":
            result += str(expr[2:])
        else:
            result += str(expr)
    if title:
        result = "\033[92m" + result + "\033[0m"  # Green
    if nobr:
        print(result, end="")
    else:
        print(result)

    return None


##############
# Arithmetic #
##############
def do_addieren(envs, args):
    """Adds two numbers.

    Syntax:
        ["addieren", a, b]
    Returns:
        a + b
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    return do(envs, args[0]) + do(envs, args[1])


def do_summe(envs, args):
    """Calculates the sum of the given numbers.

    Syntax:
        ["summe", a, b, c, ...]
    Returns:
        a + b + c + ...
    """

    s = 0
    for arg in args:
        s += do(envs, arg)

    return s


def do_subtrahieren(envs, args):
    """Subtracts the second from the first number.

    Syntax:
        ["subtrahieren", a, b]
    Returns:
        a - b
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    return do(envs, args[0]) - do(envs, args[1])


def do_multiplizieren(envs, args):
    """Multiplies the two numbers.

    Syntax:
        ["multiplizieren", a, b]
    Returns:
        a * b
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    return do(envs, args[0]) * do(envs, args[1])


def do_produkt(envs, args):
    """Calculates the product of the given numbers.

    Syntax:
        ["produkt", a, b, c, ...]
    Returns:
        a * b * c * ...
    """

    p = 1
    for arg in args:
        p *= do(envs, arg)

    return p


def do_dividieren(envs, args):
    """Divides the first number by the second number.

    Syntax:
        ["dividieren", a, b]
    Returns:
        a / b
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    return do(envs, args[0]) / do(envs, args[1])


def do_potenzieren(envs, args):
    """Raises the first number to the second number's power.

    Syntax:
        ["potenzieren", a, b]
    Returns:
        a ** b
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    return do(envs, args[0]) ** do(envs, args[1])


def do_absolutwert(envs, args):
    """Absolute value

    Syntax:
        ["absolutwert", a]
    Returns:
        abs(a)
    """
    assert len(args) == 1, f"Ungültige Anzahl Argumente. Erwartet: 1, Gegeben: {len(args)}."

    return abs(do(envs, args[0]))


##############
# Comparison #
##############
def do_gleich(envs, args):
    """Equals

    Syntax:
        ["gleich", a, b]
    Returns:
        a == b
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    return do(envs, args[0]) == do(envs, args[1])


def do_kleiner_als(envs, args):
    """Less than

    Syntax:
        ["kleiner_als", a, b]
    Returns:
        a < b
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    return do(envs, args[0]) < do(envs, args[1])


def do_kleiner_gleich(envs, args):
    """Less or equal

    Syntax:
        ["kleiner_gleich", a, b]
    Returns:
        a <= b
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    return do(envs, args[0]) <= do(envs, args[1])


def do_groesser_als(envs, args):
    """Greater than

    Syntax:
        ["groesser_als", a, b]
    Returns:
        a > b
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    return do(envs, args[0]) > do(envs, args[1])


def do_groesser_gleich(envs, args):
    """Greater or equal

    Syntax:
        ["groesser_gleich", a, b]
    Returns:
        a >= b
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    return do(envs, args[0]) >= do(envs, args[1])


#########
# Logic #
#########
def do_wahr(envs, args):
    """True

    Syntax:
        ["wahr"]
    Returns:
        True
    """
    assert len(args) == 0, f"Ungültige Anzahl Argumente. Erwartet: 0, Gegeben: {len(args)}."

    return True


def do_falsch(envs, args):
    """False

    Syntax:
        ["falsch"]
    Returns:
        False
    """
    assert len(args) == 0, f"Ungültige Anzahl Argumente. Erwartet: 0, Gegeben: {len(args)}."

    return False


def do_nicht(envs, args):
    """Logical not.

    Syntax:
        ["nicht", a]
    Returns:
        not a
    """
    assert len(args) == 1, f"Ungültige Anzahl Argumente. Erwartet: 1, Gegeben: {len(args)}."

    return not do(envs, args[0])


def do_und(envs, args):
    """Logical and

    Syntax:
        ["und", a, b]
    Returns:
        a and b
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    return do(envs, args[0]) and do(envs, args[1])


def do_oder(envs, args):
    """Logical or

    Syntax:
        ["oder", a, b]
    Returns:
        a or b
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    return do(envs, args[0]) or do(envs, args[1])


#############
# Variables #
#############
def do_variable_setzen(envs, args):
    """Sets a variable in the environment.

    Syntax:
        ["variable_setzen", name, wert]
    Returns:
        None
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    var_name = args[0]
    assert isinstance(var_name, str), f"Variablenname muss eine Zeichenfolge sein."
    value = do(envs, args[1])
    set_envs(envs, var_name, value)

    return None


def do_variable_abrufen(envs, args):
    """Gets the value of a variable.

    Syntax:
        ["variable_abrufen", name]
    Returns:
        value
    """
    assert len(args) == 1, f"Ungültige Anzahl Argumente. Erwartet: 1, Gegeben: {len(args)}."

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
    assert len(args) > 1, f"Ungültige Anzahl Argumente. Erwartet mindestens 2 Argumente."

    length = do(envs, args[0])
    elements = args[1:]
    assert len(elements) == length, f"Angegebene Länge stimmt nicht mit der Anzahl Elemente überein!"

    for element in elements:
        do(envs, element)

    return ["liste", length] + elements


def do_element_abrufen(envs, args):
    """Gets the element at the given index of a list.

    Syntax:
        ["element_abrufen", liste, index]
    Returns:
        liste[idx]
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    lst = do(envs, args[0])
    assert isinstance(lst, list), f"{lst} ist keine Liste!"
    assert lst[0] == "liste", f"{lst} ist keine Liste!"

    idx = do(envs, args[1])
    assert 0 <= idx <= lst[1], f"Ungültiger index {idx}."

    return lst[2 + idx]


def do_element_setzen(envs, args):
    """Sets the element at the given index of a list.

    Syntax:
        ["element_setzen", liste, index, element]
    Returns:
        None
    """
    assert len(args) == 3, f"Ungültige Anzahl Argumente. Erwartet: 3, Gegeben: {len(args)}."

    lst = do(envs, args[0])
    assert isinstance(lst, list), f"{lst} ist keine Liste!"
    assert lst[0] == "liste", f"{lst} ist keine Liste!"

    idx = do(envs, args[1])
    assert 0 <= idx <= lst[1], f"Ungültiger index {idx}."

    element = do(envs, args[2])
    lst[2 + idx] = element

    return None


################
# Dictionaries #
################
def do_lexikon(envs, args):
    """Creates a dictionary with the given key-value pairs.

    Syntax:
        ["lexikon", [etikett1, eintrag1], [etikett2, eintrag2], ...]
    Returns:
        {etikett1: eintrag1, etikett2: eintrag2, ...}
    """
    assert len(args) > 0, f"Ungültige Anzahl Argumente. Erwartet mindestens 1 Argument."
    assert all([len(arg) == 2 for arg in args]), f"Alle Argumente müssen Länge 2 haben: [etikett, eintrag]."

    d = {}
    for arg in args:
        key = do(envs, arg[0])
        value = do(envs, arg[1])
        d[key] = value

    return d


def do_eintrag_abrufen(envs, args):
    """Gets the entry at the given key of a dictionary.

    Syntax:
        ["element_abrufen", lexikon, etikett]
    Returns:
        lexikon[etikett]
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    dictionary = do(envs, args[0])
    assert isinstance(dictionary, dict), f"{dictionary} ist kein Lexikon!"

    key = do(envs, args[1])

    return dictionary[key]


def do_eintrag_setzen(envs, args):
    """Sets the entry at the given key of a dictionary.

    Syntax:
        ["eintrag_setzen", lexikon, etikett, eintrag]
    Returns:
        None
    """
    assert len(args) == 3, f"Ungültige Anzahl Argumente. Erwartet: 3, Gegeben: {len(args)}."

    dictionary = do(envs, args[0])
    assert isinstance(dictionary, dict), f"{dictionary} ist kein Lexikon!"

    key = do(envs, args[1])
    assert key in dictionary, f"Etikett {key} existiert nicht im Lexikon!"

    entry = do(envs, args[2])
    dictionary[key] = entry

    return None


def do_lexika_vereinen(envs, args):
    """Merge two dictionaries.

    Syntax:
        ["lexika_vereinen", lexikon1, lexikon2]
    Returns:
        lexikon1 | lexikon2
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    dict1 = do(envs, args[0])
    assert isinstance(dict1, dict), f"{dict1} ist kein Lexikon!"

    dict2 = do(envs, args[1])
    assert isinstance(dict2, dict), f"{dict2} ist kein Lexikon!"

    return dict1 | dict2


#############
# Functions #
#############
def do_funktion(envs, args):
    """Creates a new function.

    Syntax:
        ["funktion", params, body]
    Returns:
        ["funktion", params, body]
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    params = args[0]
    body = args[1]

    return ["funktion", params, body]

@trace
def do_funktion_aufrufen(envs, args):
    """Executes a given function with the given arguments.

    Syntax:
        ["funktion_aufrufen", name, arg1, arg2, ...]
    Returns:
        name(arg1, arg2, ...)
    """

    assert len(args) > 0, f"Ungültige Anzahl Argumente. Erwartet mindestens 1 Argument."

    name = do(envs, args[0])
    func = get_envs(envs, name)
    assert isinstance(func, list), f"{func} ist keine Funktion!"
    assert func[0] == "funktion", f"{func} ist keine Funktion!"

    arguments = args[1:]
    values = [do(envs, arg) for arg in arguments]
    params = func[1]
    assert len(params) == len(
        values), f"Ungültige Anzahl Argumente für Funktion {name}. Erwartet {len(params)} Argumente."

    envs.append(dict(zip(params, values)))

    body = func[2]
    result = do(envs, body)
    envs.pop()

    return result


###########
# Objects #
###########
def is_lgl_class(cls):
    """Helper function to determine if something is an LGL class."""

    if not isinstance(cls, dict):
        return False
    if "_classname" not in cls or not isinstance(cls["_classname"], str):
        return False
    if "_new" not in cls or not (cls["_new"][0] == "konstrukteur"):
        return False
    if "_parent" not in cls or not (cls["_parent"] is None or is_lgl_class(cls["_parent"])):
        return False

    return True


def do_klasse(envs, args):
    """Creates a new class.

    Syntax:
        ["klasse", name, vorfahre, ["konstrukteur", params, body], {"methode1": ["methode", params1, body1], "methode2": ["methode", params2, body2], ...}]
    Returns:
        {"_classname": name,
        "_parent": vorfahre,
        "_new": ["konstrukteur", params, body],
        "methode1":  ["methode", params1, body1],
        "method2": ["methode", params2, body2],
        ...}
    """
    assert len(args) == 4, f"Ungültige Anzahl Argumente. Erwartet: 4, Gegeben: {len(args)}."

    name = do(envs, args[0])
    assert isinstance(name, str), f"Klassennname muss eine Zeichenfolge sein."

    parent = do(envs, args[1])
    assert parent is None or is_lgl_class(parent), f'Vorfahre muss entweder ["leer"] oder eine Klasse sein.'

    new = do(envs, args[2])
    assert isinstance(new, list), f"{new} ist kein Konstrukteur!"
    assert new[0] == "konstrukteur", f"{new} ist kein Konstrukteur!"

    methods = do(envs, args[3])
    assert isinstance(methods, dict), f"{methods} ist kein Lexikon!"

    cls_base = {
        "_classname": name,
        "_parent": parent,
        "_new": new
    }

    return cls_base | methods


def is_lgl_object(obj):
    """Helper function to determine if something is an LGL object."""

    if not isinstance(obj, dict):
        return False
    if "_class" not in obj or not is_lgl_class(obj["_class"]):
        return False

    return True


def do_objekt(envs, args):
    """Creates an instance of a class.

    Syntax:
        ["objekt", klasse, eigenschaft1, eigenschaft2, ...]
    Returns:
        {"_class": klasse,
        "eigenschaft1": eigenschaft1,
        "eigenschaft2": eigenschaft2,
        ...}
    """
    assert len(args) > 0, f"Ungültige Anzahl Argumente. Erwartet mindestens 1 Argument."

    cls = do(envs, args[0])
    assert is_lgl_class(cls), f"{cls} ist keine Klasse!"

    new = cls["_new"]
    assert isinstance(new, list), f"{new} ist kein Konstrukteur!"
    assert new[0] == "konstrukteur", f"{new} ist kein Konstrukteur!"

    arguments = args[1:]
    values = [do(envs, arg) for arg in arguments]
    params = new[1]
    assert len(params) == len(
        values), f"Ungültige Anzahl Argumente für Konstrukteur {cls['_classname']}. Erwartet {len(params)} Argumente."

    envs.append(dict(zip(params, values)))
    body = new[2]
    obj = do(envs, body)
    envs.pop()

    obj["_class"] = cls

    return obj


def do_konstrukteur(envs, args):
    """Creates a constructor for a class. The constructor is called when a new instance of a class is created.

    Syntax:
        ["konstrukteur", params, body]
    Returns:
        ["konstrukteur", params, body]
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    params = args[0]
    body = args[1]
    assert body[0] == "lexikon", f"Konstrukteur muss ein Lexikon mit Klassenattributen zurückgeben."

    return ["konstrukteur", params, body]


def do_methode(envs, args):
    """Creates a new method for a class. The body has access to the object by using the variable "instanz".

    Syntax:
        ["methode", params, body]
    Returns:
        ["methode", params, body]
    """
    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    params = args[0]
    assert "instanz" not in params, f"Parameter 'instanz' darf nicht überschrieben werden."

    body = args[1]

    return ["methode", params, body]

@trace
def do_methode_aufrufen(envs, args):
    """Call a method on a given instance.

    Syntax:
        ["methode_aufrufen", instanz, methoden_name, argument1, argument2, ...]
    Returns:
        method(instanz, argument1, argument2, ...)
    """

    assert len(args) > 1, f"Ungültige Anzahl Argumente. Erwartet mindestens 2 Argumente."

    instance = do(envs, args[0])
    assert is_lgl_object(instance), f"{instance} ist kein Objekt!"

    name = do(envs, args[1])
    assert isinstance(name, str), f"Ungültiger Methodenname."

    method = find_method(instance["_class"], name)
    assert isinstance(method, list), f"{method} ist keine Methode!"
    assert method[0] == "methode", f"{method} ist keine Methode!"

    arguments = args[2:]
    values = [do(envs, arg) for arg in arguments]
    values.append(instance)
    params = method[1].copy()
    params.append("instanz")
    assert len(params) == len(
        values), f"Ungültige Anzahl Argumente für Methode {name}. Erwartet {len(params)} Argumente."

    envs.append(dict(zip(params, values)))
    body = method[2]
    result = do(envs, body)
    envs.pop()

    return result


def find_method(cls, method_name):
    """Helper function to find a method in a class."""

    if method_name in cls:
        return cls[method_name]
    else:
        assert cls["_parent"], f"{method_name} ist nicht implementiert."
        return find_method(cls["_parent"], method_name)


################
# Control Flow #
################
def do_abfolge(envs, args):
    """Executes all the given operations one after the other.

    Syntax:
        ["abfolge", expr1, expr2, ...]
    Returns:
        None
    """

    for operation in args:
        do(envs, operation)

    return None


def do_solange(envs, args):
    """Executes the given operation as long as the condition remains true.

    Syntax:
        ["solange", kondition, operation]
    Returns:
        None
    """

    assert len(args) == 2, f"Ungültige Anzahl Argumente. Erwartet: 2, Gegeben: {len(args)}."

    condition = args[0]
    operation = args[1]

    if do(envs, condition):
        do(envs, operation)
        do_solange(envs, [condition, operation])

    return None


OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}



def do(envs, expr):
    """Evaluates the given expression."""

    # Lists trigger function calls
    if isinstance(expr, list):
        assert expr[0] in OPS, f"Unbekannte Operation '{expr[0]}'."
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
    """Gets the value of a variable in the environment."""

    assert isinstance(name, str)

    for e in reversed(envs):
        if name in e:
            return e[name]

    assert False, f"Unbekannte Variable '{name}'."


def set_envs(envs, name, value):
    """Sets the value of a variable in the environment."""

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
