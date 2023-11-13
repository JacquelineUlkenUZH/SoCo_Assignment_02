["abfolge",
    ["variable_setzen", "get_cube_power",
        ["funktion", "x",
            ["potenzieren", ["variable_abrufen", "x"], 3]
        ]
    ],
    ["variable_setzen", "add_cubes",
        ["funktion", ["a", "b"],
            ["addieren",
                ["funktion_aufrufen", "get_cube_power", ["variable_abrufen", "a"]],
                ["funktion_aufrufen", "get_cube_power", ["variable_abrufen", "b"]]
            ]
        ]
    ],
    ["funktion_aufrufen", "add_cubes", 3, 2]
]