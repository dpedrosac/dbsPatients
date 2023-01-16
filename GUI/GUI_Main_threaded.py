import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, \
    QWidget, QButtonGroup, QGroupBox

from utils.helper_functions import General
from GUI.GUIintraoperative import IntraoperativeDialog
from GUI.GUIpostoperative import PostoperativeDialog
from GUI.GUIpreoperative import PreoperativeDialog


class Worker(QRunnable):
    """Worker thread intended to prevent the GUI from freezing. """

    def __init__(self, *args, **kwargs):
        super(Worker, self).__init__()
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        """Initialise the runner function with passed self.args, self.kwargs."""
        print(self.args, self.kwargs)


class ChooseGUI(QDialog):
    """GUI responsible to offer further GUI's: 1. Preoperative 2. Intraoperative 3. Postoperative"""

    def __init__(self, parent=None):
        """Initialize GUImain, a window in which all other "sub-GUIs" may be called from."""

        super().__init__(parent)
        self.threadpool = QThreadPool()
        subj_details = General.read_current_subj()

        # ====================    Create General Layout      ====================
        self.layout = QVBoxLayout()  # layout for the central widget
        widget = QWidget(self)
        widget.setLayout(self.layout)
        groupbox = QGroupBox('Which visit?', checkable=False)
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
        hbox.addWidget(self.button_openGUI_Preoperative)
        hbox.addWidget(self.button_openGUI_Intraoperative)
        hbox.addWidget(self.button_openGUI_Postoperative)

    # ====================    In the next lines, actions are defined when Buttons are pressed      ====================
    @pyqtSlot()
    def on_click(self):
        """select the further steps/GUI to open"""

        if self.button_openGUI_Preoperative.isChecked():  # selects three different options available
            dialog_date = PreoperativeDialog(parent=self)
        elif self.button_openGUI_Intraoperative.isChecked():
            dialog_date = IntraoperativeDialog(parent=self)
        else:
            dialog_date = PostoperativeDialog(parent=self)

        #self.hide()
        #if dialog_date.exec():
        #    pass

        #self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = ChooseGUI()
    dlg.show()
    sys.exit(app.exec_())
