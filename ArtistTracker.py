import sys
from PyQt4 import QtCore, QtGui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random

from pymongo import MongoClient



try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1023, 750)
        self.query_input = QtGui.QLineEdit(Dialog)
        self.query_input.setGeometry(QtCore.QRect(30, 70, 601, 41))
        self.query_input.setText(_fromUtf8(""))
        self.query_input.setObjectName(_fromUtf8("query_input"))
        self.start_button = QtGui.QPushButton(Dialog)
        self.start_button.setGeometry(QtCore.QRect(640, 70, 171, 41))
        self.start_button.setObjectName(_fromUtf8("start_button"))
        self.save_button = QtGui.QPushButton(Dialog)
        self.save_button.setGeometry(QtCore.QRect(810, 70, 171, 41))
        self.save_button.setObjectName(_fromUtf8("save_button"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(30, 40, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.plot_label = QtGui.QLabel(Dialog)
        self.plot_label.setGeometry(QtCore.QRect(440, 150, 161, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.plot_label.setFont(font)
        self.plot_label.setObjectName(_fromUtf8("plot_label"))
        self.reload_button_2 = QtGui.QPushButton(Dialog)
        self.reload_button_2.setGeometry(QtCore.QRect(240, 120, 151, 31))
        self.reload_button_2.setObjectName(_fromUtf8("reload_button_2"))
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 220, 1001, 501))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.graph_canvas = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.graph_canvas.setObjectName(_fromUtf8("graph_canvas"))
        self.reload_input = QtGui.QLineEdit(Dialog)
        self.reload_input.setGeometry(QtCore.QRect(30, 120, 201, 31))
        self.reload_input.setObjectName(_fromUtf8("reload_input"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(430, 10, 171, 51))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(24)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.start_button.clicked.connect(self.plot)

        self.graph_canvas.addWidget(self.canvas)

    def plot(self):
        # random data
        data = [random.random() for i in range(10)]
        # create an axis
        ax = self.figure.add_subplot(111)
        # discards the old graph
        ax.clear()
        # plot data
        ax.plot(data, '*-')
        # refresh canvas
        self.canvas.draw()

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.query_input.setPlaceholderText(_translate("Dialog", "ArtistName/Album/Song", None))
        self.start_button.setText(_translate("Dialog", "Track \'em !", None))
        self.save_button.setText(_translate("Dialog", "Save project", None))
        self.label.setText(_translate("Dialog", "Artist name", None))
        self.plot_label.setText(_translate("Dialog", "Song popularity", None))
        self.reload_button_2.setText(_translate("Dialog", "Reload project", None))
        self.reload_input.setPlaceholderText(_translate("Dialog", "Project name", None))
        self.label_3.setText(_translate("Dialog", "Artist Tracker", None))


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)

    client = MongoClient()
    db = client['test-database']
    print(db)




    Dialog.show()
    sys.exit(app.exec_())



