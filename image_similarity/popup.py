# Form implementation generated from reading ui file 'popup.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_PopupWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        layout = QVBoxLayout()
        self.label = QLabel();
        self.label.setGeometry(QtCore.QRect(0, 0, 1065, 700))
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setFixedSize(1065, 700);
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hinh anh"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_PopupWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
