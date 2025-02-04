import sys, os
# Add the parent directory to the sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pds
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QWidget, QButtonGroup, QGroupBox, \
    QHBoxLayout, QComboBox, QMessageBox, QLabel, QSpacerItem, QSizePolicy, QGridLayout, QCheckBox
from utils.helper_functions import General, Clean, Output
from GUI.GUIintraoperative import IntraoperativeDialog
from GUI.GUIpostoperative import PostoperativeDialog
from GUI.GUIpreoperative import PreoperativeDialog
from GUI.GUIgeneral_data import CheckForGeneralData
from GUI.GUIcheckPID import CheckPID
from dependencies import ROOTDIR, FILEDIR

class ChooseGUI(QDialog):
    """GUI responsible to offer further GUI's: 1. Preoperative 2. Intraoperative 3. Postoperative"""

    def __init__(self, parent=None):
        """Initialize GUImain, a window in which all other "sub-GUIs" may be called from."""
        super(ChooseGUI, self).__init__(parent)
        self.date = ''  # to be defined by selection in this GUI
        self.setup_ui()

    def setup_ui(self):
        self.setup_general_layout()

    def setup_general_layout(self):
        self.layout = QHBoxLayout()  # layout for the central widgets
        widget = QWidget(self)
        widget.setLayout(self.layout)
        self.setLayout(self.layout)  # Ensure the layout is set for the main widget

        self.spacer_left = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.layout.addItem(self.spacer_left)

        # Create the first group box for visit selection
        groupbox1 = QGroupBox('Which visit?', checkable=False)
        groupbox1.setFixedSize(270, 350)  # Set fixed size for groupbox1
        self.layout.addWidget(groupbox1)

        # Create the second group box for patient data
        groupbox2 = QGroupBox('Edit Patient Data', checkable=False)
        groupbox2.setFixedSize(270, 350)  # Set fixed size for groupbox2
        self.layout.addWidget(groupbox2)

        # Create the third group box for changing Patient
        groupbox3 = QGroupBox('Change current Patient')
        groupbox3.setFixedSize(270, 350)  # Set fixed size for groupbox3
        self.layout.addWidget(groupbox3)

        self.spacer_right = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.layout.addItem(self.spacer_right)

        # Set window title and geometry
        self.setMinimumSize(900, 450)
        self.move(1000, 500)

        # Add buttons to the group boxes
        self.optionbox_guimain(groupbox1)
        self.optionbox_patient_data(groupbox2)
        self.optionbox_change_patient(groupbox3)

        # Populate pid_list
        self.populate_pid_list()

        # Check if current_subject has an entry in general_data
        self.check_current_subject()

        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)

    def toggle_stylesheet(self, state):
        if state == Qt.Checked:
            self.setStyleSheet("""
                QDialog { background-color: #000000; color: white; }
                QWidget { background-color: #000000; color: white; }
                QPushButton { background-color: #333333; color: white; }
            """)
        else:
            self.setStyleSheet("")

    def optionbox_guimain(self, groupbox1):
        """Create content for buttons of GUImain and add them to the layout."""
        self.button_openGUI_Preoperative = self.create_checkable_button('Preoperative')
        self.button_openGUI_Intraoperative = self.create_checkable_button('Intraoperative')
        self.button_openGUI_Postoperative = self.create_checkable_button('Postoperative')

        btn_grp = QButtonGroup(groupbox1)
        btn_grp.setExclusive(True)
        btn_grp.addButton(self.button_openGUI_Preoperative)
        btn_grp.addButton(self.button_openGUI_Intraoperative)
        btn_grp.addButton(self.button_openGUI_Postoperative)

        hbox = QVBoxLayout()
        groupbox1.setLayout(hbox)
        hbox.addWidget(self.button_openGUI_Preoperative)
        hbox.addWidget(self.button_openGUI_Intraoperative)
        hbox.addWidget(self.button_openGUI_Postoperative)

        btn_grp.buttonClicked.connect(self.on_click)

    def optionbox_patient_data(self, groupbox2):
        """Create content for patient data and add them to the layout."""
        self.button_general_data = QPushButton('General Data')
        self.button_delete_data = QPushButton('Delete Patient')

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.button_general_data)
        vbox2.addWidget(self.button_delete_data)

        # Add label and checkbox for stylesheet change beside each other
        hbox = QHBoxLayout()
        self.label_stylesheet = QLabel('Enable Dark Mode:')
        self.checkbox_stylesheet = QCheckBox()
        self.checkbox_stylesheet.stateChanged.connect(self.toggle_stylesheet)

        hbox.addWidget(self.label_stylesheet)
        hbox.addWidget(self.checkbox_stylesheet)
        vbox2.addLayout(hbox)

        groupbox2.setLayout(vbox2)

        self.button_general_data.clicked.connect(self.onClickGeneralData)
        self.button_delete_data.clicked.connect(self.onClickDeleteData)

    def optionbox_change_patient(self, groupbox3):

        select_patient_label = QLabel('Select different Patient:')
        self.pid_list = QComboBox()
        self.pid_list.setEnabled(True)
        self.button_change_patient = QPushButton('Change Patient')
        self.button_change_patient.setEnabled(False)
        self.button_add_new_pid = QPushButton('Add new PID')
        self.button_check_pid = QPushButton('Check PID')

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.button_add_new_pid)
        vbox3.addWidget(self.button_check_pid)
        vbox3.addWidget(select_patient_label)
        vbox3.addWidget(self.pid_list)
        vbox3.addWidget(self.button_change_patient)

        groupbox3.setLayout(vbox3)

        self.button_change_patient.clicked.connect(self.onClickChangePatient)
        self.button_add_new_pid.clicked.connect(self.onClickAddNewPID)
        self.button_check_pid.clicked.connect(self.onClickCheckPID)

    def create_checkable_button(self, text):
        """Create a checkable button with the given text."""
        button = QPushButton(text)
        button.setCheckable(True)
        return button

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
            General.get_data_subject(flag=selected_button.lower(), pid2lookfor=subj_details.pid.iloc[0]) #GP: PID not integer

            if selected_button.lower() == 'preoperative':
                dialog_date = PreoperativeDialog(parent=self)
            elif selected_button.lower() == 'intraoperative':
                dialog_date = IntraoperativeDialog(parent=self)
            else:
                dialog_date = PostoperativeDialog(parent=self)

            dialog_date.exec_()

    def onClickGeneralData(self):
        """Opens the General Data GUI"""
        dialog_general_data = CheckForGeneralData(instance = 'GUImain', parent=self)
        dialog_general_data.show()

    def onClickDeleteData(self):
        current_subject_df = General.read_current_subj()
        id = current_subject_df['id'].iloc[0]
        pid = current_subject_df['pid'].iloc[0]
        reply = Output.delete_msg_box(pid_subject=pid)

        if reply:
            Clean.delete_subject_data(subject_id=id)
            # Load the updated general_data.csv
            df = General.import_dataframe('general_data.csv', separator_csv=',')
            # Get the last index
            last_index = df.index[-1]
            # Write the last index to a temporary file
            General.write_csv_temp(df, [last_index])
            self.restart_program()
        else:
            QMessageBox.information(self, 'Action Cancelled', 'Data deletion has been cancelled.')

    def onClickChangePatient(self):
        filename2load = 'general_data.csv'
        General.get_data_subject(flag='general_data', pid2lookfor=self.pid_list.currentText()) #TODO change pid2lookfor to id2lookfor
        df = General.import_dataframe(filename2load, separator_csv=',')
        idx_PID = df.index[df['PID_ORBIS'] == f"PID_{self.pid_list.currentText()}"].to_list()
        print(idx_PID)

        General.write_csv_temp(df, idx_PID)  # creates a new temporary file called current_subj.csv in ./temp
        self.restart_program()

    def onClickCheckPID(self):
        """Opens the Check PID GUI"""
        dialog_check_pid = CheckPID(parent=self)
        dialog_check_pid.exec_()
        self.restart_program()

    def onClickAddNewPID(self):
        """Opens the Add New PID GUI"""
        dialog_add_new_pid = CheckForGeneralData(parent=self)
        dialog_add_new_pid.exec_()
        self.restart_program()

    def check_current_subject(self):
        current_subj_path = os.path.join(ROOTDIR, 'temp', 'current_subj.csv')
        general_data_path = os.path.join(FILEDIR, 'general_data.csv')

        # Load the current_subj.csv file
        current_subj_df = pds.read_csv(current_subj_path)

        # Load the general_data.csv file
        general_data_df = pds.read_csv(general_data_path)

        # Check if the id in current_subj is in the ID column of general_data
        current_id = current_subj_df['pid'].iloc[0]
        if current_id in general_data_df['PID_ORBIS'].values:
            self.setWindowTitle(f'Choose GUI for subj with PID: {current_id.strip("PID_")}')
        else:
            self.setWindowTitle('No PID chosen')
            self.button_openGUI_Postoperative.setEnabled(False)
            self.button_openGUI_Intraoperative.setEnabled(False)
            self.button_openGUI_Preoperative.setEnabled(False)
            self.button_general_data.setEnabled(False)
            self.button_delete_data.setEnabled(False)

    def populate_pid_list(self):
        filename2load = 'general_data.csv'
        df = General.import_dataframe(filename2load, separator_csv=',')

        self.pid_list.clear()
        self.pid_list.setEnabled(True)
        self.button_change_patient.setEnabled(True)
        # Sort the PID_ORBIS values
        sorted_pids = sorted(df['PID_ORBIS'].str.strip("PID_"))

        # Iterate through each sorted PID_ORBIS and add it to the combobox
        for pid in sorted_pids:
            self.pid_list.addItem(pid)
        try:
            curr_no = df.index[df['PID_ORBIS'] == General.read_current_subj().pid[0]].tolist()[0]
            self.pid_list.setCurrentIndex(curr_no)
        except IndexError: pass

    def restart_program(self):
        """Restart the program by creating a new instance of the main class."""
        self.close()  # Close the current instance
        self.__init__() # Reinitialize the class
        self.show()  # Show the new instance

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(f'{ROOTDIR}/test/unimr_lead_image.png'))
    dlg = ChooseGUI()
    dlg.show()
    sys.exit(app.exec_())