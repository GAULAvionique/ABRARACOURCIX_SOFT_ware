import sys
from PyQt6.QtWidgets import QApplication
from darktheme.widget_template_pyqt6 import DarkPalette
from InterfaceMain import MainWindow


def main():
    # Create the Qt application
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    #window.setPalette(DarkPalette())
    window.resize(800, 400)
    window.show()

    # Run the Qt event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
