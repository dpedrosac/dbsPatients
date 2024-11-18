#!/usr/bin/env python3
import sys, os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLineEdit, QVBoxLayout, QGroupBox, QHBoxLayout, \
    QWidget, QLabel, QComboBox, QCalendarWidget, QMessageBox

from utils.helper_functions import General
from dependencies import FILEDIR


class CheckForGeneralData(QDialog):
    """GUI which provides a mean to enter all the general data of a patient (Name, Surname, etc.).
    Several options are possible after entering all the details:
    1. add the data, 2. close the GUI"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # ====================    Create General Layout      ====================
        self.setWindowTitle('Enter data for the unknown subject')
        self.setGeometry(400, 100, 1000, 400)  # left, right, width, height
        self.move(550, 200)
        textfield_width = 450

        self.calendarWindow = QWidget()
        self.layout = QVBoxLayout(self)  # entire layout for GUI
        self.content_box = QVBoxLayout(self)  # content of the box

        # ====================    Create Content for only option box       ====================
        self.optionbox_guistart = QGroupBox('Please enter all data for the new subject:')
        self.settings_optionbox1 = QVBoxLayout(self.optionbox_guistart)

        self.subj_surname = QLabel('Surname:\t\t')
        self.lineEditSurname = QLineEdit()

        self.lineEditSurname.setFixedWidth(textfield_width)
        self.lineEditSurname.setFixedHeight(50)

        lay1 = QHBoxLayout()
        lay1.addWidget(self.subj_surname)
        lay1.addWidget(self.lineEditSurname)
        lay1.addStretch()

        self.subj_name = QLabel('Name:\t\t\t')
        self.lineEditName = QLineEdit()

        self.lineEditName.setFixedWidth(textfield_width)
        self.lineEditName.setFixedHeight(50)

        lay2 = QHBoxLayout()
        lay2.addWidget(self.subj_name)
        lay2.addWidget(self.lineEditName)
        lay2.addStretch()

        self.subj_name = QLabel('Name Suffix:\t\t')
        self.lineEditNameSuffix = QLineEdit()

        self.lineEditNameSuffix.setFixedWidth(textfield_width)
        self.lineEditNameSuffix.setFixedHeight(50)

        lay3 = QHBoxLayout()
        lay3.addWidget(self.subj_name)
        lay3.addWidget(self.lineEditNameSuffix)
        lay3.addStretch()

        self.subj_birthdate = QLabel('Birthdate:\t\t')
        self.lineEditBirthdate = CustomLineEdit()
        self.lineEditBirthdate.setFixedWidth(textfield_width)
        self.lineEditBirthdate.setFixedHeight(50)
        self.lineEditBirthdate.clicked.connect(self.open_calendar)
        self.lineEditBirthdate.editingFinished.connect(self.validate_birthdate)

        lay4 = QHBoxLayout()
        lay4.addWidget(self.subj_birthdate)
        lay4.addWidget(self.lineEditBirthdate)
        lay4.addStretch()

        self.subj_PID = QLabel('PID (without zeros):\t')
        self.lineEditPID = QLineEdit()

        self.lineEditPID.setFixedWidth(textfield_width)
        self.lineEditPID.setFixedHeight(50)

        lay6 = QHBoxLayout()
        lay6.addWidget(self.subj_PID)
        lay6.addWidget(self.lineEditPID)
        lay6.addStretch()

        self.subj_ID = QLabel('ID:\t\t\t')
        self.lineEditID = QLineEdit()
        self.lineEditID.setText(General.create_pseudonym(8))

        self.lineEditID.setFixedWidth(textfield_width)
        self.lineEditID.setFixedHeight(50)

        lay7 = QHBoxLayout()
        lay7.addWidget(self.subj_ID)
        lay7.addWidget(self.lineEditID)
        lay7.addStretch()

        self.subj_gender = QLabel('Gender:\t\t\t')
        self.lineEditGender = QComboBox()
        self.lineEditGender.addItems(['female', 'male', 'diverse'])
        self.lineEditGender.setFixedWidth(textfield_width)
        self.lineEditGender.setFixedHeight(50)

        lay8 = QHBoxLayout()
        lay8.addWidget(self.subj_gender)
        lay8.addWidget(self.lineEditGender)
        lay8.addStretch()

        self.subj_diagnosis = QLabel('Diagnosis:\t\t')
        self.lineEditDiagnosis = QComboBox()
        self.lineEditDiagnosis.addItems(['Bradykinetic-rigid parkinson-syndrome (PD1)',
                                         'Tremordominant parkinson-syndrome(PD2)',
                                         'Mixed-type parkinson-syndrome (PD3)',
                                         'Dystonia (DT)',
                                         'Essential tremor (ET)', 'Equivalence type parkinson-syndrome',
                                         'Hypokinetic-rigid type parkinson-syndrome',
                                         'Akinetic-rigid type parkinson-syndrome',
                                         'Other'])

        self.lineEditDiagnosis.setFixedWidth(textfield_width)
        self.lineEditDiagnosis.setFixedHeight(50)

        lay9 = QHBoxLayout()
        lay9.addWidget(self.subj_diagnosis)
        lay9.addWidget(self.lineEditDiagnosis)
        lay9.addStretch()

        self.subj_side = QLabel('Side Dominance:\t\t')
        self.lineEditDominance = QComboBox()
        self.lineEditDominance.addItems(['right', 'left', 'unknown'])

        self.lineEditDominance.setFixedWidth(textfield_width)
        self.lineEditDominance.setFixedHeight(50)

        lay10 = QHBoxLayout()
        lay10.addWidget(self.subj_side)
        lay10.addWidget(self.lineEditDominance)
        lay10.addStretch()

        self.subj_side = QLabel('IPG serial number:\t')
        self.lineEditIPG = QLineEdit()

        self.lineEditIPG.setFixedWidth(textfield_width)
        self.lineEditIPG.setFixedHeight(50)

        lay11 = QHBoxLayout()
        lay11.addWidget(self.subj_side)
        lay11.addWidget(self.lineEditIPG)
        lay11.addStretch()

        self.settings_optionbox1.addLayout(lay1)
        self.settings_optionbox1.addLayout(lay2)
        self.settings_optionbox1.addLayout(lay3)
        self.settings_optionbox1.addLayout(lay4)
        self.settings_optionbox1.addLayout(lay6)
        self.settings_optionbox1.addLayout(lay7)
        self.settings_optionbox1.addLayout(lay8)
        self.settings_optionbox1.addLayout(lay9)
        self.settings_optionbox1.addLayout(lay10)
        self.settings_optionbox1.addLayout(lay11)
        self.content_box.addWidget(self.optionbox_guistart)

        # ====================    Create Content for Buttons at the Bottom      ====================
        layout_buttons = QHBoxLayout()
        self.button_savegeneraldata = QPushButton('Add general data \ninformation')
        self.button_savegeneraldata.clicked.connect(self.onClickedSaveGeneralData)
        self.button_close = QPushButton('Close GUI')
        self.button_close.clicked.connect(self.close)

        layout_buttons.addStretch(1)
        layout_buttons.addWidget(self.button_savegeneraldata)
        layout_buttons.addWidget(self.button_close)

        # ====================    Add boxes and buttons to self.entire_layout      ====================
        self.layout.addLayout(self.content_box)
        self.layout.addLayout(layout_buttons)

    @QtCore.pyqtSlot()
    def open_calendar(self):
        """opens a calender in order to enter the birthdate of a subject"""

        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.clicked[QtCore.QDate].connect(self.showDate)

        # create a new window that contains the calendar taken from:
        hbox = QHBoxLayout()
        hbox.addWidget(self.cal)
        self.calendarWindow.setLayout(hbox)
        self.calendarWindow.setGeometry(300, 300, 415, 350)
        self.calendarWindow.setWindowTitle('Calendar')
        self.calendarWindow.show()

    def showDate(self, date):
        self.lineEditBirthdate.setText(str(date.toPyDate()))

    def validate_birthdate(self):
        date_text = self.lineEditBirthdate.text()
        formatted_date = General.validate_and_format_dates(date_text)
        if formatted_date == 'Invalid date format':
            #GP: invalid date format
            QMessageBox.warning(self, 'Invalid Date', 'The entered date is invalid. Please enter a date in the format DD/MM/YYYY.')
        else:
            self.lineEditBirthdate.setText(formatted_date)

    # In the next lines, actions are defined when Buttons are pressed
    @QtCore.pyqtSlot()
    def onClickedSaveGeneralData(self):
        """when button is pressed, data is added to ./data/general_data.csv """

        filename2load = os.path.join(FILEDIR, 'general_data.csv')
        df = General.import_dataframe(filename2load, separator_csv=',')
        entered_data = [self.lineEditSurname.text(),
                        self.lineEditName.text(),
                        self.lineEditBirthdate.text(),
                        self.lineEditPID.text(),
                        self.lineEditID.text(),
                        len(df.index),
                        str(self.lineEditGender.currentText()),
                        str(self.lineEditDiagnosis.currentText()),
                        str(self.lineEditDominance.currentText()),
                        self.lineEditIPG.text()]
        df.loc[len(df)] = entered_data
        df.to_csv(filename2load, index=False, sep=',')

        #GP: changes current_subj to the one just added to general_data

        filename2load = 'general_data.csv'
        General.get_data_subject(flag='general_data', pid2lookfor=self.lineEditPID.text())
        df = General.import_dataframe(filename2load, separator_csv=',')
        PID2lookfor = self.lineEditPID.text().lstrip('0')  # string that is searched for in metadata file
        idx_PID = df.index[df['PID_ORBIS'] == int(PID2lookfor)].to_list()
        General.write_csv_temp(df, idx_PID)  # creates a new temporary file called current_subj.csv in ./temp

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
