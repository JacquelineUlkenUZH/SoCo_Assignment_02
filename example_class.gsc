["abfolge",
    ["variable_setzen", "Shape",
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
    ],

    ["variable_setzen", "Square",
        ["klasse", "Square", ["variable_abrufen", "Shape"],
            ["konstrukteur", ["name", "side"],
                ["lexikon",
                    ["name", ["variable_abrufen", "name"]],
                    ["side", ["variable_abrufen", "side"]]
                ]
            ],
            ["lexikon",
                ["area",
                    ["methode", [],
                        ["potenzieren", ["eintrag_abrufen", ["variable_abrufen", "instanz"], "side"], 2]
                    ]
                ]
            ]
        ]
    ],

    ["variable_setzen", "Circle",
        ["klasse", "Circle", ["variable_abrufen", "Shape"],
            ["konstrukteur", ["name", "radius"],
                ["lexikon",
                    ["name", ["variable_abrufen", "name"]],
                    ["radius", ["variable_abrufen", "radius"]]
                ]
            ],
            ["lexikon",
                ["area",
                    ["methode", [],
                        ["multiplizieren", 3.141593, ["potenzieren", ["eintrag_abrufen", ["variable_abrufen", "instanz"], "radius"], 2]]
                    ]
                ]
            ]
        ]
    ],

    ["variable_setzen", "sq", ["objekt", ["variable_abrufen", "Square"], "sq", 3]],
    ["variable_setzen", "ci", ["objekt", ["variable_abrufen", "Circle"], "ci", 2]],
    ["ausdrucken", ["addieren", ["methode_aufrufen", ["variable_abrufen", "sq"], "density", 5], ["methode_aufrufen", ["variable_abrufen", "ci"], "density", 5]]]
]