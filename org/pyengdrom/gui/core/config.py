


from core.menubar import MenuBar


MENU_BAR__TEXT_EDITOR = MenuBar(
    [
        ("File", [
            ("New",         "new", "Ctrl+N"),
            ("Open Folder", "open", "Ctrl+O"),
            ("Save",        [
                ("Save", "save", "Ctrl+S"),
                ("Save as", "save_as", "Ctrl+Shift+S")
            ]),
            ("Exit",        "exit")
        ]),
        ("Edit", [
            ("Undo", "undo",   "Ctrl+Z"),
            ("Redo", "redo",   "Ctrl+Y"),
            ("Cut", "cut",     "Ctrl+X"),
            ("Copy", "copy",   "Ctrl+C"),
            ("Paste", "paste", "Ctrl+V"),
            ("Find", "find",   "Ctrl+F")
        ])
    ]
)