#!/usr/bin/env python3
import os, sys, re
import numpy as np
import pandas as pds
from PyQt5 import QtCore
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QWidget, QGridLayout, QLineEdit, QLabel, QCheckBox
from GUI.GUImedication import MedicationDialog
from utils.helper_functions import General, Content, Clean
from dependencies import FILEDIR

pds.options.mode.chained_assignment = None  # default='warn' cf.
# https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas
# TODO's: needs fix: go on 'save and return' after entering data before entering medicationGUI,
#  or else on 'return' all windows close and data will be deleted


class PreoperativeDialog(QDialog):
    """Dialog to introduce all important information of preoperative data ('Indikationsprüfung')"""

    def __init__(self, parent=None, textwidth=300):
        """Initializer."""
        super(PreoperativeDialog, self).__init__(parent)
        self.dialog_medication = None
        self.date = 'preoperative'  # defines the date at which data are taken from/saved at
        self.setup_ui()

    def setup_ui(self):
        self.initialize_content()
        self.setup_general_layout()

    def setup_general_layout(self):
        """Defines the general layout for the GUI"""
        subj_details = General.read_current_subj()  # reads information for the subject last bein processed
        General.synchronize_data_with_general(self.date, subj_details.id[0],
                                              messagebox=False)  # for identical general columns in 'preoperative.csv'

        self.create_medication_dialog()

        self.setWindowTitle('Postoperative Information (PID: {})'.format(str(int(subj_details.pid))))  # not necessary
        self.setGeometry(200, 100, 280, 170)
        self.move(400, 200)

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # Option boxes appearing in the preoperative GUI
        # Create optionbox for important dates
        self.optionbox_dates_preoperative(layout_general)

        # Create optionbox for reports and study participation
        self.optionbox_reports_preoperative(layout_general)

        # Create optionbox for scales and questionnaires during or visit
        self.optionbox_questionnaires_preoperative(layout_general)

        # Create optionbox for tests performed during preoperative visits
        self.optionbox_preoperative_other(layout_general)

        # Create buttons at the bottom of the GUI
        self.create_bottom_buttons_preoperative(layout_general)

        # Connect button actions that are needed so that everything works
        self.connect_button_actions()

        # Obtain data that has been stored already for the preoperatively
        self.updatePreoperativeData()

    def initialize_content(self):
        """Initializes the contant that may be needed later for reading or saving data from/to csv-files"""

        self.column_widgets = {
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

    def optionbox_dates_preoperative(self, layout_general):
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

        self.optionbox_dates_preoperative = QGroupBox('Diagnosis and indication check')
        self.optionbox_dates_preoperative_Content = QVBoxLayout(self.optionbox_dates_preoperative)
        layout_general.addWidget(self.optionbox_dates_preoperative, 0, 0)

        FirstDiagnosed, self.lineEditFirstDiagnosed = create_line_edit_for_dates('First diagnosed')
        AdmNeurIndCheck, self.lineEditAdmNeurIndCheck = create_line_edit_for_dates('Admission Neurology')
        DismNeurIndCheck, self.lineEditDismNeurIndCheck = create_line_edit_for_dates('Dismission Neurology')
        OutpatientContact, self.lineEditOutpatientContact = create_line_edit_for_dates('Outpatient contact')
        NsurgContact, self.lineEditNsurgContact = create_line_edit_for_dates('Neurosurgical contact')
        DBSconference, self.lineEditDBSconference = create_line_edit_for_dates('DBS conference')

        # Create lines of layout
        textbox_line1_1 = create_horizontal_layout_dates(FirstDiagnosed, self.lineEditFirstDiagnosed)
        textbox_line2_1 = create_horizontal_layout_dates(AdmNeurIndCheck, self.lineEditAdmNeurIndCheck)
        textbox_line3_1 = create_horizontal_layout_dates(DismNeurIndCheck, self.lineEditDismNeurIndCheck)
        textbox_line1_2 = create_horizontal_layout_dates(OutpatientContact, self.lineEditOutpatientContact)
        textbox_line2_2 = create_horizontal_layout_dates(NsurgContact, self.lineEditNsurgContact)
        textbox_line3_2 = create_horizontal_layout_dates(DBSconference, self.lineEditDBSconference)

        # Add layouts to option box content
        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(textbox_line1_1)
        horizontal_layout.addLayout(textbox_line1_2)
        self.optionbox_dates_preoperative_Content.addLayout(horizontal_layout)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(textbox_line2_1)
        horizontal_layout.addLayout(textbox_line2_2)
        self.optionbox_dates_preoperative_Content.addLayout(horizontal_layout)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addLayout(textbox_line3_1)
        horizontal_layout.addLayout(textbox_line3_2)
        self.optionbox_dates_preoperative_Content.addLayout(horizontal_layout)

        self.optionbox_dates_preoperative.setLayout(self.optionbox_dates_preoperative_Content)

    def optionbox_reports_preoperative(self, layout_general):

        self.optionbox_reports_preoperative = QGroupBox('Reports and study participation:')
        self.optionbox_reportsContent = QVBoxLayout(self.optionbox_reports_preoperative)
        layout_general.addWidget(self.optionbox_reports_preoperative, 1, 0)

        def create_checkbox(label_text):
            checkbox = QCheckBox()
            checkbox_label = QLabel(label_text)
            checkbox_label.setAlignment(QtCore.Qt.AlignLeft)
            return checkbox, checkbox_label

        checkboxes_info = [
            ('Report_preop', 'Report'),
            ('Decision_DBS_preop', 'Decision for lead placement'),
            ('icVRCS_preop', 'Consent VERCISE DBS'),
            ('inexVRCS_preop', 'In-/Exclusion criteria VERCISE-DBS'),
        ]

        textbox = QHBoxLayout()
        for checkbox_name, label_text in checkboxes_info:
            checkbox, checkbox_label = create_checkbox(label_text)
            setattr(self, checkbox_name, checkbox)
            setattr(self, f'{checkbox_name}_Label', checkbox_label)
            textbox.addWidget(checkbox)
            textbox.addWidget(checkbox_label)

        textbox.addStretch()
        self.optionbox_reportsContent.addLayout(textbox)
        self.optionbox_reports_preoperative.setLayout(self.optionbox_reportsContent)

    def optionbox_questionnaires_preoperative(self, layout_general):

        self.optionbox_questionnaires = QGroupBox('Scales and questionnaires:')
        self.optionbox_questionnairesContent = QHBoxLayout(self.optionbox_questionnaires)
        layout_general.addWidget(self.optionbox_questionnaires, 2, 0)

        self.updrsON = QLineEdit()
        self.updrsII = QLineEdit()
        self.hruq = QLineEdit()
        self.moca = QLineEdit()
        self.mmst = QLineEdit()
        self.bdi2 = QLineEdit()
        self.nmsq = QLineEdit()
        self.updrsOFF = QLineEdit()
        self.hy = QLineEdit()
        self.eq5d = QLineEdit()
        self.demtect = QLineEdit()
        self.pdq8 = QLineEdit()
        self.pdq39 = QLineEdit()
        self.se = QLineEdit()

        content = [{'UPDRS III ON': self.updrsON,
                    'UPDRS II': self.updrsII,
                    'HRUQ': self.hruq,
                    'MoCa': self.moca,
                    'MMST': self.mmst,
                    'BDI-II': self.bdi2,
                    'NMSQ': self.nmsq},
                   {'UPDRS III OFF': self.updrsOFF,
                    'H&Y': self.hy,
                    'EQ5D': self.eq5d,
                    'DemTect': self.demtect,
                    'PDQ8': self.pdq8,
                    'PDQ39': self.pdq39,
                    'S&E': self.se}]

        self.GridCoordinatesLeft = QGridLayout()
        for i in range(0, 2):  # rows
            idx_cols = 0
            for k, v in content[i].items():  # columns
                self.GridCoordinatesLeft.addWidget(QLabel(k), i, idx_cols)
                idx_cols += 1
                self.GridCoordinatesLeft.addWidget(v, i, idx_cols)
                idx_cols += 1

        self.optionbox_questionnairesContent.addStretch()
        self.optionbox_questionnairesContent.addLayout(self.GridCoordinatesLeft)
        self.optionbox_questionnairesContent.addStretch()

    def optionbox_preoperative_other(self, layout_general):
        self.optionbox_other = QGroupBox('Other:')
        self.optionbox_otherContent = QVBoxLayout(self.optionbox_other)
        layout_general.addWidget(self.optionbox_other, 3, 0)

        def create_checkbox(label_text):
            checkbox = QCheckBox()
            checkbox_label = QLabel(label_text)
            checkbox_label.setAlignment(QtCore.Qt.AlignLeft)
            return checkbox, checkbox_label

        checkboxes_info = [
            ('Video_preop', 'Video'),
            ('MRI_preop', 'MRI'),
            ('fpcit_spect_preop', 'FP-CIT SPECT'),
        ]

        box4line1 = QHBoxLayout()
        for checkbox_name, label_text in checkboxes_info:
            checkbox, checkbox_label = create_checkbox(label_text)
            setattr(self, checkbox_name, checkbox)
            setattr(self, f'{checkbox_name}_Label', checkbox_label)
            box4line1.addWidget(checkbox)
            box4line1.addWidget(checkbox_label)

        box4line1.addStretch(1)
        self.optionbox_otherContent.addLayout(box4line1)
        self.optionbox_other.setLayout(self.optionbox_otherContent)

    def create_bottom_buttons_preoperative(self, layout_general):
        """Creates two buttons a) to read medication and b) to save settings and exit GUI """
        # Use more descriptive names for the buttons
        self.button_medication = QPushButton('Open GUI \nMedication')
        self.button_save = QPushButton('Save')
        self.button_save_return = QPushButton('Save and \nReturn')

        # Set fixed size for all buttons
        button_width = 200
        button_height = 75

        # Apply fixed size using a loop for cleaner code
        for button in [self.button_medication, self.button_save, self.button_save_return]:
            button.setFixedSize(button_width, button_height)

        # Use QVBoxLayout for better vertical alignment
        vlay_bottom = QHBoxLayout()

        # Add buttons to the layout
        vlay_bottom.addWidget(self.button_medication)
        vlay_bottom.addWidget(self.button_save)
        vlay_bottom.addWidget(self.button_save_return)

        # Add stretch to push buttons to the sides
        vlay_bottom.addStretch()

        # Create a horizontal layout for overall alignment
        hlay_bottom = QHBoxLayout()
        hlay_bottom.addStretch(5)
        hlay_bottom.addLayout(vlay_bottom)
        hlay_bottom.addStretch(1)

        # Add the horizontal layout to the general layout
        layout_general.addLayout(hlay_bottom, 4, 0, 1, 3)

        # self.read_content_csv()

    def updatePreoperativeData(self):
        """Displays all the information that has been stored already in the csv files"""

        df_subj = Content.extract_saved_data(self.date)
        if not df_subj["ID"]:  # this is only for when no information could be found
            return

        for column, widget in self.column_widgets.items():
            widget_object = getattr(self, widget)
            widget_object.setText(str(df_subj[column][0])) if str(
                df_subj[column][0]) != 'nan' else widget_object.setText('')

        # Edit Upper CheckBoxes with content using a ternary operator

        checkboxes = ["Video_preop", "MRI_preop", "fpcit_spect_preop", "Report_preop",
                      "Decision_DBS_preop", "icVRCS_preop", "inexVRCS_preop"]

        for checkbox in checkboxes:
            if str(df_subj[checkbox][0]) == '1':
                getattr(self, checkbox).setCheckState(QtCore.Qt.Checked)
            else:
                getattr(self, checkbox).setCheckState(QtCore.Qt.Unchecked)
        # or QtCore.Qt.Checked

        return

    def connect_button_actions(self):
        """Defines the actions that are taken once a button is pressed or specific input is made"""
        # self.lineEditreason.currentIndexChanged.connect(self.update_context)
        # self.lineEditsubjIPG.currentIndexChanged.connect(self.update_IPG)
        self.button_medication.clicked.connect(self.onClickedMedication)
        self.button_save.clicked.connect(self.onClickedSave)
        self.button_save_return.clicked.connect(self.onClickedSaveReturn)

    # ====================   Defines actions when buttons are pressed      ====================
    @QtCore.pyqtSlot()
    def onClickedMedication(self):
        """Shows medication dialog ; former implementation with creating GUI was replaced with show/hide GUI which is
        initiated at beginning at the disadvantage of not being saved until GUIpreoperative is closed"""
        self.dialog_medication.show()

    @QtCore.pyqtSlot()
    def onClickedSave(self):
        self.save_data2csv()

    def onClickedSaveReturn(self):
        """closes GUI and returns to calling (main) GUI"""
        self.save_data2csv()
        self.close()

    def save_data2csv(self):

        subject_id = General.read_current_subj().id[0]  # reads data from current_subj (saved in ./tmp)
        df_general = Clean.extract_subject_data(subject_id)

        # First of all, read general data so that pre-/intra- and postoperative share these
        try:
            df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=',')
            df_subj = df.iloc[df.index[df['ID'] == subject_id][0], :].to_dict()
        except IndexError:
            df_subj = {k: '' for k in Content.extract_saved_data(self.date).keys()}  # create empty dictionary

        # Start filling the dataframe [df_subj] with data from the entries in the GUI
        df_general.reset_index(inplace=True, drop=True)

        # Compare with general_data.csv
        df_subj['ID'] = General.read_current_subj().id[0]
        df_subj['PID_ORBIS'] = df_general['PID_ORBIS'][0] # is this necessary?
        df_subj['Gender'] = df_general['Gender'][0]
        df_subj['Diagnosis_preop'] = df_general['diagnosis'][0]

        # Now extract changed data from the GUI

        for column, widget in self.column_widgets:
            widget_object = getattr(self, widget)
            df_subj[column] = widget_object.text()
        checkboxes = ["Video_preop", "MRI_preop", "fpcit_spect_preop", "Report_preop",
                      "Decision_DBS_preop", "icVRCS_preop", "inexVRCS_preop"]

        for checkbox in checkboxes:
            df_subj[checkbox] = 1 if getattr(self, checkbox).isChecked() else 0

        # Incorporate the [df_subj] dataframe into the entire dataset and save as csv
        try:
            idx2replace = df.index[df['ID'] == subject_id][0]
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
    dlg = PreoperativeDialog()
    dlg.show()
    sys.exit(app.exec_())
