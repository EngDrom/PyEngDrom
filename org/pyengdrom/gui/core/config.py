


from core.menubar import MenuBar


MENU_BAR__TEXT_EDITOR = MenuBar(
    [
        ("File", [
            ("New",         "new"    ),
            ("Open Folder", "open"   ),
            ("Save",        [
                ("Save", "save"),
                ("Save as", "save_as")
            ]),
            ("Exit",        "exit"   )
        ]),
        ("Edit", [
            ("Undo", "undo"),
            ("Redo", "redo"),
            ("Cut", "cut"),
            ("Copy", "copy"),
            ("Paste", "paste"),
            ("Find", "find")
        ])
    ]
)