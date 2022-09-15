
from typing import List, Tuple
from PyQt5.QtWidgets import *

MenuBarConfig = List[
    Tuple[
        str, # name
        "MenuBarConfig"
    ]
]

class MenuBar:
    def __init__(self, config: MenuBarConfig):
        self.config = config
    def _build(self, config: MenuBarConfig, bar=None):
        if bar is None: 
            bar = QMenuBar()

        for string, next, *args in config:
            if not isinstance(next, str) and next is not None:
                menu = bar.addMenu(string)
                self._build(next, menu)
            elif string is not None:
                action = bar.addAction(string)

                if next is not None:
                    action.triggered.connect(getattr(self.element, next))
                if len(args) >= 1:
                    action.setShortcut(args[0])
            else:
                bar.addSeparator()
        
        return bar
        
    def apply(self, gui_app):
        self.element = gui_app
        if not hasattr(self, "_bar"):
            self._bar = self._build(self.config)
        
        gui_app.window.setMenuBar(self._bar)
