["abfolge",
    ["ausdrucken", ""],
    ["ausdrucken", "Welcome to our programming language: The Little German Language, LGL!"],

    ["ausdrucken", ""],
    ["ausdrucken", "### Basic arithmetic and variables ###", "title"],
    ["ausdrucken", "We create a variable 'a' = 8. We then showcase basic math operations."],
    ["variable_setzen", "a", 8],
    ["ausdrucken", "a = ", ["variable_abrufen", "a"]],
    ["variable_setzen", "a", ["addieren", ["variable_abrufen", "a"], 2]],
    ["ausdrucken", "+ 2 = ", ["variable_abrufen", "a"]],
    ["variable_setzen", "a", ["subtrahieren", ["variable_abrufen", "a"], 4]],
    ["ausdrucken", "- 4 = ", ["variable_abrufen", "a"]],
    ["variable_setzen", "a", ["dividieren", ["variable_abrufen", "a"], -3]],
    ["ausdrucken", "/ (-3) = ", ["variable_abrufen", "a"]],
    ["variable_setzen", "a", ["produkt", ["variable_abrufen", "a"], 3, 6, -7]],
    ["ausdrucken", "* 3 * 6 * (-7) = ", ["variable_abrufen", "a"]],
    ["variable_setzen", "a", ["potenzieren", ["variable_abrufen", "a"], 3]],
    ["ausdrucken", "* 3 = ", ["variable_abrufen", "a"]],
    ["ausdrucken", ""],

    ["ausdrucken", "### While loop ###", "title"],
    ["ausdrucken", "We create a = 2 and b = 20, then add 5 to a and 1 to b as long as a < b."],
    ["variable_setzen", "a", 2],
    ["ausdrucken", "a = ", ["variable_abrufen", "a"], ", ", "nobr"],
    ["variable_setzen", "b", 20],
    ["ausdrucken", "b = ", ["variable_abrufen", "b"]],
    ["solange", ["kleiner_als", ["variable_abrufen", "a"], ["variable_abrufen", "b"]],
        ["abfolge",
            ["variable_setzen", "a", ["addieren", ["variable_abrufen", "a"], 5]],
            ["ausdrucken", "a = ", ["variable_abrufen", "a"], ", ", "nobr"],
            ["variable_setzen", "b", ["addieren", ["variable_abrufen", "b"], 1]],
            ["ausdrucken", "b = ", ["variable_abrufen", "b"]]
        ]
    ],
    ["ausdrucken", ""],

    ["ausdrucken", "### Arrays ###", "title"],
    ["ausdrucken", "We create an array of size 3: [1, 'Wort', 3.14], change 'Wort' to 'Zahl' and retrieve the second element"],
    ["variable_setzen", "beispiel_liste",["liste", 3, 1, "Wort", 3.14]],
    ["ausdrucken", "beispiel_liste = ", ["variable_abrufen", "beispiel_liste"]],
    ["element_setzen",["variable_abrufen", "beispiel_liste"], 1, "Zahl"],
    ["ausdrucken", "beispiel_liste[1] = ", ["element_abrufen", ["variable_abrufen", "beispiel_liste"], 1]],
    ["ausdrucken", "beispiel_liste = ", ["variable_abrufen", "beispiel_liste"]],
    ["ausdrucken", ""],

    ["ausdrucken", "### Dictionaries ###", "title"],
    ["ausdrucken", "We create a dictionary: {'Name': 'Alice', 'Alter': 25, 'Beruf': Lehrerin}, retrieve the name, change 'Alter' to 26 and print the final dictionary:"],
    ["variable_setzen", "person", ["lexikon", ["Name", "Alice"], ["Alter", "25"], ["Beruf", "Lehrerin"]]],
    ["ausdrucken", "person = ", ["variable_abrufen", "person"]],
    ["ausdrucken", "person['Name'] = ", ["eintrag_abrufen", ["variable_abrufen", "person"], "Name"]],
    ["eintrag_setzen", ["variable_abrufen", "person"], "Alter", "26"],
    ["ausdrucken", "person['Alter'] = ", ["eintrag_abrufen", ["variable_abrufen", "person"], "Alter"]],
    ["ausdrucken", "person = ", ["variable_abrufen", "person"]],
    ["ausdrucken", "Now we create another dictionary: {'Name': 'Alice', 'Email': 'alice.muster@email.com', 'registriert': True}, and merge the two dictionary:"],
    ["variable_setzen", "person_extra", ["lexikon", ["Name", "Alice"], ["Email", "alice.muster@email.com"], ["registriert", ["wahr"]]]],
    ["ausdrucken", "person_extra = ", ["variable_abrufen", "person_extra"]],
    ["variable_setzen", "person", ["lexika_vereinen", ["variable_abrufen", "person"], ["variable_abrufen", "person_extra"]]],
    ["ausdrucken", "person | person_extra = ", ["variable_abrufen", "person"]]

]
