#!/usr/bin/env python3
import logging
import sys
from pathlib import Path

import pandas as pds
from PyQt5 import QtCore
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QGroupBox, QSpacerItem, QSizePolicy, \
    QHBoxLayout, QGridLayout, QLineEdit, QLabel, QListWidget, QCheckBox, QComboBox

import dependencies
from GUI.GUImedication import MedicationDialog
from GUI.GUIsettingsDBS import DBSsettingsDialog
from utils.helper_functions import General, Content, Clean
from dependencies import FILEDIR, ROOTDIR, MEDICATION, SYSTEMS

pds.options.mode.chained_assignment = None  # default='warn' cf.
# https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas

# TODO's: needs fix: go on 'save and return' after entering data before entering medicationGUI,
#  or else on 'return' all windows close and data will be deleted


# Added lines for loading selected list items
def setitemactive(itemname: str, listwidget: QListWidget):
    """
    check for itemname in list, if it exists set the item active
    Args:
        itemname: name of searched item
        listwidget: QListWidget to be searched

    Returns: none        self.optionbox2 = QGroupBox('Surgery')
        self.optionbox2Content = QVBoxLayout(self.optionbox2)
        layout_general.addWidget(self.optionbox2, 0, 1)
        # Surgery Date
        self.SurgeryDate = QLabel('Surgery Date \n(dd/mm/yyyy):\t')
        self.lineEditSurgeryDate = QLineEdit()

        box2line1 = QHBoxLayout()
        box2line1.addWidget(self.SurgeryDate)
        box2line1.addWidget(self.lineEditSurgeryDate)
        # box2line1.addStretch()
        # Target List
        self.targetLabel = QLabel('Target:\t\t')
        self.targetLabel.setAlignment(QtCore.Qt.AlignTop)
        self.targetList = QListWidget()
        self.targetList.show()
        ls = ['STN', 'GPi', 'VLp', 'Other']
        for k in ls:
            self.targetList.addItem(k)

        box2line2 = QHBoxLayout()
        box2line2.addWidget(self.targetLabel)
        box2line2.addWidget(self.targetList)

        self.optionbox2Content.addLayout(box2line1)
        self.optionbox2Content.addStretch()
        self.optionbox2Content.addLayout(box2line2)
        self.optionbox2.setLayout(self.optionbox2Content)


    """
    list_items = [n.text() for n in listwidget.findItems(".*", Qt.MatchRegExp)]
    if itemname in list_items:
        listwidget.setCurrentItem(
            listwidget.findItems(itemname, Qt.MatchExactly)[0]
        )


