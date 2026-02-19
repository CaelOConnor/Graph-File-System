import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Graph File System")

        button = QPushButton("Press Me!")

        screen = QApplication.primaryScreen()
        screen_size = screen.availableGeometry()

        self.setMinimumSize(QSize(400, 300))
        self.setMaximumSize(QSize(screen_size.width(), screen_size.height()))

        button.setMinimumSize(50, 50)
        button.setMaximumSize(300, 300)

        # Set the central widget of the Window.
        self.setCentralWidget(button)



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()