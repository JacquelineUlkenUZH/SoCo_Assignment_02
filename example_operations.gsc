["abfolge",
  ["ausdrucken", ""],
  ["ausdrucken", "Welcome to our programming language: The Little German Language, LGL!"],

  ["ausdrucken", ""],
  ["ausdrucken", "### Basic arithmetic and variables ###", "title"],
  ["ausdrucken", "We create a variable 'a' = 8. We then showcase basic math operations."],
  ["ausdrucken", ["variable_setzen", "a", 8]],
  ["ausdrucken", "add 2"],
  ["ausdrucken", ["variable_setzen", "a", ["addieren", ["variable_abrufen", "a"], 2]]],
  ["ausdrucken", "subtract 4"],
  ["ausdrucken", ["variable_setzen", "a", ["subtrahieren", ["variable_abrufen", "a"], 4]]],
  ["ausdrucken", "divide by -3"],
  ["ausdrucken", ["variable_setzen", "a", ["dividieren", ["variable_abrufen", "a"], -3]]],
  ["ausdrucken", "multiply with 3, 6 and -7 in one go"],
  ["ausdrucken", ["variable_setzen", "a", ["produkt", ["variable_abrufen", "a"], 3, 6, -7]]],
  ["ausdrucken", "to the power of 3"],
  ["ausdrucken", ["variable_setzen", "a", ["potenzieren", ["variable_abrufen", "a"], 3]]],

  ["ausdrucken", ""],
  ["ausdrucken", "### While loop alternative ###", "title"],
  ["ausdrucken", "We create a=2 and b=20, then add 5 to a and 1 to b as long as a<b."],
  ["ausdrucken", ["variable_setzen", "a", 2]],
  ["ausdrucken", ["variable_setzen", "b", 20]],
  ["solange_alt", ["kleiner_als", ["variable_abrufen", "a"], ["variable_abrufen", "b"]],
    ["abfolge",
    ["ausdrucken", "a = ", "nobr"],
    ["ausdrucken", ["variable_setzen", "a", ["addieren", ["variable_abrufen", "a"], 5]]],
    ["ausdrucken", "b = ", "nobr"],
    ["ausdrucken", ["variable_setzen", "b", ["addieren", ["variable_abrufen", "b"], 1]]]
    ]
  ],
  
  ["ausdrucken", ""],
  ["ausdrucken", "### While loop ###", "title"],
  ["ausdrucken", "We create a=2 and b=20, then add 5 to a and 1 to b as long as a<b."],
  ["ausdrucken", ["variable_setzen", "a", 2]],
  ["ausdrucken", ["variable_setzen", "b", 20]],
  ["solange", [["variable_abrufen", "a"], "<", ["variable_abrufen", "b"]], [
    ["ausdrucken", "a = ", "nobr"],
    ["ausdrucken", ["variable_setzen", "a", ["addieren", ["variable_abrufen", "a"], 5]]],
    ["ausdrucken", "b = ", "nobr"],
    ["ausdrucken", ["variable_setzen", "b", ["addieren", ["variable_abrufen", "b"], 1]]]
  ]],
  
  ["ausdrucken", ""],
  ["ausdrucken", "### Lists ###", "title"],
  ["ausdrucken", "We create [1, 'wort', True], retrieve the last position, change 'wort' to 'bike' and print the final list:"],
  ["ausdrucken", ["variable_setzen", "a", "[1, 'wort', True]"]],
  ["ausdrucken", ["variable_abrufen", "a", 2]],
  ["ausdrucken", ["variable_setzen", "a", "bike", 1]],
  ["ausdrucken", ["variable_abrufen", "a"]],
  
  ["ausdrucken", ""]
]
