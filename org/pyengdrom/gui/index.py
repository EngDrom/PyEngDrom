from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QMessageBox


class EngdromGUI:
    @staticmethod
    def main(argv):
        app = QApplication.instance()
        fen = QWidget()
        fen.resize(250, 150)
        fen.move(300, 300)
        fen.setWindowTitle("Engdrom GUI")
        fen.show()
        app.exec_()


if __name__ == "__main__":
    import sys

    EngdromGUI.main(sys.argv)
