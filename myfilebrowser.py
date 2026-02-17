from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                             QHBoxLayout, QWidget, QTreeView, QListView,
                             QSplitter, QLabel, QPushButton, QFileSystemModel)

import sys
import os
from os.path import expanduser


class FileBrowserForm(object):

    def __init__(self):
        self.selected = None


    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(569, 486)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(24)
        self.label.setFont(font)

        self.verticalLayout.addWidget(self.label)

        # instantiate the view for the model-view-controller architecture
        self.treeView = QTreeView(Form)
        self.treeView.setObjectName(u"treeView")

        # instantiate the model for the model-view-controller architecture
        self.model = QFileSystemModel()

        # check if we're on windows or mac
        if os.name == 'nt':
            home_directory = expanduser('C:/')
        else:
            home_directory = expanduser('/')

        self.model.setRootPath(home_directory)

        # link the model to the view
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(home_directory))

        self.verticalLayout.addWidget(self.treeView)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        # create buttons
        self.new_folder_button = QPushButton(Form)
        self.new_folder_button.setObjectName(u"new_folder_button")
        self.new_folder_button.clicked.connect(self.new_folder)

        self.horizontalLayout.addWidget(self.new_folder_button)

        self.new_file_button = QPushButton(Form)
        self.new_file_button.setObjectName(u"new_file_button")
        self.new_file_button.clicked.connect(self.new_file)

        self.horizontalLayout.addWidget(self.new_file_button)

        self.delete_button = QPushButton(Form)
        self.delete_button.setObjectName(u"delete_button")
        self.delete_button.clicked.connect(self.delete)

        self.horizontalLayout.addWidget(self.delete_button)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        """
        Add text to the UI components
        It's good practice to keep these all in one place, so that's what qt designer does
        """
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"My File Browser", None))
        self.new_folder_button.setText(QCoreApplication.translate("Form", u"New Folder", None))
        self.new_file_button.setText(QCoreApplication.translate("Form", u"New File", None))
        self.delete_button.setText(QCoreApplication.translate("Form", u"Delete", None))

    def get_path(self, filename, ind):
        ind = ind.siblingAtColumn(0)
        
        
        path = ''
        while(ind.parent().isValid()):
            path = os.path.join(self.model.data(ind), path)
            ind = ind.parent()

        path = os.path.join(self.model.rootPath(), path)
        print(path, 'before dirname')
        path = os.path.dirname(path)
        print(path, 'after dirname')
        return os.path.join(path, filename)

    def new_folder(self, attempt=0):
        ind = self.treeView.currentIndex()
        if(not ind.isValid()):
            return
        else:
            fname = 'New Folder'
            if attempt > 0:
                fname += '({})'.format(attempt)
            try:
                path = self.get_path(fname, ind)
                print('Creating directory: ', path)
                os.mkdir(path)
            except:
                self.new_folder(attempt=attempt+1)

    def new_file(self, attempt=0):
        ind = self.treeView.currentIndex()
        if(not ind.isValid()):
            return
        else:
            fname = 'New File'
            if attempt > 0:
                fname += '({})'.format(attempt)
            path = self.get_path(fname, ind)
            if os.path.exists(path):
                self.new_file(attempt=attempt+1)
            else:
                print('Creating file', path)
                with open(path, 'w') as f:
                    pass

    def delete(self):
        ind = self.treeView.currentIndex()
        if(not ind.isValid()):
            return
        else:
            path = self.get_path(self.model.data(ind.siblingAtColumn(0)), ind.parent())
            print('Removing', path)
            if os.path.exists(path):
                os.remove(path)
            else:
                print("tried to remove non-existent file: {}".format(path))
                

app = QApplication(sys.argv)
window = QWidget()
ui = FileBrowserForm()
ui.setupUi(window)
window.show()
sys.exit(app.exec())