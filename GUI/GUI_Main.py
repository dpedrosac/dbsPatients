import os
import sys

import pandas as pds
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, \
    QWidget, QButtonGroup, QHBoxLayout, QGroupBox

from utils.helper_functions import General
from GUI.GUI_Intraoperative import IntraoperativeDialog
from GUI.GUI_Postoperative import PostoperativeDialog
from GUI.GUIpreoperative import PreoperativeDialog
from dependencies import ROOTDIR


class ChooseGUI(QDialog):
    """This GUI is responsible to open further GUI'S:
    1. Preoperative 2. Intraoperative 3. Postoperative"""

    def __init__(self, parent=None):
        """Initialize GUImain, a window in which all other "sub-GUIs" may be called from."""

        super().__init__(parent)
        subj_details = General.read_current_subj()

        # ====================    Create General Layout      ====================
        self.layout = QVBoxLayout()  # layout for the central widget
        widget = QWidget(self)
        widget.setLayout(self.layout)
        groupbox = QGroupBox("Which visit?", checkable=False)
        self.layout.addWidget(groupbox)

        self.setWindowTitle('Choose GUI for subj with PID: {}'.format(str(int(subj_details.pid))))
        self.setGeometry(400, 100, 800, 300)  # left, right, width, height
        self.move(750, 375)

        # ====================    Create Content for Buttons of GUImain      ====================
        self.button_openGUI_Preoperative = QPushButton('Preoperative')
        self.button_openGUI_Preoperative.setCheckable(True)

        self.button_openGUI_Intraoperative = QPushButton('Intraoperative')
        self.button_openGUI_Intraoperative.setCheckable(True)

        self.button_openGUI_Postoperative = QPushButton('Postoperative')
        self.button_openGUI_Postoperative.setCheckable(True)

        # ====================    Add ButtonGroup and buttons to self.layout      ====================
        btn_grp = QButtonGroup(widget)
        btn_grp.setExclusive(True)
        btn_grp.addButton(self.button_openGUI_Preoperative)
        btn_grp.addButton(self.button_openGUI_Intraoperative)
        btn_grp.addButton(self.button_openGUI_Postoperative)
        btn_grp.buttonClicked.connect(self.on_click)

        hbox = QVBoxLayout()
        groupbox.setLayout(hbox)
        #hbox.addStretch()
        hbox.addWidget(self.button_openGUI_Preoperative)
        hbox.addWidget(self.button_openGUI_Intraoperative)
        hbox.addWidget(self.button_openGUI_Postoperative)

    # ====================    In the next lines, actions are defined when Buttons are pressed      ====================
    @QtCore.pyqtSlot()
    def on_click(self):
        if self.button_openGUI_Preoperative.isChecked():  # selects three different options available
            dialog = PreoperativeDialog(parent=self)
        elif self.button_openGUI_Intraoperative.isChecked():
            dialog = IntraoperativeDialog(parent=self)
        else:
            dialog = PostoperativeDialog(parent=self)

        self.hide()
        if dialog.exec():
            pass
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = ChooseGUI()
    dlg.show()
    sys.exit(app.exec_())
