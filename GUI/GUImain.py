import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, \
    QWidget, QButtonGroup, QGroupBox

from utils.helper_functions import General
from GUI.GUIintraoperative import IntraoperativeDialog
from GUI.GUIpostoperative import PostoperativeDialog
from GUI.GUIpreoperative import PreoperativeDialog


class ChooseGUI(QDialog):
    """GUI responsible to offer further GUI's: 1. Preoperative 2. Intraoperative 3. Postoperative"""

    def __init__(self, parent=None):
        """Initialize GUImain, a window in which all other "sub-GUIs" may be called from."""
        super(ChooseGUI, self).__init__(parent)
        subj_details = General.read_current_subj()
        self.date = ''  # to be defined by selection in this GUI

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
        self.button_openGUI_Preoperative = self.create_checkable_button('Preoperative')
        self.button_openGUI_Intraoperative = self.create_checkable_button('Intraoperative')
        self.button_openGUI_Postoperative = self.create_checkable_button('Postoperative')

        # ====================    Add ButtonGroup and buttons to self.layout      ====================
        btn_grp = QButtonGroup(widget)
        btn_grp.setExclusive(True)
        btn_grp.addButton(self.button_openGUI_Preoperative)
        btn_grp.addButton(self.button_openGUI_Intraoperative)
        btn_grp.addButton(self.button_openGUI_Postoperative)

        hbox = QVBoxLayout()
        groupbox.setLayout(hbox)
        hbox.addWidget(self.button_openGUI_Preoperative)
        hbox.addWidget(self.button_openGUI_Intraoperative)
        hbox.addWidget(self.button_openGUI_Postoperative)

        btn_grp.buttonClicked.connect(self.on_click)

    def create_checkable_button(self, text):
        """Create a checkable button with the given text."""
        button = QPushButton(text)
        button.setCheckable(True)
        return button

    # ====================    In the next lines, actions are defined when Buttons are pressed      ====================
    @pyqtSlot()
    def on_click(self):
        """Calls the respective GUI to enter data"""
        subj_details = General.read_current_subj()
        flag_mapping = {
            self.button_openGUI_Preoperative: 'Preoperative',
            self.button_openGUI_Intraoperative: 'Intraoperative',
            self.button_openGUI_Postoperative: 'Postoperative'
        }

        selected_button = self.sender().checkedButton().text()
        if selected_button in flag_mapping.values():
            General.get_data_subject(flag=selected_button.lower(), pid2lookfor=int(subj_details.pid.iloc[0]))

            if selected_button.lower() == 'preoperative':
                dialog_date = PreoperativeDialog(parent=self)
            elif selected_button.lower() == 'intraoperative':
                dialog_date = IntraoperativeDialog(parent=self)
            else:
                dialog_date = PostoperativeDialog(parent=self)

            #self.hide()
            #if dialog_date.exec():
            #    pass  # Your logic after the dialog is executed
            #self.show()
            dialog_date.show()  # Use show() instead of exec() to keep the main window running
            #GP: every time a msg_box closed, the whole program shut down

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = ChooseGUI()
    dlg.show()
    sys.exit(app.exec_())
