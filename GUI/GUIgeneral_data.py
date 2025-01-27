import sys, os
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QVBoxLayout, QGroupBox, QHBoxLayout, \
    QWidget, QLabel, QComboBox, QCalendarWidget, QMessageBox
from utils.helper_functions import General
from dependencies import FILEDIR, ROOTDIR

class CheckForGeneralData(QDialog):
    """GUI which provides a mean to enter all the general data of a patient"""

    def __init__(self, instance=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Enter data for the unknown subject')
        self.setGeometry(400, 100, 1000, 400)  # left, right, width, height
        self.move(550, 200)
        self.textfield_width = 450
        self.instance = instance  # GP: if general_data gets accessed through GUImain

        self.init_ui()
        if self.instance:
            self.setWindowTitle(f'Change general data for current subject')
            self.read_general_data()

    def init_ui(self):
        self.layout = QVBoxLayout(self)  # entire layout for GUI
        self.content_box = QVBoxLayout(self)  # content of the box

        self.create_option_box()
        self.create_buttons()

        self.layout.addLayout(self.content_box)
        self.layout.addLayout(self.layout_buttons)

    def create_option_box(self):
        """Create the option box with input fields"""
        self.optionbox_guistart = QGroupBox('Please enter all data for the new subject:')
        self.settings_optionbox1 = QVBoxLayout(self.optionbox_guistart)

        self.subj_surname = QLabel('Surname:\t\t')
        self.lineEditSurname = QLineEdit()
        self.lineEditSurname.setFixedWidth(self.textfield_width)
        self.lineEditSurname.setFixedHeight(50)

        self.subj_name = QLabel('Name:\t\t\t')
        self.lineEditName = QLineEdit()
        self.lineEditName.setFixedWidth(self.textfield_width)
        self.lineEditName.setFixedHeight(50)

        self.subj_birthdate = QLabel('Birthdate:\t\t')
        self.lineEditBirthdate = CustomLineEdit()
        self.lineEditBirthdate.setFixedWidth(self.textfield_width)
        self.lineEditBirthdate.setFixedHeight(50)
        self.lineEditBirthdate.clicked.connect(self.open_calendar)
        self.lineEditBirthdate.editingFinished.connect(self.validate_birthdate)

        self.subj_PID = QLabel('PID: \t\t\t')
        self.lineEditPID = QLineEdit()
        self.lineEditPID.setFixedWidth(self.textfield_width)
        self.lineEditPID.setFixedHeight(50)

        self.subj_ID = QLabel('ID:\t\t\t')
        self.lineEditID = QLineEdit()
        self.lineEditID.setText(General.create_pseudonym(8))
        self.lineEditID.setEnabled(False)
        self.lineEditID.setFixedWidth(self.textfield_width)
        self.lineEditID.setFixedHeight(50)

        self.subj_gender = QLabel('Gender:\t\t\t')
        self.lineEditGender = QComboBox()
        self.lineEditGender.addItems(['Choose gender', 'female', 'male', 'diverse'])
        self.lineEditGender.setFixedWidth(self.textfield_width)
        self.lineEditGender.setFixedHeight(50)
        self.lineEditGender.setCurrentIndex(0)

        self.subj_diagnosis = QLabel('Diagnosis:\t\t')
        self.lineEditDiagnosis = QComboBox()
        self.lineEditDiagnosis.addItems(['Choose diagnosis',
                                         'Bradykinetic-rigid parkinson-syndrome (PD1)',
                                         'Tremordominant parkinson-syndrome(PD2)',
                                         'Mixed-type parkinson-syndrome (PD3)',
                                         'Dystonia (DT)',
                                         'Essential tremor (ET)', 'Equivalence type parkinson-syndrome',
                                         'Hypokinetic-rigid type parkinson-syndrome',
                                         'Akinetic-rigid type parkinson-syndrome',
                                         'Other'])

        self.lineEditDiagnosis.setFixedWidth(self.textfield_width)
        self.lineEditDiagnosis.setFixedHeight(50)
        self.lineEditDiagnosis.setCurrentIndex(0)

        self.subj_side = QLabel('Side Dominance:\t\t')
        self.lineEditDominance = QComboBox()
        self.lineEditDominance.addItems(['Choose side dominance', 'right', 'left', 'unknown'])
        self.lineEditDominance.setCurrentIndex(0)
        self.lineEditDominance.setFixedWidth(self.textfield_width)
        self.lineEditDominance.setFixedHeight(50)

        self.subj_ipg = QLabel('IPG serial number:\t')
        self.lineEditIPG = QLineEdit()
        self.lineEditIPG.setFixedWidth(self.textfield_width)
        self.lineEditIPG.setFixedHeight(50)

        self.add_widgets_to_layout()

    def add_widgets_to_layout(self):
        """Add widgets to the layout"""
        self.settings_optionbox1.addLayout(self.create_hbox_layout(self.subj_surname, self.lineEditSurname))
        self.settings_optionbox1.addLayout(self.create_hbox_layout(self.subj_name, self.lineEditName))
        self.settings_optionbox1.addLayout(self.create_hbox_layout(self.subj_birthdate, self.lineEditBirthdate))
        self.settings_optionbox1.addLayout(self.create_hbox_layout(self.subj_PID, self.lineEditPID))
        self.settings_optionbox1.addLayout(self.create_hbox_layout(self.subj_ID, self.lineEditID))
        self.settings_optionbox1.addLayout(self.create_hbox_layout(self.subj_gender, self.lineEditGender))
        self.settings_optionbox1.addLayout(self.create_hbox_layout(self.subj_diagnosis, self.lineEditDiagnosis))
        self.settings_optionbox1.addLayout(self.create_hbox_layout(self.subj_side, self.lineEditDominance))
        self.settings_optionbox1.addLayout(self.create_hbox_layout(self.subj_ipg, self.lineEditIPG))
        self.content_box.addWidget(self.optionbox_guistart)

    def create_hbox_layout(self, label, line_edit):
        """Create a horizontal box layout with a label and a line edit"""
        hbox = QHBoxLayout()
        hbox.addWidget(label)
        hbox.addWidget(line_edit)
        hbox.addStretch()
        return hbox

    def create_buttons(self):
        """Create the buttons at the bottom"""
        self.layout_buttons = QHBoxLayout()
        self.button_savegeneraldata = QPushButton('Save general data \ninformation')
        self.button_savegeneraldata.clicked.connect(self.onClickedSaveGeneralData)
        self.button_savegeneraldata.setFixedSize(200, 75)
        self.button_close = QPushButton('Close GUI')
        self.button_close.clicked.connect(self.close)
        self.button_close.setFixedSize(200, 75)

        self.layout_buttons.addStretch(1)
        self.layout_buttons.addWidget(self.button_savegeneraldata)
        self.layout_buttons.addWidget(self.button_close)

    def open_calendar(self):
        """opens a calendar in order to enter the birthdate of a subject"""
        self.calendarWindow = QDialog(self)
        self.cal = QCalendarWidget(self.calendarWindow)
        self.cal.setGridVisible(True)
        self.cal.clicked[QtCore.QDate].connect(self.showDate)

        hbox = QHBoxLayout()
        hbox.addWidget(self.cal)
        self.calendarWindow.setLayout(hbox)
        self.calendarWindow.setGeometry(100, 500, 900, 500)
        self.calendarWindow.setWindowTitle('Calendar')
        self.calendarWindow.exec_()

    def showDate(self, date):
        formatted_date = date.toString('dd/MM/yyyy')  # Format the date as DD/MM/YYYY
        self.lineEditBirthdate.setText(formatted_date)
        self.calendarWindow.close()

    def validate_birthdate(self):
        date_text = self.lineEditBirthdate.text()
        formatted_date = General.validate_and_format_dates(date_text)
        if formatted_date == 'Invalid date format':
            QMessageBox.warning(self, 'Invalid Date', 'The entered date is invalid. Please enter a date in the format DD/MM/YYYY.')
        else:
            self.lineEditBirthdate.setText(formatted_date)

    def read_general_data(self):
        """Reads the PID from current_subject.csv and populates the corresponding data from general_data.csv into the GUI inputs."""
        current_subject_df = General.read_current_subj()
        general_data_path = os.path.join(FILEDIR, 'general_data.csv')

        # Read the current subject file to get the PID
        pid = current_subject_df['pid'].iloc[0]

        # Read the general data file to get the corresponding data
        general_data_df = pd.read_csv(general_data_path)
        subject_data = general_data_df[general_data_df['PID_ORBIS'] == pid].iloc[0]

        print(subject_data)

        # Populate the GUI inputs with the retrieved data
        self.lineEditSurname.setText(str(subject_data['surname']))
        self.lineEditName.setText(str(subject_data['name']))
        self.lineEditBirthdate.setText(str(subject_data['birthdate']))
        self.lineEditPID.setText(str(subject_data['PID_ORBIS']).strip("PID_"))
        self.lineEditPID.setEnabled(False)
        self.lineEditID.setText(str(subject_data['ID']))
        self.lineEditID.setEnabled(False)
        self.lineEditGender.setCurrentText(str(subject_data['gender']))
        self.lineEditDiagnosis.setCurrentText(str(subject_data['diagnosis']))
        self.lineEditDominance.setCurrentText(str(subject_data['side_dominance']))
        self.lineEditIPG.setText(str(subject_data['IPG_serial_number']).strip("IPG_"))

    @QtCore.pyqtSlot()
    def onClickedSaveGeneralData(self):
        """when button is pressed, data is added to ./data/general_data.csv """
        required_fields = [
            self.lineEditSurname,
            self.lineEditName,
            self.lineEditBirthdate,
            self.lineEditPID,
            self.lineEditID,
            self.lineEditGender,
            self.lineEditDiagnosis,
            self.lineEditDominance,
            self.lineEditIPG
        ]

        missing_list = []
        for field, name in zip(required_fields,
                               ['Surname', 'Name', 'Birthdate', 'PID', 'ID', 'Gender', 'Diagnosis', 'Side Dominance',
                                'IPG']):
            if isinstance(field, QLineEdit) and not field.text():
                missing_list.append(name)
            elif isinstance(field, QComboBox) and 'Choose' in field.currentText():
                missing_list.append(name)

        if missing_list:
            QMessageBox.warning(self, 'Missing Information',
                                f'Please fill in the following fields:\n\n{", \n".join(missing_list)}')
            return
        else:
            filename2load = os.path.join(FILEDIR, 'general_data.csv')
            df = General.import_dataframe(filename2load, separator_csv=',')
            pid_orbis = f'PID_{self.lineEditPID.text()}'
            if self.instance:
                # Update the existing PID
                pid = self.lineEditPID.text()
                print(pid)
                idx_PID = df.index[df['PID_ORBIS'] == pid_orbis].to_list()
                print(idx_PID)
                if not idx_PID:
                    QMessageBox.warning(self, 'PID Not Found', f'The PID {pid_orbis} was not found in the data.')
                    return
                idx = idx_PID[0]
                df.at[idx, 'surname'] = self.lineEditSurname.text()
                df.at[idx, 'name'] = self.lineEditName.text()
                df.at[idx, 'birthdate'] = self.lineEditBirthdate.text()
                df.at[idx, 'ID'] = self.lineEditID.text()
                df.at[idx, 'gender'] = self.lineEditGender.currentText()
                df.at[idx, 'diagnosis'] = self.lineEditDiagnosis.currentText()
                df.at[idx, 'side_dominance'] = self.lineEditDominance.currentText()
                df.at[idx, 'IPG_serial_number'] = f"IPG_{self.lineEditIPG.text()}" #dtype problem

                df.to_csv(filename2load, index=False, sep=',')
            else:
                filename2load = os.path.join(FILEDIR, 'general_data.csv')
                df = General.import_dataframe(filename2load, separator_csv=',')
                pid_orbis = f'PID_{self.lineEditPID.text()}'

                # Check if the PID already exists
                if pid_orbis in df['PID_ORBIS'].values:
                    QMessageBox.warning(self, 'Duplicate PID', f'The PID {pid_orbis} already exists in the data.')
                    return
                entered_data = [self.lineEditSurname.text(),
                                self.lineEditName.text(),
                                self.lineEditBirthdate.text(),
                                pid_orbis,
                                self.lineEditID.text(),
                                len(df.index),
                                str(self.lineEditGender.currentText()),
                                str(self.lineEditDiagnosis.currentText()),
                                str(self.lineEditDominance.currentText()),
                                self.lineEditIPG.text()]
                df.loc[len(df)] = entered_data
                df.to_csv(filename2load, index=False, sep=',')

                # set current_subject to just entered pid
                General.get_data_subject(flag='general_data', pid2lookfor=pid_orbis)
                df = General.import_dataframe(filename2load, separator_csv=',')
                idx_PID = df.index[df['PID_ORBIS'] == pid_orbis].to_list()

                if not idx_PID:
                    QMessageBox.warning(self, 'PID Not Found', f'The PID {pid_orbis} was not found in the data.')
                    return

                General.write_csv_temp(df, idx_PID)
                self.close()
            return

class CustomLineEdit(QLineEdit):
    """this class intends to make the LineEdit clickable; code adapted from:
    https://stackoverflow.com/questions/49901868/onclick-event-for-textboxes-in-pyqt5"""
    clicked = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = CheckForGeneralData()
    dlg.show()
    sys.exit(app.exec_())