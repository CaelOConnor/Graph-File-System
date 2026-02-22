import os
import sys

from PyQt6.QtCore import QPointF, QRectF, QSize, Qt
from PyQt6.QtGui import QBrush, QColor, QPainter, QPainterPath, QPen
from PyQt6.QtWidgets import QApplication, QLineEdit, QMainWindow, QPushButton, QScrollArea, QWidget
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

#Taken hex button and turned into circles
class CircleButton(QPushButton):
    def __init__(self, text="", parent=None, color=node_color):
        super().__init__(text, parent)
        self.setCheckable(False)
        self.setMinimumSize(60, 60)
        self.color = color

    def circlePath(self):
        # create a path in the shape of a hexagon
        # it's a function because it needs to be recreated with the right pen/brush
        rect = QRectF(self.rect())

        w = rect.width()
        h = rect.height()
        cx = rect.center().x()
        cy = rect.center().y()
        r = min(w, h) / 2 # radius, half the width or height

        path = QPainterPath()
        path.addEllipse(QPointF(cx, cy,), r,r)

        return path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = self.circlePath()

        if self.isDown():
            brush = QBrush(QColor(50,50,50))
        else:
            brush = QBrush(self.color)

        painter.setBrush(brush)
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawPath(path)

        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())

    def hitButton(self, pos):
        return self.circlePath().contains(QPointF(pos))
    
#Separate class for making nodes
class makeNode(CircleButton):
    def __init__(self, node_data, paint, parent=None):
        super().__init__(node_data["name"], parent or paint)
        self.node_data = node_data
        self.paint = paint
        self.color = QColor(outer_node_color if self.is_outer_node() else node_color)
        self.clicked.connect(self.on_clicked)

    def is_outer_node(self):
        return not self.node_data["is_dir"]

    def on_clicked(self):
        self.paint.node_clicked(self)

    def mouseDoubleClickEvent(self, event):
        if self.is_outer_node():
            self.open_outer_node()
        super().mouseDoubleClickEvent(event)

    def open_outer_node(self):
        if os.path.isfile(self.node_data["path"]):
            os.startfile(self.node_data["path"])

#Painting graph onto GUI
class paintData(QWidget):
    def __init__(self, data):
        super().__init__()
        self.setFixedSize(1600, 1200)

        self.all_nodes  = {}
        self.focus_node = None

        # ui
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search:")
        self.search_bar.resize(100, 30)

        self.add_button = QPushButton("+", self)
        self.add_button.resize(30,30)

        self.add_outer_node_button = QPushButton("add outer node", self)
        self.add_outer_node_button.resize(130,30)
        self.add_outer_node_button.hide()
        self.add_node_button = QPushButton("add node", self)
        self.add_node_button.resize(130,30)
        self.add_node_button.hide()

        self.add_outer_node_button.clicked.connect(self.add_file)
        self.add_node_button.clicked.connect(self.add_folder)

        self.add_button.clicked.connect(self.show_add_buttons)
        self.move_ui_to_top_right()

        # nodes
        self.build_all_nodes(data, parent_widget=None)
        root_widget = self.all_nodes[data["path"]]
        self.set_focus_node(root_widget)

    # adds folder
    def add_folder(self, attempt=0):
        if not self.focus_node.node_data["is_dir"]:
            return
        parent_path = self.focus_node.node_data["path"]
        name = "New Folder"
        if attempt > 0:
            name += f"({attempt})"
        
        new_path = os.path.join(parent_path, name)
        try:
            os.mkdir(new_path)
        except:
            self.add_folder(attempt + 1)
            return

        
    # adds file
    def add_file(self, attempt=0):
        if not self.focus_node.node_data["is_dir"]:
            return
        parent_path = self.focus_node.node_data["path"]
        name = "New Folder"
        if attempt > 0:
            name += f"({attempt})"
        name += ".txt"
        
        new_path = os.path.join(parent_path, name)
        try:
            with open(new_path, 'w') as f:
                f.write(".")
        except:
            self.add_folder(attempt + 1)
            return
    
    # for the add outer node and add node buttons
    def show_add_buttons(self):
        if not self.focus_node.node_data["is_dir"]:
            return
        
        visible = self.add_outer_node_button.isVisible()
        if visible:
            self.add_outer_node_button.hide()
            self.add_node_button.hide()
        else:
            x = self.add_button.x()
            y = self.add_button.y()
            self.add_outer_node_button.move(x, y + 30)
            self.add_node_button.move(x, y + 60)
            self.add_outer_node_button.show()
            self.add_node_button.show()

    # moves search bar and add button to top right
    def move_ui_to_top_right(self):
        self.search_bar.move(self.width() - self.search_bar.width(), self.add_button.height() - self.search_bar.height())
        
        self.add_button.move(self.width() - self.add_button.width() - self.search_bar.width(), self.add_button.height() - self.search_bar.height())

