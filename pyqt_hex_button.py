from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QPainter, QPainterPath, QPen, QBrush, QColor
from PySide6.QtCore import Qt, QPointF, QRectF

from PySide6.QtWidgets import QApplication, QWidget, QGridLayout
import sys

class HexButton(QPushButton):
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCheckable(False)
        self.setMinimumSize(60, 60)

    def hexagonPath(self):
        # create a path in the shape of a hexagon
        # it's a function because it needs to be recreated with the right pen/brush
        rect = QRectF(self.rect())

        w = rect.width()
        h = rect.height()
        cx = rect.center().x()
        cy = rect.center().y()
        r = min(w, h) / 2 # radius, half the width or height


        
        points = [
            QPointF(cx + r * 0.5, cy - r), # bottom right
            QPointF(cx + r,       cy), # middle right
            QPointF(cx + r * 0.5, cy + r), # top right
            QPointF(cx - r * 0.5, cy + r), # top left
            QPointF(cx - r,       cy), # middle left
            QPointF(cx - r * 0.5, cy - r), # bottom left
        ]

        path = QPainterPath()
        path.moveTo(points[0])
        for p in points[1:]:
            path.lineTo(p)
        path.closeSubpath()

        return path

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = self.hexagonPath()

        # Background color by state
        if self.isDown() or self.isChecked():
            brush = QBrush(QColor(50,50,50))
        elif self.underMouse():
            brush = QBrush(QColor(100,100,100))
        else:
            brush = QBrush(QColor(200,200,200))

        painter.setBrush(brush)
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawPath(path)

        # Draw text
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())

    def hitButton(self, pos):
        return self.hexagonPath().contains(QPointF(pos))


if __name__=='__main__':

    app = QApplication(sys.argv)

    window = QWidget()
    layout = QGridLayout(window)

    btn = HexButton("Hex1")
    layout.addWidget(btn, 1, 1)

    btn = HexButton("Hex2")
    layout.addWidget(btn, 1, 3)

    btn = HexButton("Hex3")
    layout.addWidget(btn, 3, 2)

    btn = HexButton("Hex4")
    layout.addWidget(btn, 3, 4)

    window.show()
    sys.exit(app.exec())