class IntraoperativeDialog(QDialog):
    """Dialog to introduce all important information of intraoperative visit. """

    def __init__(self, parent=None):
        super(IntraoperativeDialog, self).__init__(parent)
        self.dialog_medication, self.dialog_DBSsettings, self.content_widgets = None, None, None  # initialised  Dialogs
        self.date = 'intraoperative'  # defines the date at which data are taken from/saved at
        self.setup_ui()

    def setup_ui(self):
        self.setup_general_layout()

    def setup_general_layout(self):
        """Defines the general layout for the GUI"""
        subj_details = General.read_current_subj()  # reads information for the subject last bein processed
        General.synchronize_data_with_general(self.date, subj_details.id[0],
                                              messagebox=False)  # for identical general columns in 'preoperative.csv'

        self.create_medication_dialog()
        self.create_DBSsettings_dialog()

        self.setWindowTitle(f'Please insert the intraoperative patient data (PID: {int(subj_details.pid)})')
        self.setGeometry(200, 100, 280, 170)
        self.move(400, 200)

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # Option boxes appearing in the intraoperative GUI
        # Create optionbox for important dates
        self.optionbox_dates_intraoperative(layout_general)

        # Create optionbox for general data
        self.optionbox_general_intraoperative(layout_general)

        # Create optionbox for general data
        self.optionbox_intraoperative_data(layout_general)

        # Create buttons at the bottom of the GUI
        self.create_bottom_buttons_intraoperative(layout_general)

        # Connect button actions that are needed so that everything works
        self.connect_button_actions()

    def initialize_content(self):
        """Initializes the contant that may be needed later for reading or saving data from/to csv-files
        TODO: needs to be adapted for intraoperative data"""

        self.content_widgets = {
            'First_Diagnosed_preop': 'lineEditFirstDiagnosed',
            'Admission_preop': 'lineEditAdmNeurIndCheck',
            'Dismissal_preop': 'lineEditDismNeurIndCheck',
            'Outpat_Contact_preop': 'lineEditOutpatientContact',
            'nch_preop': 'lineEditNsurgContact',
            'DBS_Conference_preop': 'lineEditDBSconference',
            'H&Y_preop': 'hy',
            'UPDRS_On_preop': 'updrsON',
            'UPDRS_Off_preop': 'updrsOFF',
            'UPDRSII_preop': 'updrsII',
            'HRUQ_preop': 'hruq',
            'MoCa_preop': 'moca',
            'MMST_preop': 'mmst',
            'BDI2_preop': 'bdi2',
            'NMSQ_preop': 'nmsq',
            'EQ5D_preop': 'eq5d',
            'DemTect_preop': 'demtect',
            'PDQ8_preop': 'pdq8',
            'PDQ39_preop': 'pdq39',
            'S&E_preop': 'se',
        }

    def create_medication_dialog(self):
        self.dialog_medication = MedicationDialog(parent=self, visit=self.date)  # creates medication dialog
        self.dialog_medication.hide()

    def create_DBSsettings_dialog(self):
        self.dialog_DBSsettings = DBSsettingsDialog(parent=self, visit=self.date)  # creates medication dialog
        self.dialog_DBSsettings.hide()

    def optionbox_dates_intraoperative(self, layout_general):
        """creates upper left optionbox in which important dates are added"""

        def create_line_edit_for_dates(label_text, line_edit_width=500, label_width=800):
            label = QLabel(f'{label_text} (dd/mm/yyyy):\t\t')
            label.setFixedWidth(label_width)
            line_edit = QLineEdit()
            line_edit.setEnabled(False)
            line_edit.setFixedWidth(line_edit_width)
            return label, line_edit

        def create_horizontal_layout_dates(*widgets):
            layout = QHBoxLayout()
            for widget in widgets:
                layout.addWidget(widget)
            layout.addStretch(1)
            return layout

        self.optionbox_dates_intraoperative = QGroupBox('Important dates')
        self.optionbox_datesContent = QVBoxLayout(self.optionbox_dates_intraoperative)
        layout_general.addWidget(self.optionbox_dates_intraoperative, 0, 0)

        admission_Nch, self.lineEditAdmission_Nch = create_line_edit_for_dates('Admission Neurosurgery')
        admission_NR, self.lineEditAdmission_NR = create_line_edit_for_dates('Admission Neurology')
        dismission_Nch, self.lineEditDismission_Nch = create_line_edit_for_dates('Dismission Neurosurgery')
        dismission_NR, self.lineEditDismission_NR = create_line_edit_for_dates('Dismission Neurology')
        surgeryDate, self.lineEditSurgeryDate = create_line_edit_for_dates('Surgery Date')

        # Create lines of layout
        testbox_line1 = create_horizontal_layout_dates(admission_Nch, self.lineEditAdmission_Nch)
        testbox_line2 = create_horizontal_layout_dates(admission_NR, self.lineEditAdmission_NR)
        testbox_line3 = create_horizontal_layout_dates(dismission_Nch, self.lineEditDismission_Nch)
        testbox_line4 = create_horizontal_layout_dates(dismission_NR, self.lineEditDismission_NR)
        testbox_line5 = create_horizontal_layout_dates(surgeryDate, self.lineEditSurgeryDate)

        # Add layouts to option box content
        self.optionbox_datesContent.addLayout(testbox_line1)
        self.optionbox_datesContent.addLayout(testbox_line2)
        self.optionbox_datesContent.addLayout(testbox_line3)
        self.optionbox_datesContent.addLayout(testbox_line4)
        self.optionbox_datesContent.addLayout(testbox_line5)

        self.optionbox_dates_intraoperative.setLayout(self.optionbox_datesContent)

    def optionbox_general_intraoperative(self, layout_general):
        """General data for the intraoperative recordings"""

        self.optionbox_general = QGroupBox('General data')
        self.optionbox_generalContent = QVBoxLayout(self.optionbox_general)
        layout_general.addWidget(self.optionbox_general, 0, 1)

        # Target List
        targetLabel = QLabel('Target:\t\t')
        targetLabel.setAlignment(QtCore.Qt.AlignTop)
        self.targetList = QListWidget()
        self.targetList.show()
        ls = ['STN', 'GPi', 'VLp', 'Other']
        for k in ls:
            self.targetList.addItem(k)

        textbox_line1 = QHBoxLayout()
        textbox_line1.addWidget(targetLabel)
        textbox_line1.addWidget(self.targetList)

        self.optionbox_generalContent.addLayout(textbox_line1)
        self.optionbox_general.setLayout(self.optionbox_generalContent)

    def optionbox_intraoperative_data(self, layout_general):
        self.optionbox3 = QGroupBox('Intraoperative')
        self.optionbox3Content = QVBoxLayout(self.optionbox3)
        layout_general.addWidget(self.optionbox3, 1, 0)
        # Checkboxes Reports
        self.ReportNeurCheck = QCheckBox()
        self.ReportNeurLabel = QLabel('Report Neurology')
        self.ReportNeurLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.AwakePatientCheck = QCheckBox()
        self.AwakePatientLabel = QLabel('Awake Patient')
        self.AwakePatientLabel.setAlignment(QtCore.Qt.AlignLeft)

        box3line1 = QHBoxLayout()
        box3line1.addWidget(self.ReportNeurCheck)
        box3line1.addWidget(self.ReportNeurLabel)
        box3line1.addStretch()
        box3line1.addWidget(self.AwakePatientCheck)
        box3line1.addWidget(self.AwakePatientLabel)
        box3line1.addStretch()

        self.ReportNChCheck = QCheckBox()
        self.ReportNChLabel = QLabel('Report Neurosurgery\t')
        self.ReportNChLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.ProtocolNeurCheck = QCheckBox()
        self.ProtocolNeurLabel = QLabel('Protocol Neurology')
        self.ProtocolNeurLabel.setAlignment(QtCore.Qt.AlignLeft)

        box3line2 = QHBoxLayout()
        box3line2.addWidget(self.ReportNChCheck)
        box3line2.addWidget(self.ReportNChLabel)
        box3line2.addStretch()
        box3line2.addWidget(self.ProtocolNeurCheck)
        box3line2.addWidget(self.ProtocolNeurLabel)
        box3line2.addStretch()

        # Duration and Trajectories enter field
        self.DurationSurgery = QLabel('Duration \nsurgery (min):\t')
        self.lineEditDurationSurgery = QLineEdit()
        self.Trajectories = QLabel('Trajectories:')
        self.lineEditTrajectories = QLineEdit()

        box3line3 = QHBoxLayout()
        box3line3.addWidget(self.DurationSurgery)
        box3line3.addWidget(self.lineEditDurationSurgery)
        box3line3.addWidget(self.Trajectories)
        box3line3.addWidget(self.lineEditTrajectories)
        box3line3.addStretch()
        # List selection neurologist
        self.testingNeurLabel = QLabel('Testing Neurologist(s):')
        self.testingNeurList = QListWidget()
        self.testingNeurList.show()
        ls = ['Oehrn/Weber', 'Pedrosa', 'Waldthaler', 'Other']
        [self.testingNeurList.addItem(k) for k in ls]

        box3line4 = QHBoxLayout()
        box3line4.addWidget(self.testingNeurLabel)
        # box3line4.addStretch()
        box3line4.addWidget(self.testingNeurList)
        box3line4.addStretch()

        self.optionbox3Content.addLayout(box3line1)
        self.optionbox3Content.addLayout(box3line2)
        self.optionbox3Content.addLayout(box3line3)
        self.optionbox3Content.addLayout(box3line4)

        self.optionbox3.setLayout(self.optionbox3Content)

    def create_bottom_buttons_intraoperative(self, layout_general):
        """Creates buttons a) to enter medication, b) to enter DBSsettings c) to save or d) to save and close GUI """

        self.ButtonEnterMedication = QPushButton('Open GUI \nMedication')
        self.ButtonEnterDBSsettings = QPushButton('Open GUI \nDBS settings')
        self.button_buffer = QPushButton('Save')
        self.button_save = QPushButton('Save and \nReturn')

        # Set fixed size for all buttons
        button_width = 200
        button_height = 75

        self.ButtonEnterMedication.setFixedSize(button_width, button_height)
        self.button_buffer.setFixedSize(button_width, button_height)
        self.button_save.setFixedSize(button_width, button_height)

        hlay_bottom = QHBoxLayout()
        hlay_bottom.addStretch(5)
        hlay_bottom.addWidget(self.ButtonEnterMedication)
        hlay_bottom.addWidget(self.ButtonEnterDBSsettings)
        hlay_bottom.addWidget(self.button_buffer)
        hlay_bottom.addWidget(self.button_save)
        hlay_bottom.addStretch(1)
        layout_general.addLayout(hlay_bottom, 4, 0, 1, 3)

        # self.read_content_csv()

    def connect_button_actions(self):
        """Defines the actions that are taken once a button is pressed or specific input is made"""
        # self.lineEditreason.currentIndexChanged.connect(self.update_context)
        # self.lineEditsubjIPG.currentIndexChanged.connect(self.update_IPG)
        self.ButtonEnterMedication.clicked.connect(self.onClickedMedication)
        self.ButtonEnterDBSsettings.clicked.connect(self.onClickedDBSsettings)
        self.button_buffer.clicked.connect(self.onClickedSave)
        self.button_save.clicked.connect(self.onClickedSaveReturn)

    # ====================   Defines actions when buttons are pressed      ====================
    @QtCore.pyqtSlot()
    def onClickedMedication(self):
        """Shows medication dialog ; former implementation with creating GUI was replaced with show/hide GUI which is
        initiated at beginning at the disadvantage of not being saved until GUIintraoperative is closed"""
        self.dialog_medication.show()

    def onClickedDBSsettings(self):
        """shows the DBSsettiongs dialog when button is pressed"""
        self.dialog_DBSsettings.show()

    @QtCore.pyqtSlot()
    def onClickedSave(self):
        self.save_data2csv()

    def onClickedSaveReturn(self):
        """closes GUI and returns to calling (main) GUI"""
        self.save_data2csv()
        self.close()


    def test(self):
        # logger.debug("__init__ created new instance")
        """Initializer."""
        # super().__init__(parent)

        self.date = 'intraoperative'  # defines the date at which data are taken from/saved at
        subj_details = General.read_current_subj()
        General.synchronize_data_with_general(self.date, subj_details.id[0],
                                              messagebox=False)
        # LE: Added for medication dialog to funktion and return properly
        self.dialog_medication = MedicationDialog(parent=self, visit=self.date)  # creates medication dialog
        self.dialog_medication.hide()

        # ====================    Create General Layout      ====================
        self.setWindowTitle('Please insert the data from the intraoperative patient contact ...(PID: {})'
                            .format(str(int(subj_details.pid))))

        # self.setWindowTitle('Please enter preoperative data (PID: {})'.format(str(int(subj_details.pid))))
        self.setGeometry(200, 100, 280, 170)
        self.move(400, 100)
        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # ==================== Optionbox(1)-Admisson and Dismission-, left upper corner   ====================
        # self.optionbox1 = QGroupBox('Admission and Dimission dates')
        # self.optionbox1Content = QVBoxLayout(self.optionbox1)
        # layout_general.addWidget(self.optionbox1, 0, 0)
        #
        # self.AdmNCh = QLabel('Admission Neurosurgery (dd/mm/yyyy):\t')
        # self.lineEditAdmNCh = QLineEdit()
        # self.AdmNeurLabel = QLabel('Admission Neurology (dd/mm/yyyy):\t')
        # self.lineEditAdmNeur = QLineEdit()
        # self.DismNeurLabel = QLabel('Dismission Neurology (dd/mm/yyyy):\t')
        # self.lineEditDismNeur = QLineEdit()
        # self.DismNCh = QLabel('Dismission Neurosurgery (dd/mm/yyyy):\t')
        # self.lineEditDismNCh = QLineEdit()
        #
        # box1line1 = QHBoxLayout()
        # box1line1.addWidget(self.AdmNCh)
        # box1line1.addWidget(self.lineEditAdmNCh)
        # box1line1.addStretch()
        #
        # box1line2 = QHBoxLayout()
        # box1line2.addWidget(self.AdmNeurLabel)
        # box1line2.addWidget(self.lineEditAdmNeur)
        # box1line2.addStretch()
        #
        # box1line3 = QHBoxLayout()
        # box1line3.addWidget(self.DismNeurLabel)
        # box1line3.addWidget(self.lineEditDismNeur)
        # box1line3.addStretch()
        #
        # box1line4 = QHBoxLayout()
        # box1line4.addWidget(self.DismNCh)
        # box1line4.addWidget(self.lineEditDismNCh)
        # box1line4.addStretch()
        #
        # self.optionbox1Content.addLayout(box1line1)
        # self.optionbox1Content.addLayout(box1line2)
        # self.optionbox1Content.addLayout(box1line3)
        # self.optionbox1Content.addLayout(box1line4)
        # self.optionbox1.setLayout(self.optionbox1Content)

        # # ==================== Optionbox (2)-Surgery-, right upper corner   ====================
        # self.optionbox_general = QGroupBox('Surgery')
        # self.optionbox_generalContent = QVBoxLayout(self.optionbox_general)
        # layout_general.addWidget(self.optionbox_general, 0, 1)
        # # Surgery Date
        # self.SurgeryDate = QLabel('Surgery Date \n(dd/mm/yyyy):\t')
        # self.lineEditSurgeryDate = QLineEdit()
        #
        # box2line1 = QHBoxLayout()
        # box2line1.addWidget(self.SurgeryDate)
        # box2line1.addWidget(self.lineEditSurgeryDate)
        # # box2line1.addStretch()
        # # Target List
        # self.targetLabel = QLabel('Target:\t\t')
        # self.targetLabel.setAlignment(QtCore.Qt.AlignTop)
        # self.targetList = QListWidget()
        # self.targetList.show()
        # ls = ['STN', 'GPi', 'VLp', 'Other']
        # for k in ls:
        #     self.targetList.addItem(k)
        #
        # box2line2 = QHBoxLayout()
        # box2line2.addWidget(self.targetLabel)
        # box2line2.addWidget(self.targetList)
        #
        # self.optionbox_generalContent.addLayout(box2line1)
        # self.optionbox_generalContent.addStretch()
        # self.optionbox_generalContent.addLayout(box2line2)
        # self.optionbox_general.setLayout(self.optionbox_generalContent)

        # ==================== Optionbox(3)-Intraoperative-, upper middle left ====================
        # self.optionbox3 = QGroupBox('Intraoperative')
        # self.optionbox3Content = QVBoxLayout(self.optionbox3)
        # layout_general.addWidget(self.optionbox3, 1, 0)
        # # Checkboxes Reports
        # self.ReportNeurCheck = QCheckBox()
        # self.ReportNeurLabel = QLabel('Report Neurology')
        # self.ReportNeurLabel.setAlignment(QtCore.Qt.AlignLeft)
        # self.AwakePatientCheck = QCheckBox()
        # self.AwakePatientLabel = QLabel('Awake Patient')
        # self.AwakePatientLabel.setAlignment(QtCore.Qt.AlignLeft)
        #
        # box3line1 = QHBoxLayout()
        # box3line1.addWidget(self.ReportNeurCheck)
        # box3line1.addWidget(self.ReportNeurLabel)
        # box3line1.addStretch()
        # box3line1.addWidget(self.AwakePatientCheck)
        # box3line1.addWidget(self.AwakePatientLabel)
        # box3line1.addStretch()
        #
        # self.ReportNChCheck = QCheckBox()
        # self.ReportNChLabel = QLabel('Report Neurosurgery\t')
        # self.ReportNChLabel.setAlignment(QtCore.Qt.AlignLeft)
        # self.ProtocolNeurCheck = QCheckBox()
        # self.ProtocolNeurLabel = QLabel('Protocol Neurology')
        # self.ProtocolNeurLabel.setAlignment(QtCore.Qt.AlignLeft)
        #
        # box3line2 = QHBoxLayout()
        # box3line2.addWidget(self.ReportNChCheck)
        # box3line2.addWidget(self.ReportNChLabel)
        # box3line2.addStretch()
        # box3line2.addWidget(self.ProtocolNeurCheck)
        # box3line2.addWidget(self.ProtocolNeurLabel)
        # box3line2.addStretch()
        # # Duration and Trajectories enter field
        # self.DurationSurgery = QLabel('Duration \nsurgery (min):\t')
        # self.lineEditDurationSurgery = QLineEdit()
        # self.Trajectories = QLabel('Trajectories:')
        # self.lineEditTrajectories = QLineEdit()
        #
        # box3line3 = QHBoxLayout()
        # box3line3.addWidget(self.DurationSurgery)
        # box3line3.addWidget(self.lineEditDurationSurgery)
        # box3line3.addWidget(self.Trajectories)
        # box3line3.addWidget(self.lineEditTrajectories)
        # box3line3.addStretch()
        # # List selection neurologist
        # self.testingNeurLabel = QLabel('Testing Neurologist(s):')
        # self.testingNeurList = QListWidget()
        # self.testingNeurList.show()
        # ls = ['Oehrn/Weber', 'Pedrosa', 'Waldthaler', 'Other']
        # [self.testingNeurList.addItem(k) for k in ls]
        #
        # box3line4 = QHBoxLayout()
        # box3line4.addWidget(self.testingNeurLabel)
        # # box3line4.addStretch()
        # box3line4.addWidget(self.testingNeurList)
        # box3line4.addStretch()
        #
        # self.optionbox3Content.addLayout(box3line1)
        # self.optionbox3Content.addLayout(box3line2)
        # self.optionbox3Content.addLayout(box3line3)
        # self.optionbox3Content.addLayout(box3line4)
        #
        # self.optionbox3.setLayout(self.optionbox3Content)

        # ==================== Optionbox(4)-System Information-, upper middle right ====================
        self.optionbox4 = QGroupBox('System Information')
        self.optionbox4Content = QVBoxLayout(self.optionbox4)
        layout_general.addWidget(self.optionbox4, 1, 1)
        # List selection Lead implant
        self.LeadImplantedLabel = QLabel('Lead:\t\t')
        self.LeadImplantedList = QListWidget()
        self.LeadImplantedLabel.setAlignment(QtCore.Qt.AlignTop)
        self.LeadImplantedList.show()
        ls = ['Medtronic 3389', 'Boston Scientific 2202-30/-45',
              'St. Jude 6146/6147/6148/6149', 'Other']
        [self.LeadImplantedList.addItem(k) for k in ls]

        box4line1 = QHBoxLayout()
        box4line1.addWidget(self.LeadImplantedLabel)
        box4line1.addWidget(self.LeadImplantedList)
        # List selection IPG implant
        self.IPGImplantedLabel = QLabel('IPG:\t\t')
        self.IPGImplantedLabel.setAlignment(QtCore.Qt.AlignTop)
        self.IPGImplantedList = QListWidget()
        self.IPGImplantedList.show()
        ls = ['Medtronic Activa PC', 'Medtronic Activa RC', 'Medtronic Activa SC',
              'Boston Scientific Vercise', 'Boston Scientific Vercise PC']
        [self.IPGImplantedList.addItem(k) for k in ls]

        box4line2 = QHBoxLayout()
        box4line2.addWidget(self.IPGImplantedLabel)
        box4line2.addWidget(self.IPGImplantedList)

        self.optionbox4Content.addLayout(box4line1)
        self.optionbox4Content.addLayout(box4line2)
        self.optionbox4.setLayout(self.optionbox4Content)

        # ==================== Optionbox(5)-Coordinates DBS leads-, lower middle left ====================
        self.optionbox5 = QGroupBox('Coordinates DBS leads')
        self.optionbox5Content = QHBoxLayout(self.optionbox5)
        layout_general.addWidget(self.optionbox5, 2, 0)

        self.GridCoordinatesLeft = QGridLayout()
        self.GridCoordinatesLeftLabel = QLabel('\tLeft\t')
        for i in range(0, 8):
            for j in range(0, 4):
                if j == 0:
                    self.GridCoordinatesLeft.addWidget(QLabel(str(i)), i, j)
                else:
                    self.GridCoordinatesLeft.addWidget(QLineEdit(), i, j)

        self.GridCoordinatesRight = QGridLayout()
        self.GridCoordinatesRightLabel = QLabel('\tRight\t')
        for i in range(0, 8):
            for j in range(0, 4):
                if j != 3:
                    hspacer = QSpacerItem(QSizePolicy.Expanding, QSizePolicy.Minimum)  # necessary?!
                    self.GridCoordinatesRight.addItem(hspacer, 0, i, -1, 1)
                    self.GridCoordinatesRight.addWidget(QLineEdit(), i, j)

                else:
                    self.GridCoordinatesRight.addWidget(QLabel(str(i)), i, j)

        self.optionbox5Content.addStretch()
        self.optionbox5Content.addWidget(self.GridCoordinatesLeftLabel)
        self.optionbox5Content.addLayout(self.GridCoordinatesLeft)
        self.optionbox5Content.addStretch()
        self.optionbox5Content.addWidget(self.GridCoordinatesRightLabel)
        self.optionbox5Content.addLayout(self.GridCoordinatesRight)
        #self.optionbox5Content.addLayout(self.GridCoordinatesRight)
        self.optionbox5Content.addStretch()

        # ==================== Optionbox(6)-Activation-, lower middle right ====================
        self.optionbox6 = QGroupBox('Activation')
        self.optionbox6Content = QVBoxLayout(self.optionbox6)
        layout_general.addWidget(self.optionbox6, 2, 1)
        # Postop activation Checkboxes
        self.PostopCTScanCheck = QCheckBox()
        self.PostopCTScanLabel = QLabel('Postoperative CT Scan')
        self.ImplVerciseDBSCheck = QCheckBox()
        self.ImplVerciseDBSCheckLabel = QLabel('Implantation VERCISE DBS')
        self.ActivateVerciseDBSCheck = QCheckBox()
        self.ActivateVerciseDBSLabel = QLabel('Activation VERCISE DBS')
        self.InclusionQualiPaCheck = QCheckBox()
        self.InclusionQualiPaLabel = QLabel('Inclusion QualiPa')

        box6line1 = QHBoxLayout()
        box6line1.addWidget(self.PostopCTScanCheck)
        box6line1.addWidget(self.PostopCTScanLabel)
        box6line1.addStretch(1)

        box6line2 = QHBoxLayout()
        box6line2.addWidget(self.ImplVerciseDBSCheck)
        box6line2.addWidget(self.ImplVerciseDBSCheckLabel)
        box6line2.addStretch(1)

        box6line3 = QHBoxLayout()
        box6line3.addWidget(self.ActivateVerciseDBSCheck)
        box6line3.addWidget(self.ActivateVerciseDBSLabel)
        box6line3.addStretch(1)

        box6line4 = QHBoxLayout()
        box6line4.addWidget(self.InclusionQualiPaCheck)
        box6line4.addWidget(self.InclusionQualiPaLabel)
        box6line4.addStretch(1)

        self.optionbox6Content.addLayout(box6line1)
        self.optionbox6Content.addLayout(box6line2)
        self.optionbox6Content.addLayout(box6line3)
        self.optionbox6Content.addLayout(box6line4)

        # ====================   Adds buttons at the bottom of the GUI      ====================
        self.ButtonEnterMedication = QPushButton('Open GUI \nMedication')
        self.ButtonEnterDBSsettings = QPushButton('Open GUI \nDBS settings')
        self.button_buffer = QPushButton('Save')
        self.button_save = QPushButton('Save and \nReturn')

        hlay_bottom = QHBoxLayout()
        hlay_bottom.addStretch(5)
        hlay_bottom.addWidget(self.ButtonEnterMedication)
        hlay_bottom.addWidget(self.ButtonEnterDBSsettings)
        hlay_bottom.addWidget(self.button_buffer)
        hlay_bottom.addWidget(self.button_save)
        hlay_bottom.addStretch(1)
        layout_general.addLayout(hlay_bottom, 4, 0, 1, 3)

        self.updatetext()

        # ==================== Actions when buttons are pressed     ====================
        # self.ButtonEnterMedication.clicked.connect(self.on_clickedMedication)
        # self.button_save.clicked.connect(self.onClickedSaveReturn)

    # =========================== reloads existing data ===========================#
    def updatetext(self):
        """adds information extracted from database already provided"""

        df_subj = Content.extract_saved_data(self.date)

        if not df_subj["ID"]:
            return

        ###################
        # Admission dates #
        ###################
        self.lineEditAdmission_Nch.setText(str(df_subj["admission_Nch_intraop"][0])) \
            if df_subj["admission_Nch_intraop"][0] != 0 else self.lineEditAdmission_Nch.setText('')
        (self.lineEditAdmission_NR.setText(str(df_subj["Admission_intraop"][0]))) \
            if df_subj["Admission_intraop"][0] != 0 else self.lineEditAdmission_NR.setText('')
        self.lineEditDismission_NR.setText(str(df_subj["Dismissal_intraop"][0])) \
            if df_subj["Dismissal_intraop"][0] != 0 else self.lineEditDismission_NR.setText('')
        self.lineEditDismission_Nch.setText(str(df_subj["dismissal_NCh_intraop"][0])) \
            if df_subj["dismissal_NCh_intraop"][0] != 0 else self.lineEditDismission_Nch.setText('')

        #############################################
        #               Intraoperative              #
        #############################################
        # Duration and Trajectories
        self.lineEditDurationSurgery.setText(str(df_subj["op_duration_intraop"][0])) \
            if str(df_subj["op_duration_intraop"][0]) != 'nan' else self.lineEditDurationSurgery.setText('')
        self.lineEditTrajectories.setText(str(df_subj["no_traj_intraop"][0])) \
            if str(df_subj["no_traj_intraop"][0]) != 'nan' else self.lineEditTrajectories.setText('')

        # Intraoperative Checkboxes
        if df_subj["report_file_NR_intraop"][0] != 0:
            self.ReportNeurCheck.setChecked(True)
        if df_subj["awake_intraop"][0] != 0:
            self.AwakePatientCheck.setChecked(True)
        if df_subj["report_file_NCh_intraop"][0] != 0:
            self.ReportNChCheck.setChecked(True)
        if df_subj["protocol_intraop"][0] != 0:
            self.ProtocolNeurCheck.setChecked(True)

        # LE: Added line for loading selected list items
        setitemactive(df_subj['neur_test_intraop'][0], self.testingNeurList)

        ########################
        # System information #          # LE: Added lines for loading selected list items
        ######################
        # setitemactive(df_subj['Lead_intraop'][0], self.LeadImplantedList)

        # setitemactive(df_subj['IPG_intraop'][0], self.IPGImplantedList)

        ###########
        # surgery #
        ###########
        self.lineEditSurgeryDate.setText(str(df_subj["surgery_date_intraop"][0])) \
            if str(df_subj["surgery_date_intraop"][0]) != 'nan' else self.lineEditSurgeryDate.setText('')
        # LE: Added line for loading selected list items
        setitemactive(df_subj['target_intraop'][0], self.targetList)

        ###############################
        # Activation Checkboxes right #
        ###############################
        if df_subj["CTscan_intraop"][0] != 0:
            self.PostopCTScanCheck.setChecked(True)
        if df_subj["implantation_visit_intraop"][0] != 0:
            self.ImplVerciseDBSCheck.setChecked(True)
        if df_subj["activation_visit_intraop"][0] != 0:
            self.ActivateVerciseDBSCheck.setChecked(True)
        if df_subj["incl_qualiPA_intraop"][0] != 0:
            self.InclusionQualiPaCheck.setChecked(True)

        return

        ##########################
        # DBS Coordinates leads #        # TODO: doesnt work yet
        #########################

    # def load_data(self, data: Intraoperative_data):
    #     # left side
    #     for i in range(1, 9):
    #         DBSleft = self.GridCoordinatesLeft.itemAtPosition(0, i).widget()
    #         column_name = "targetL{}_intraop".format(i)
    #
    #         if column_name in data.d.columns:
    #             value = data.d.loc[data.d.index[0], column_name]
    #             if not pd.isna(value):  # Überprüfen, ob der Wert nicht NaN ist
    #                 DBSleft.setText(str(value))
    #             else:
    #                 DBSleft.clear()
    #         else:
    #             DBSleft.clear()
    #     # right side
    #     for i in range(1, 9):
    #         DBSright = self.GridCoordinatesRight.itemAtPosition(0, i).widget()
    #         column_name = "targetR{}_intraop".format(i)
    #
    #         if column_name in data.d.columns:
    #             value = data.d.loc[data.d.index[0], column_name]
    #             if not pd.isna(value):  # Überprüfen, ob der Wert nicht NaN ist
    #                 DBSright.setText(str(value))
    #             else:
    #                 DBSright.clear()
    #         else:
    #             DBSright.clear()  # Leerfeld, wenn der Wert NaN ist oder leer
    #
    #             #   for i in range(8):

    #      DBSleft = self.GridCoordinatesLeft.itemAtPosition(i, 1).widget()
    #     DBSleft.setText(str(df_subj["targetL{}_intraop".format(i + 1)][0]))

    # DBS Coordinates leads
    # for i in range(8):
    #    DBSright = self.GridCoordinatesRight.itemAtPosition(i, 1).widget()
    #    DBSright.setText(str(df_subj["targetR{}_intraop".format(i + 1)][0]))

    # ==================== Defines actions when buttons are pressed, saves data      ====================

    # changed line damit nicht alle Fenster bei 'return' von MedicationGUI geschlossen werden
    @QtCore.pyqtSlot()
    def on_clickedMedication(self):
        """shows the medication dialog when button is pressed; former implementation with creating GUI was replaced with
        show/hide GUI which is initiated at beginning"""
        self.dialog_medication.show()

    #   @QtCore.pyqtSlot()
    #   def onClickedMedication(self):
    #       """shows the medication dialog when button is pressed"""
    #       dialog = MedicationDialog(visit=self.date, parent=self)
    #       self.hide()
    #       if dialog.exec():
    #          pass
    #     self.show()

    def onClickedSaveReturn(self):
        """closes this GUI and returns to calling (main) GUI"""

        subj_id = General.read_current_subj().id[0]  # reads data from current_subj (saved in ./tmp)
        df_general = Clean.extract_subject_data(subj_id)
        # read general data so that pre-/intra- and postoperative share these
        try:
            subj_id = General.read_current_subj().id[0]  # reads data from current_subj (saved in ./tmp)
            df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=',')
            # if df.shape[1] == 1:
            #     df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=';')
            df_subj = df.iloc[df.index[df['ID'] == subj_id][0], :].to_dict()
        except IndexError:
            df_subj = {k: '' for k in Content.extract_saved_data(self.date).keys()}  # create empty dictionary

        df_general.reset_index(inplace=True, drop=True)

        df_subj['ID'] = General.read_current_subj().id[0]
        df_subj['PID'] = df_general['PID_ORBIS'][0]
        df_subj['Gender'] = df_general['Gender'][0]
        df_subj['Diagnosis_preop'] = df_general['diagnosis'][0]

        self.close()

        # Now extract the changed data from the GUI, save data

        # Admission dates #
        ###################
        df_subj["admission_Nch_intraop"] = self.lineEditAdmission_Nch.text()
        df_subj['Admission_intraop'] = self.lineEditAdm_NR.text()
        df_subj['Dismissal_intraop'] = self.lineEditDismission_NR.text()
        df_subj['dismissal_NCh_intraop'] = self.lineEditDismission_Nch.text()

        #   Intraoperative  #
        ##############################
        # surgery duration
        df_subj['op_duration_intraop'] = self.lineEditDurationSurgery.text()
        df_subj['no_traj_intraop'] = self.lineEditTrajectories.text()
        # report after surgery
        df_subj["report_file_NR_intraop"] = self.ReportNeurCheck.isChecked()
        df_subj["awake_intraop"] = self.AwakePatientCheck.isChecked()
        df_subj["report_file_NCh_intraop"] = self.ReportNChCheck.isChecked()
        df_subj["protocol_intraop"] = self.ProtocolNeurCheck.isChecked()
        # neurologist (LE: added lines to save selected list items)
        selected_neurologist_items = [self.testingNeurList.item(i).text() for i in range(self.testingNeurList.count())
                                      if
                                      self.testingNeurList.item(i).isSelected()]
        df_subj["neur_test_intraop"] = ', '.join(selected_neurologist_items)

        # surgery #
        ###########
        # date of surgery
        df_subj["surgery_date_intraop"] = self.lineEditSurgeryDate.text()
        # target of surgery (added lines to save selected list items)
        selected_target_items = [self.targetList.item(i).text() for i in range(self.targetList.count()) if
                                 self.targetList.item(i).isSelected()]
        df_subj["target_intraop"] = ', '.join(selected_target_items)

        # Activation #
        ##############
        # checkboxes
        df_subj["CTscan_intraop"] = self.PostopCTScanCheck.isChecked()
        df_subj["implantation_visit_intraop"] = self.ImplVerciseDBSCheck.isChecked()
        df_subj["activation_visit_intraop"] = self.ActivateVerciseDBSCheck.isChecked()
        df_subj["incl_qualiPA_intraop"] = self.InclusionQualiPaCheck.isChecked()

        # Sytsem information #
        ######################
        # 'Lead' Auswahl speichern (LE: added lines to save selected list items)
        selected_lead_items = [self.LeadImplantedList.item(i).text() for i in range(self.LeadImplantedList.count()) if
                               self.LeadImplantedList.item(i).isSelected()]
        df_subj["Lead_intraop"] = ', '.join(selected_lead_items)

        # 'IPG' Auswahl speichern (LE: added lines to save selected list items)
        selected_ipg_items = [self.IPGImplantedList.item(i).text() for i in range(self.IPGImplantedList.count()) if
                              self.IPGImplantedList.item(i).isSelected()]
        df_subj["IPG_intraop"] = ', '.join(selected_ipg_items)

        # logger.debug("Lead Selection:", df_subj["Lead_intraop"])
        # logger.debug("IPG Selection:", df_subj["IPG_intraop"])

        # DBS Coordinates #          # TODO: doesnt work yet
        ###################
        left_data = []
        right_data = []

        for i in range(1, 9):
            left_row_data = ['targetL{}_intraop']
            # logger.debug('Coordinates DBS leads', left_row_data=['targetL{}_intraop'])
            right_row_data = ['targetR{}_intraop']
            for j in range(1, 9):
                if j != 4:
                    DBSleft = self.GridCoordinatesLeft.itemAtPosition(i, j).widget()
                    left_row_data.append(DBSleft.text())
                if j >= 3: #8:
                    DBSright = self.GridCoordinatesRight.itemAtPosition(i, j).widget()
                    right_row_data.append(DBSright.text())
                else:
                    print(logging.ERROR)
            left_data.append(left_row_data)
            right_data.append(right_row_data)

        column_names = ['targetL1_intraop', 'targetL2_intraop', 'targetL3_intraop', 'targetL4_intraop',
                        'targetL5_intraop', 'targetL6_intraop', 'targetL7_intraop', 'targetL8_intraop',
                        'targetR1_intraop', 'targetR2_intraop', 'targetR3_intraop', 'targetR4_intraop',
                        'targetR5_intraop', 'targetR6_intraop', 'targetR7_intraop', 'targetR8_intraop']

        for i, col_name in enumerate(column_names):
            df_subj[col_name] = [row[i] for row in left_data] + [row[i] for row in right_data]


        # # DBS Coordinates left
        #  for i in range(8):
        #       for j in range(4):
        #          if j != 0:
        #              df_subj['targetL{}_intraop'.format(i + 1)] = self.GridCoordinatesLeft.itemAtPosition(i,
        #                                                                                                  1).widget().text()

        # DBS Coordinates Right
        # for i in range(8):
        #    for j in range(4):
        #        if j != 3:
        #            DBSright = self.GridCoordinatesRight.itemAtPosition(i, j).widget()
        #            df_subj['targetR{}_intraop'.format(i + 1)] = DBSright.text()

        # == DBS settings after dismissal == #
        ################################
        for j in range(8):
            DBSright = self.DBSpercentageRight.itemAtPosition(0, j + 1).widget()
            df_subj["Perc{}_intraop".format(j + 8)] = DBSright.text()
        for j in range(8):
            DBSleft = self.DBSpercentageLeft.itemAtPosition(0, j + 1).widget()
            df_subj["Perc{}_intraop".format(j)] = DBSleft.text()

        #  == Amplitude, Pulse, Frequency == #
        ######################################
        for i in range(1, 3):
            for j in range(1, 4):
                DBSsettings = self.gridDBSsettings.itemAtPosition(i, j).widget()
                if i == 1 and j == 1:
                    df_subj["AmplL_intraop"] = DBSsettings.text()
                elif i == 1 and j == 2:
                    df_subj["PWL_intraop"] = DBSsettings.text()
                elif i == 1 and j == 3:
                    df_subj["FreqL_intraop"] = DBSsettings.text()
                elif i == 2 and j == 1:
                    df_subj["AmplR_intraop"] = DBSsettings.text()
                elif i == 2 and j == 2:
                    df_subj["PWR_intraop"] = DBSsettings.text()
                elif i == 2 and j == 3:
                    df_subj["FreqR_intraop"] = DBSsettings.text()

        # Incorporate the [df_subj] dataframe into the entire dataset and save as csv
        try:
            idx2replace = df.index[df['ID'] == subj_id][0]
            df.loc[idx2replace, :] = df_subj
            df = df.replace(['nan', ''], [np.nan, np.nan])
        except IndexError:
            df_subj = pds.DataFrame(df_subj, index=[df.index.shape[0]])
            df = pds.concat([df, df_subj], ignore_index=True)
            # df = df.append(df_subj, ignore_index=True)
            df = df.replace('nan', np.nan)

        df.to_csv(Path(f"{FILEDIR}/{self.date}.csv"), index=False)
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = IntraoperativeDialog()
    dlg.show()
    sys.exit(app.exec_())