#Recursively makes all the nodes we will need and stores them
    def build_all_nodes(self, data, parent_widget):
        node = makeNode(data, self, parent=self)
        self.all_nodes[data["path"]] = node
        for child in data["children"]:
            self.build_all_nodes(child, node)

    def set_focus_node(self, node):
#Hides all nodes and resets their size so they can be redone with new focus
        for n in self.all_nodes.values():
            n.hide()
            n.setFixedSize(reg_node_radius * 2, reg_node_radius * 2)

        self.focus_node = node

        cx = self.width()  // 2
        cy = self.height() // 2

        node.setFixedSize(focus_node_radius * 2, focus_node_radius * 2)
        node.move(cx - focus_node_radius, cy - focus_node_radius)
        node.show()

        # for hiding add buttons
        self.add_outer_node_button.hide()
        self.add_node_button.hide()

#Puts parent of focus above
        parent_data = node.node_data.get("parent")
        if parent_data:
            pw = self.all_nodes.get(parent_data["path"])
            if pw:
                pw.move(cx - reg_node_radius, cy - edge_length - reg_node_radius)
                pw.show()

#Spreads the children of focus out beneath
        children = node.node_data["children"]
        n_children = len(children)
        if n_children:
            total = (n_children - 1) * edge_length
            start_x = cx - total // 2
            for i, child_data in enumerate(children):
                cw = self.all_nodes.get(child_data["path"])
                if cw:
                    cw.move(start_x + i * edge_length - reg_node_radius,
                            cy + edge_length - reg_node_radius)
                    cw.show()

        self.update()

#If a node is clicked make the focus if not a file
    def node_clicked(self, node):
        if not node.is_outer_node():
            self.set_focus_node(node)
            

    def paintEvent(self, event):
#Settings and coordinates for painting edges
        if not self.focus_node:
            return
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor(edge_color), 2))

        def centre(w):
            return w.x() + w.width() // 2, w.y() + w.height() // 2

        fx, fy = centre(self.focus_node)

#Makes edge from parent to focus node
        parent_data = self.focus_node.node_data.get("parent")
        if parent_data:
            pw = self.all_nodes.get(parent_data["path"])
            if pw and pw.isVisible():
                px, py = centre(pw)
                painter.drawLine(fx, fy, px, py)

#Creates all the edges from the focus node to its children
        for child_data in self.focus_node.node_data["children"]:
            cw = self.all_nodes.get(child_data["path"])
            if cw and cw.isVisible():
                cx, cy = centre(cw)
                painter.drawLine(fx, fy, cx, cy)


#Adding painting to scrollable window
class MainWindow(QScrollArea):
    def __init__(self, paint):
        super().__init__()
        self.paint = paint

        self.setWindowTitle("Graph File System")

        # button = QPushButton("Press Me!")
        # button.setMinimumSize(QSize(2000, 1000))

        self.setMinimumSize(QSize(1200, 800))

        self.setWidget(paint)

#Centers the root node at the start
    def showEvent(self, event):
        super().showEvent(event)
        cx = self.widget().width() // 2
        cy = self.widget().height() // 2
        self.horizontalScrollBar().setValue(cx - self.width() // 2)
        self.verticalScrollBar().setValue(cy - self.height() // 2)

if __name__ == "__main__":
    root = os.path.join(os.getcwd(), "..")
    app = QApplication(sys.argv)
    root_data = build_tree(root)
    paint = paintData(root_data)
    window = MainWindow(paint)
    window.show()

    sys.exit(app.exec())
