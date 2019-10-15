# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../temp.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, generator):
        super().__init__()
        self.setupUi()
        self.generator = generator

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1024, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1001, 591))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(10, 10, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 10, 0)
        self.treeView = QtWidgets.QTreeView(self.horizontalLayoutWidget)
        self.treeView.setObjectName("treeView")
        self.verticalLayout.addWidget(self.treeView)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        # self.fig = plt.Figure()
        # self.canvas = FigureCanvas(self.fig)
        self.canvas = draw_canvas(self)
        self.verticalLayout_2.addWidget(self.canvas)
        self.horizontalSlider = QtWidgets.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.setSingleStep(1)
        self.verticalLayout_2.addWidget(self.horizontalSlider)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.horizontalLayoutWidget)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox.setValue(1.0)
        self.doubleSpinBox.setSingleStep(0.01)
        self.horizontalLayout_2.addWidget(self.doubleSpinBox)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.setCentralWidget(self.centralwidget)

        self.dirModel = QtWidgets.QFileSystemModel(self)
        self.dirModel.setRootPath(QtCore.QDir.currentPath())
        self.indexRoot = self.dirModel.index(self.dirModel.rootPath())

        self.treeView.setDragEnabled(True)
        self.treeView.setModel(self.dirModel)
        self.treeView.setRootIndex(self.indexRoot)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def analyzeButtonClicked(self):
        self.generator.unit_E = self.doubleSpinBox.value()
        self.generator.analyze()
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(len(self.generator.z_range) - 1)
        self.horizontalSlider.setValue(0)
        self.generator.draw_plane(self.canvas.ax, 0)
        self.canvas.fig.canvas.draw()
        self.lineEdit.setText(self.generator.infile.split('/')[-1][:-4] + '.gcode')

    def createButtonClicked(self):
        self.generator.outfile = self.lineEdit.text()
        self.generator.write_file()

    def horizontalSliderMoved(self):
        self.generator.draw_plane(self.canvas.ax, self.horizontalSlider.value())
        self.canvas.fig.canvas.draw()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowIcon(QtGui.QIcon(resource_path('./logo.png')))
        self.setWindowTitle(_translate("MainWindow", "Gcode Generator"))
        self.label.setText(_translate("MainWindow", "Extruder"))
        self.pushButton.setText(_translate("MainWindow", "analyze"))
        self.label_2.setText(_translate("MainWindow", "File name"))
        self.pushButton_2.setText(_translate("MainWindow", "create"))

        self.pushButton.clicked.connect(self.analyzeButtonClicked)
        self.pushButton_2.clicked.connect(self.createButtonClicked)
        self.horizontalSlider.valueChanged.connect(self.horizontalSliderMoved)


class draw_canvas(QtWidgets.QWidget):

    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)

        self.setAcceptDrops(True)

        self.name = QtWidgets.QLineEdit()
        self.name.setReadOnly(True)
        plt.ion()
        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.canvas)
        self.layout.addWidget(self.name)

        self.setLayout(self.layout)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/uri-list'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        url = e.mimeData().urls()[0]
        self.parent.generator.infile = str(url.toLocalFile())
        self.name.setText(str(url.toLocalFile()).split('/')[-1])
