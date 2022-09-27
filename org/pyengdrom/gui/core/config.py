


from org.pyengdrom.gui.core.menubar import MenuBar


MENU_BAR__TEXT_EDITOR = MenuBar(
    [
        ("File", [
            ("New",         "new", "Ctrl+N"),
            ("Open Folder", "open_folder", "Ctrl+O"),
            ( None,         "separator"),
            ("Save", "save", "Ctrl+S"),
            ("Save as", "save_as", "Ctrl+Shift+S"),
            ( None,         "separator"),
            ("Exit",        "exit")
        ]),
        ("Edit", [
            ("Undo", "undo",   "Ctrl+Z"),
            ("Redo", "redo",   "Ctrl+Y"),
            ( None,  "separator"),
            ("Cut", "cut",     "Ctrl+X"),
            ("Copy", "copy",   "Ctrl+C"),
            ("Paste", "paste", "Ctrl+V"),
            ( None,  "separator"),
            ("Find", "find",   "Ctrl+F")
        ])
    ]
)

class ColorPalette:
    textEditorBackground = "bg-theme-800"
    textEditorTab        = "bg-theme-700"