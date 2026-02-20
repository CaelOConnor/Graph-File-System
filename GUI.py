import os
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QScrollArea, QWidget
from pyqt_circle_button import CircleButton

focus_node_radius = 100
reg_node_radius = 50
edge_length = 200

node_color = "#949494"
outer_node_color = "#90d5ff"
text_color = "#000000"
edge_color = "#eff7fa"

#Creating graph structure for file system
def build_tree(path, parent=None): 
    name = os.path.basename(path) or path
    is_dir = os.path.isdir(path)
    node = {
        "name": name,
        "path": path,
        "is_dir": is_dir,
        "children": [],
        "parent": parent,
    }
    if is_dir:
        try:
            entries = sorted(os.listdir(path))
        except PermissionError:
            entries = []
        for entry in entries:
            child_path = os.path.join(path, entry)
            node["children"].append(build_tree(child_path, node))
    return node

#Painting graph onto GUI
class paintData(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.resize(800,600)

        self.root_node = QPushButton("Root Node", self)
        self.root_node.resize(200,100)
        self.center_root_node()

    def center_root_node(self):
        cx = self.width() // 2
        cy = self.height() // 2
        root_node_width = self.root_node.width()
        root_node_height = self.root_node.height()
        self.root_node.move(cx - root_node_width//2, cy - root_node_height//2)
    
    def create_nodes(self, data):
        node = makeNode(data, self)

    def set_focus_node(node):
        pass

    def node_clicked(self, node):
        if node.is_outer_node():
            node.open_outer_node()
        else:
            self.set_focus_node(node)

    def paint_edges(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

#Separate class for making nodes
class makeNode(QWidget):
    def __init__(self, node_data, paint):
        super().__init__(paint)
        self.node_data = node_data
        self.paint = paint

    def place_node(self):
        pass

    def is_outer_node(self):
        return not self.node_data["is_dir"]
    
    def paint_node(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.paint.node_clicked(self)
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if self.is_file():
            self.open_file()
        super().mouseDoubleClickEvent(event)

    def open_outer_node(self):
        try:
            with open(self.node_data["path"], 'r') as file:
                info = file.read()
                print(info)
        except Exception as e:
            print("Error reading file")


#Adding painting to scrollable window
class MainWindow(QScrollArea):
    def __init__(self, paint):
        super().__init__()
        self.paint = paint

        self.setWindowTitle("Graph File System")

        # button = QPushButton("Press Me!")
        # button.setMinimumSize(QSize(2000, 1000))

        self.setMinimumSize(QSize(800, 600))

        self.setWidget(paint)

if __name__ == "__main__":
    root = os.path.join(os.getcwd(), "..")
    app = QApplication(sys.argv)
    root_data = build_tree(root)
    paint = paintData(root_data)
    window = MainWindow(paint)
    window.show()

    sys.exit(app.exec())
