#!/usr/bin/env python3
import logging
import sys
from pathlib import Path

import pandas as pds
from PyQt5 import QtCore
import numpy as np
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QGroupBox, QSpacerItem, QSizePolicy, \
    QHBoxLayout, QGridLayout, QLineEdit, QLabel, QListWidget, QCheckBox

from GUImedication import MedicationDialog
from GUI.GUIsettingsDBS import DBSsettingsDialog
from utils.helper_functions import General, Content, Clean
from dependencies import FILEDIR

pds.options.mode.chained_assignment = None  # default='warn' cf.
# https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas

class IntraoperativeDialog(QDialog):
    """Dialog to introduce all important information of intraoperative visit. """

    def __init__(self, parent=None):
        super(IntraoperativeDialog, self).__init__(parent)
        self.dialog_medication, self.dialog_DBSsettings, self.content_widgets = None, None, None  # initialised  Dialogs
        self.date = 'intraoperative'  # defines the date at which data are taken from/saved at
        self.setup_ui()

    def setup_ui(self):
        self.initialize_content()
        self.setup_general_layout()

    def setup_general_layout(self):
        """Defines the general layout for the GUI"""
        subj_details = General.read_current_subj()  # reads information for the subject last being processed
        General.synchronize_data_with_general(self.date, subj_details.id[0],
                                              messagebox=False)  # for identical general columns in 'preoperative.csv'

        self.create_medication_dialog()
        self.create_DBSsettings_dialog()

        self.setWindowTitle(f'Please insert the intraoperative patient data (PID: {int(subj_details.pid.iloc[0])})')
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

        # Obtain data that has been stored already in intraoperative.csv
        self.updateIntraoperativeData()

    def initialize_content(self):
        """Initializes the content that may be needed later for reading or saving data from/to csv-files"""

        self.content_widgets = {
            'Admission_intraop': 'lineEditAdmission_Nch',
            'Dismissal_intraop': 'lineEditDismission_Nch',
            'admission_Nch_intraop': 'lineEditAdmission_NR',
            'dismissal_NCh_intraop': 'lineEditDismission_NR',
            'surgery_date_intraop': 'lineEditSurgeryDate',
            'no_traj_intraop': 'lineEditTrajectories',
            'op_duration_intraop': 'lineEditDurationSurgery'
        }

    def create_medication_dialog(self):
        self.dialog_medication = MedicationDialog(parent=self, visit=self.date)  # creates medication dialog
        self.dialog_medication.hide()

    def create_DBSsettings_dialog(self):
        self.dialog_DBSsettings = DBSsettingsDialog(parent=self, visit=self.date, reason="Initial intraoperative settings")  # creates medication dialog
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

        # Add toggle button
        self.toggle_button = QPushButton('Change dates')
        self.toggle_button.setFixedSize(150, 50)
        self.toggle_button.clicked.connect(self.toggle_line_edit)
        self.optionbox_datesContent.addWidget(self.toggle_button)

    def toggle_line_edit(self):
        line_edits = [
            self.lineEditAdmission_Nch,
            self.lineEditAdmission_NR,
            self.lineEditDismission_Nch,
            self.lineEditDismission_NR,
            self.lineEditSurgeryDate
        ]

        for line_edit in line_edits:
            line_edit.setEnabled(not line_edit.isEnabled())

    def optionbox_general_intraoperative(self, layout_general):
        """creates upper right optionbox: General data for the intraoperative recordings"""

        self.optionbox_general = QGroupBox('General data')
        self.optionbox_generalContent = QVBoxLayout(self.optionbox_general)
        layout_general.addWidget(self.optionbox_general, 0, 1)

        # Target List
        targetLabel = QLabel('Target:\t\t')
        targetLabel.setAlignment(QtCore.Qt.AlignTop)
        self.targetList = QListWidget()
        self.targetList.show()
        ls = ['STN', 'GPi', 'VLp', 'Other'] #GP: should the user to be able to input custom 'other'?
        for k in ls:
            self.targetList.addItem(k)

        textbox_line1 = QHBoxLayout()
        textbox_line1.addWidget(targetLabel)
        textbox_line1.addWidget(self.targetList)

        self.optionbox_generalContent.addLayout(textbox_line1)
        self.optionbox_general.setLayout(self.optionbox_generalContent)

    def optionbox_intraoperative_data(self, layout_general):
        """creates lower left optionbox for Intraoperative data"""
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
        self.ReportNChLabel = QLabel('Report Neurosurgery')
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
        self.DurationSurgery = QLabel('Duration surgery (min):\t')
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
        #box3line4.addStretch()
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
        self.button_save = QPushButton('Save')
        self.button_save_return = QPushButton('Save and \nReturn')

        # Set fixed size for all buttons
        button_width = 200
        button_height = 75

        self.ButtonEnterMedication.setFixedSize(button_width, button_height)
        self.ButtonEnterDBSsettings.setFixedSize(button_width, button_height)
        self.button_save.setFixedSize(button_width, button_height)
        self.button_save_return.setFixedSize(button_width, button_height)

        hlay_bottom = QHBoxLayout()
        hlay_bottom.addStretch(5)
        hlay_bottom.addWidget(self.ButtonEnterMedication)
        hlay_bottom.addWidget(self.ButtonEnterDBSsettings)
        hlay_bottom.addWidget(self.button_save)
        hlay_bottom.addWidget(self.button_save_return)
        hlay_bottom.addStretch(1)
        layout_general.addLayout(hlay_bottom, 4, 0, 1, 3)

    def connect_button_actions(self):
        """Defines the actions that are taken once a button is pressed or specific input is made"""

        self.ButtonEnterMedication.clicked.connect(self.onClickedMedication)
        self.ButtonEnterDBSsettings.clicked.connect(self.onClickedDBSsettings)
        self.button_save.clicked.connect(self.onClickedSave)
        self.button_save_return.clicked.connect(self.onClickedSaveReturn)

    # ====================   Defines actions when buttons are pressed      ====================
    @QtCore.pyqtSlot()
    def onClickedMedication(self):
        """Shows medication dialog ; former implementation with creating GUI was replaced with show/hide GUI which is
        initiated at beginning at the disadvantage of not being saved until GUIintraoperative is closed"""
        self.dialog_medication.show()

    def onClickedDBSsettings(self):
        """shows the DBSsettings dialog when button is pressed"""
        self.dialog_DBSsettings.show()

    @QtCore.pyqtSlot()
    def onClickedSave(self):
        self.save_data2csv()

    def onClickedSaveReturn(self):
        """closes GUI and returns to calling (main) GUI"""
        self.save_data2csv()
        self.close()

    # =========================== reloads existing data ===========================#
    def updateIntraoperativeData(self):
        """adds information extracted from database already provided"""

        df_subj = Content.extract_saved_data(self.date)
        if not df_subj["ID"]:
            print("No ID for current_subject in preoperative.csv found")
            return

        # LineEdits
        for column, widget in self.content_widgets.items():
            widget_object = getattr(self, widget)
            widget_object.setText(str(df_subj[column][0])) if str(
                df_subj[column][0]) != 'nan' else widget_object.setText('')

        # Intraoperative Checkboxes
        checkboxes = {"report_file_NR_intraop": 'ProtocolNeurCheck',
                      "awake_intraop": 'AwakePatientCheck',
                      "report_file_NCh_intraop": 'ReportNChCheck',
                      "protocol_intraop": 'ProtocolNeurCheck'}

        for df_name, checkbox_name in checkboxes.items():
            if str(df_subj[df_name][0]) == '1':
                getattr(self, checkbox_name).setCheckState(QtCore.Qt.Checked)
            else:
                getattr(self, checkbox_name).setCheckState(QtCore.Qt.Unchecked)

        # Set selected items for target_intraop
        if isinstance(df_subj["target_intraop"][0], str): #GP: if cell is 'nan', its still considered a float, float.split() Error
            target_choices = df_subj["target_intraop"][0].split(', ')
            for i in range(self.targetList.count()):
                item = self.targetList.item(i)
                if item.text() in target_choices:
                    item.setSelected(True)
                else:
                    item.setSelected(False)

        else:
            for i in range(self.targetList.count()):
                item = self.targetList.item(i)
                item.setSelected(False)

        # Set selected items for neur_test_intraop
        if isinstance(df_subj["neur_test_intraop"][0], str):
            neurologist_choices = df_subj["neur_test_intraop"][0].split(', ')
            for i in range(self.testingNeurList.count()):
                item = self.testingNeurList.item(i)
                if item.text() in neurologist_choices:
                    item.setSelected(True)
                else:
                    item.setSelected(False)
        else:
            for i in range(self.testingNeurList.count()):
                item = self.testingNeurList.item(i)
                item.setSelected(False)
        return

    # ====================   Defines actions when buttons are pressed      ====================
    @QtCore.pyqtSlot()
    def on_clickedMedication(self):
        """shows the medication dialog when button is pressed; former implementation with creating GUI was replaced with
        show/hide GUI which is initiated at beginning"""
        self.dialog_medication.show()

    @QtCore.pyqtSlot()
    def onClickedSave(self):
        self.save_data2csv()

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
        try:
            df_subj['ID'] = General.read_current_subj().id[0]
            df_subj['PID_ORBIS'] = df_general['PID_ORBIS'][
                0]  # is this necessary? -> Error if subj has no data in general_data
            df_subj['Gender'] = df_general['gender'][0]
            df_subj['Diagnosis_preop'] = df_general['diagnosis'][0]
        except KeyError:
            print("No Data in general_data for this ID found")

        # Now extract changed data from the GUI
        for column, widget in self.content_widgets.items():
            if 'lineEdit' in widget:
                widget_object = getattr(self, widget)
                print(widget_object.text())
                if widget == 'lineEditTrajectories' or widget == 'lineEditDurationSurgery':
                    widget_object = getattr(self, widget)
                    df_subj[column] = widget_object.text()
                    pass
                else:
                    date = General.validate_and_format_dates(widget_object.text())
                    df_subj[column] = date
            else:
                widget_object = getattr(self, widget)
                df_subj[column] = widget_object.text()

        checkboxes = {"report_file_NR_intraop": 'ProtocolNeurCheck',
                      "awake_intraop": 'AwakePatientCheck',
                      "report_file_NCh_intraop" : 'ReportNChCheck',
                      "protocol_intraop": 'ProtocolNeurCheck'}


        for df_name, checkbox_name in checkboxes.items():
            df_subj[df_name] = 1 if getattr(self, checkbox_name).isChecked() else 0

        # Extract selected items from QListWidgets
        selected_neurologist_items = [self.testingNeurList.item(i).text() for i in
                                      range(self.testingNeurList.count()) if
                                      self.testingNeurList.item(i).isSelected()]
        df_subj["neur_test_intraop"] = ', '.join(selected_neurologist_items)

        selected_target_items = [self.targetList.item(i).text() for i in range(self.targetList.count()) if
                                 self.targetList.item(i).isSelected()]
        df_subj["target_intraop"] = ', '.join(selected_target_items)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = IntraoperativeDialog()
    dlg.show()
    sys.exit(app.exec_())
