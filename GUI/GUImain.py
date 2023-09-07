import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, \
    QWidget, QButtonGroup, QGroupBox

from utils.helper_functions import General
from GUI.GUIintraoperative import IntraoperativeDialog
from GUI.GUIpostoperative import PostoperativeDialog
from GUI.GUIpreoperative import PreoperativeDialog


@staticmethod  # Versuch Speicherproblem?
def fill_missing_demographics(flag):
    """very unique function without much versatility intended to fill missing data from general_data.csv to
    pre-/intra-/postoperative.csv in the ./data folder"""

    file_general = General.import_dataframe('general_data.csv', separator_csv=',')
    # if file_general.shape[1] == 1:  # avoids problems with comma-separated vs. semicolon-separated csv-files
    #    file_general = General.import_dataframe('general_data.csv', separator_csv=';')

    for index, row in file_general.iterrows():
        General.synchronize_data_with_general(flag, row['ID'], messagebox=False)
class ChooseGUI(QDialog):
    """GUI responsible to offer further GUI's: 1. Preoperative 2. Intraoperative 3. Postoperative"""

    def __init__(self, parent=None):
        """Initialize GUImain, a window in which all other "sub-GUIs" may be called from."""
        super(ChooseGUI, self).__init__(parent)
# 'parent' welches Elternelement (parent) dieses GUI-Element hat
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

        hbox = QVBoxLayout()
        groupbox.setLayout(hbox)
        hbox.addWidget(self.button_openGUI_Preoperative)
        hbox.addWidget(self.button_openGUI_Intraoperative)
        hbox.addWidget(self.button_openGUI_Postoperative)

        btn_grp.buttonClicked.connect(self.on_click)

    # ====================    In the next lines, actions are defined when Buttons are pressed      ====================
    @pyqtSlot()
    def on_click(self):
        """Calls the respective GUI to enter data"""

        subj_details = General.read_current_subj()
        if self.button_openGUI_Preoperative.isChecked():
            General.get_data_subject(flag='preoperative', pid2lookfor=int(subj_details.pid))
            dialog_date = PreoperativeDialog(parent=self)
        elif self.button_openGUI_Intraoperative.isChecked():
            General.get_data_subject(flag='intraoperative', pid2lookfor=int(subj_details.pid))
            dialog_date = IntraoperativeDialog(parent=self)
        else:
            General.get_data_subject(flag='postoperative', pid2lookfor=int(subj_details.pid))
            dialog_date = PostoperativeDialog(parent=self)

        self.hide()
        if dialog_date.exec():
            pass
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = ChooseGUI()
    dlg.show()
    sys.exit(app.exec_())
