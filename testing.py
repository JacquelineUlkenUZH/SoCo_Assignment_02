from lgl_interpreter import *


def test_functions_variables_init():
    program = json.loads(
        """[
  "abfolge",
  ["varsetzen", "meinefunktion", ["funktion", ["meinargument"], ["subtrahieren", 10, ["varabrufen", "meinargument"]]]],
  ["varsetzen", "variabel_a", ["funkaufrufen", "meinefunktion", 3]],
  ["varsetzen", "variabel_b", ["addieren", 2, 3]],
  ["addieren", ["varabrufen", "variabel_a"], ["varabrufen", "variabel_b"]]
]
"""
    )
    actual = do([{}], program)
    expected = 12
    assert actual == expected


def test_functions_variables_absolutwert():
    program = json.loads(
        """[
  "abfolge",
  ["varsetzen", "meinefunktion", ["funktion", ["meinargument"], ["absolutwert", ["varabrufen", "meinargument"]]]],
  ["varsetzen", "variabel_a", ["funkaufrufen", "meinefunktion", -3]],
  ["varsetzen", "variabel_b", ["addieren", 2, 3]],
  ["addieren", ["varabrufen", "variabel_a"], ["varabrufen", "variabel_b"]]
]
"""
    )
    actual = do([{}], program)
    expected = 8
    assert actual == expected


def test_multiply_two_values():
    program = json.loads(
        """[
  "abfolge",
  ["multiplizieren", -2, 3]
]
"""
    )
    actual = do([{}], program)
    expected = -6
    assert actual == expected


def test_multiply_multiple_values():
    program = json.loads(
        """[
  "abfolge",
  ["multiplizieren", -2, 3, 6, -7]
]
"""
    )
    actual = do([{}], program)
    expected = 252
    assert actual == expected


def test_while_addup():
    program = json.loads(
        """
        ["abfolge",
        ["varsetzen", "a", 0],
        ["solange", [["varabrufen", "a"], "<", 5], [
            ["varsetzen", "a", ["addieren", ["varabrufen", "a"], 1]]]]
        ]
    """
    )
    actual = do([{}], program)
    expected = 5
    assert actual == expected


def test_while_addup2():
    program = json.loads(
        """
        ["abfolge",
        ["varsetzen", "a", 0],
        ["solange", [["varabrufen", "a"], "!=", 56], [
            ["varsetzen", "a", ["addieren", ["varabrufen", "a"], 1]]]]
        ]
    """
    )
    actual = do([{}], program)
    expected = 56
    assert actual == expected


def test_while_defined():
    program = json.loads(
        """
        ["abfolge",
        ["varsetzen", "a", "True"],
        ["solange", [["varabrufen", "a"]], [
            ["varsetzen", "a", "False"],
            ["varsetzen", "erfolg", "solange executed"]            
        ]],
        ["varabrufen", "erfolg"]]
    """
    )
    actual = do([{}], program)
    expected = "solange executed"
    assert actual == expected


def test_division():
    program = json.loads(
        """[
  "abfolge",
  ["dividieren", -6, 3]
]
"""
    )
    actual = do([{}], program)
    expected = -2
    assert actual == expected


def test_power():
    program = json.loads(
        """[
  "abfolge",
  ["potenzieren", -6, 2]
]
"""
    )
    actual = do([{}], program)
    expected = 36
    assert actual == expected


# call all functions in global namespace
results = {"pass": 0, "fail": 0, "error": 0}
name, fnc = None, None
for name, fnc in globals().items():
    if name.startswith("test_") and callable(fnc):
        try:
            fnc()
            results["pass"] += 1
        except AssertionError:
            results["fail"] += 1
        except Exception:
            results["error"] += 1

print(f"pass {results['pass']}")
print(f"fail {results['fail']}")
print(f"error {results['error']}")
