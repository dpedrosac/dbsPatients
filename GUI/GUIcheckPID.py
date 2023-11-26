#!/usr/bin/env python3
import sys
from PyQt5 import QtCore, QtWidgets
from utils.helper_functions import General, Output
from GUI.GUIgeneral_data import CheckForGeneralData
from GUI.GUImain import ChooseGUI


class CheckPID(QtWidgets.QDialog):
    """Initial GUI for entering a PID and checking for existence. Possible options after entering a PID:
    1. if existent -> GUI_Start -> Gui_Main, 2. if nonexistent enter data in general table"""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.EnterNewPID = CheckForGeneralData()
        self.GuiMain = ChooseGUI()

        self.setWindowTitle('Please enter the PID to search for')
        self.setGeometry(400, 100, 500, 300)  # left, right, width, height
        self.move(750, 300)

        self.init_ui()

    def init_ui(self):
        self.content_box = QtWidgets.QVBoxLayout()  # content of the box
        self.layout = QtWidgets.QVBoxLayout(self)  # entire layout for GUI

        # ====================    Create Content for First Option box on Top left      ====================
        self.optionbox_guistart = QtWidgets.QGroupBox('Please enter the PID_Orbis')
        self.settings_optionbox1 = QtWidgets.QVBoxLayout(self.optionbox_guistart)

        self.subj_PID = QtWidgets.QLabel('PID-ORBIS (without zeros):\t\t')
        self.lineEditPID = QtWidgets.QLineEdit()

        self.lineEditPID.setFixedWidth(200)
        # self.lineEditPID.setFixedHeight(40)

        lay1 = QtWidgets.QHBoxLayout()
        lay1.addWidget(self.subj_PID)
        lay1.addWidget(self.lineEditPID)
        lay1.addStretch()

        self.settings_optionbox1.addLayout(lay1)
        self.content_box.addWidget(self.optionbox_guistart)

        # ====================    Create Content for Buttons at the Bottom      ====================
        layout_buttons = QtWidgets.QHBoxLayout()
        self.button_checkPID = QtWidgets.QPushButton('Check for \nexistence')
        self.button_checkPID.clicked.connect(self.onClickedCheckPID)
        self.button_close = QtWidgets.QPushButton('Close GUI')
        self.button_close.clicked.connect(self.close)

        layout_buttons.addStretch(1)
        layout_buttons.addWidget(self.button_checkPID)
        layout_buttons.addWidget(self.button_close)

        # ====================    Add boxes and buttons to self.entire_layout      ====================
        self.layout.addLayout(self.content_box)
        self.layout.addLayout(layout_buttons)

    # In the next lines, actions are defined when buttons are pressed
    @QtCore.pyqtSlot()
    def onClickedCheckPID(self):
        """when button pressed, a series of checks are performed to retrieve data/to set the following GUI """

        if not self.lineEditPID.text():
            Output.msg_box(text='Missing input for the PID, please enter a number', title='Missing input')
            return

        if self.lineEditPID.text():
            filename2load = 'general_data.csv'
            General.get_data_subject(flag='general_data', pid2lookfor=self.lineEditPID.text())
            df = General.import_dataframe(filename2load, separator_csv=',')

            PID2lookfor = self.lineEditPID.text().lstrip('0')  # string that is searched for in metadata file
            idx_PID = df.index[df['PID_ORBIS'] == int(PID2lookfor)].to_list()

        if not idx_PID:
            Output.msg_box(text='No corresponding subject found, please create new entry', title='Missing PID')
            self.EnterNewPID.show()
            self.hide()

        elif len(idx_PID) > 1:
            Output.msg_box(text='Too many entries for PID, please double check file manually: {}'.format(filename2load),
                           title='Too many PID entries')
            return
        else:
            General.write_csv_temp(df, idx_PID)  # creates a new temporary file called current_subj.csv in ./temp
            self.hide()
            self.GuiMain.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dlg = CheckPID()
    dlg.show()
    sys.exit(app.exec_())
