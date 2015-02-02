# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flightmapper_dialog_base.ui'
#
# Created: Mon Feb 02 06:52:00 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_flightmapperDialogBase(object):
    def setupUi(self, flightmapperDialogBase):
        flightmapperDialogBase.setObjectName(_fromUtf8("flightmapperDialogBase"))
        flightmapperDialogBase.resize(348, 275)
        self.label = QtGui.QLabel(flightmapperDialogBase)
        self.label.setGeometry(QtCore.QRect(10, 10, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.line = QtGui.QFrame(flightmapperDialogBase)
        self.line.setGeometry(QtCore.QRect(10, 40, 331, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_2 = QtGui.QLabel(flightmapperDialogBase)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 61, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton_2 = QtGui.QPushButton(flightmapperDialogBase)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 60, 31, 21))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.comboBox = QtGui.QComboBox(flightmapperDialogBase)
        self.comboBox.setGeometry(QtCore.QRect(90, 60, 201, 20))
        self.comboBox.setFrame(True)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox_2 = QtGui.QComboBox(flightmapperDialogBase)
        self.comboBox_2.setGeometry(QtCore.QRect(90, 90, 201, 22))
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.label_3 = QtGui.QLabel(flightmapperDialogBase)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 61, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.comboBox_3 = QtGui.QComboBox(flightmapperDialogBase)
        self.comboBox_3.setGeometry(QtCore.QRect(90, 120, 201, 22))
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.label_4 = QtGui.QLabel(flightmapperDialogBase)
        self.label_4.setGeometry(QtCore.QRect(10, 120, 61, 20))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(flightmapperDialogBase)
        self.label_5.setGeometry(QtCore.QRect(10, 210, 101, 20))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.pushButton_3 = QtGui.QPushButton(flightmapperDialogBase)
        self.pushButton_3.setGeometry(QtCore.QRect(310, 210, 31, 21))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.lineEdit = QtGui.QLineEdit(flightmapperDialogBase)
        self.lineEdit.setGeometry(QtCore.QRect(90, 210, 201, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.line_2 = QtGui.QFrame(flightmapperDialogBase)
        self.line_2.setGeometry(QtCore.QRect(10, 190, 331, 20))
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.label_6 = QtGui.QLabel(flightmapperDialogBase)
        self.label_6.setGeometry(QtCore.QRect(10, 150, 101, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.lineEdit_2 = QtGui.QLineEdit(flightmapperDialogBase)
        self.lineEdit_2.setGeometry(QtCore.QRect(90, 150, 201, 20))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.widget = QtGui.QWidget(flightmapperDialogBase)
        self.widget.setGeometry(QtCore.QRect(180, 240, 162, 27))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.cancelButton = QtGui.QPushButton(self.widget)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.okButton = QtGui.QPushButton(self.widget)
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.horizontalLayout.addWidget(self.okButton)

        self.retranslateUi(flightmapperDialogBase)
        QtCore.QMetaObject.connectSlotsByName(flightmapperDialogBase)

    def retranslateUi(self, flightmapperDialogBase):
        flightmapperDialogBase.setWindowTitle(_translate("flightmapperDialogBase", "flightmapper", None))
        self.label.setText(_translate("flightmapperDialogBase", "flightmapper", None))
        self.label_2.setText(_translate("flightmapperDialogBase", "Point Layer", None))
        self.pushButton_2.setText(_translate("flightmapperDialogBase", "...", None))
        self.label_3.setText(_translate("flightmapperDialogBase", "Resolution", None))
        self.label_4.setText(_translate("flightmapperDialogBase", "Basemap", None))
        self.label_5.setText(_translate("flightmapperDialogBase", "Export Folder", None))
        self.pushButton_3.setText(_translate("flightmapperDialogBase", "...", None))
        self.label_6.setText(_translate("flightmapperDialogBase", "Title", None))
        self.cancelButton.setText(_translate("flightmapperDialogBase", "Cancel", None))
        self.okButton.setText(_translate("flightmapperDialogBase", "OK", None))

