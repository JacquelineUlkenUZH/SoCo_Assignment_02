["abfolge",
  ["ausdrucken", ""],
  ["ausdrucken", "Welcome to our programming language: The Little German Language, LGL!"],

  ["ausdrucken", ""],
  ["ausdrucken", "### Basic arithmetic and variables ###"],
  ["ausdrucken", "We create a variable 'a' = 8. We then showcase basic math operations."],
  ["ausdrucken", ["varsetzen", "a", 8]],
  ["ausdrucken", "add 2"],
  ["ausdrucken", ["varsetzen", "a", ["addieren", ["varabrufen", "a"], 2]]],
  ["ausdrucken", "subtract 4"],
  ["ausdrucken", ["varsetzen", "a", ["subtrahieren", ["varabrufen", "a"], 4]]],
  ["ausdrucken", "divide by -3"],
  ["ausdrucken", ["varsetzen", "a", ["dividieren", ["varabrufen", "a"], -3]]],
  ["ausdrucken", "multiply with 3, 6 and -7 in one go"],
  ["ausdrucken", ["varsetzen", "a", ["multiplizieren", ["varabrufen", "a"], 3, 6, -7]]],
  ["ausdrucken", "to the power of 3"],
  ["ausdrucken", ["varsetzen", "a", ["potenzieren", ["varabrufen", "a"], 3]]],
  
  ["ausdrucken", ""],
  ["ausdrucken", "### While loop ###"],
  ["ausdrucken", "We create a=2 and b=20, then add 5 to a and 1 to b as long as a<b."],
  ["ausdrucken", ["varsetzen", "a", 2]],
  ["ausdrucken", ["varsetzen", "b", 20]],
  ["solange", [["varabrufen", "a"], "<", ["varabrufen", "b"]], [
    ["ausdrucken", "a = ", "nobr"],
    ["ausdrucken", ["varsetzen", "a", ["addieren", ["varabrufen", "a"], 5]]],
    ["ausdrucken", "b = ", "nobr"],
    ["ausdrucken", ["varsetzen", "b", ["addieren", ["varabrufen", "b"], 1]]]
  ]],
  
  ["ausdrucken", ""],
  ["ausdrucken", "### Lists ###"],
  ["ausdrucken", "We create [1, 'wort', True], retrieve the last position, change 'wort' to 'bike' and print the final list:"],
  ["ausdrucken", ["varsetzen", "a", "[1, 'wort', True]"]],
  ["ausdrucken", ["varabrufen", "a", 2]],
  ["ausdrucken", ["varsetzen", "a", "bike", 1]],
  ["ausdrucken", ["varabrufen", "a"]]
]
