#!/usr/bin/env python3
import os, sys
import pandas as pds
import numpy as np
from PyQt5 import QtCore
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QWidget, QGridLayout, QLineEdit, QLabel, QCheckBox
from GUI.GUImedication import MedicationDialog
from utils.helper_functions import General, Content, Clean
from dependencies import FILEDIR

pds.options.mode.chained_assignment = None  # default='warn' cf.
# https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas


class PreoperativeDialog(QDialog):
    """Dialog to introduce all important information of preoperative data ('indication check')"""

    def __init__(self, parent=None, textwidth=300):
        """Initializer."""
        super(PreoperativeDialog, self).__init__(parent)

        subj_details = General.read_current_subj()
        self.date = 'preoperative'  # defines the date at which data are taken from/saved at

        General.synchronize_data_with_general(self.date, subj_details.id[0],
                                              messagebox=False)  # ensures identical first columns in preoperative.csv
        self.dialog_medication = MedicationDialog(parent=self, visit=self.date)  # creates medication dialog (preop)
        self.dialog_medication.hide()

        # ====================    Create General Layout      ====================
        self.setWindowTitle('Please enter preoperative data (PID: {})'.format(str(int(subj_details.pid))))
        self.setGeometry(200, 100, 280, 170)
        self.move(400, 100)

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # ====================    Optionbox (1) middle, highest      ====================
        self.optionbox1 = QGroupBox('Diagnosis and indication check')
        self.optionbox1Content = QVBoxLayout(self.optionbox1)
        layout_general.addWidget(self.optionbox1, 0, 0)

        self.FirstDiagnosed = QLabel('First diagnosed:\t\t')
        self.lineEditFirstDiagnosed = QLineEdit()
        self.lineEditFirstDiagnosed.setFixedWidth(textwidth)
        self.AdmNeurIndCheckLabel = QLabel('Admission (yyyy-mm-dd):\t')
        self.lineEditAdmNeurIndCheck = QLineEdit()
        self.lineEditAdmNeurIndCheck.setFixedWidth(textwidth)
        self.DismNeurIndCheck = QLabel('Dismission (yyyy-mm-dd):\t')
        self.DismNeurIndCheckLabel = QLineEdit()
        self.DismNeurIndCheckLabel.setFixedWidth(textwidth)
        self.OutpatientContact = QLabel('Outpatient contact (yyyy-mm-dd):\t\t')
        self.lineEditOutpatientContact = QLineEdit()
        self.lineEditOutpatientContact.setFixedWidth(textwidth)
        self.NChContact = QLabel('Neurosurgical contact (yyyy-mm-dd):\t')
        self.lineEditNChContact = QLineEdit()
        self.lineEditNChContact.setFixedWidth(textwidth)
        self.DBSconferenceDate = QLabel('DBS conference (yyyy-mm-dd):\t\t')
        self.lineEditDBSconferenceDate = QLineEdit()
        self.lineEditDBSconferenceDate.setFixedWidth(textwidth)

        box1line1 = QHBoxLayout()
        box1line1.addWidget(self.FirstDiagnosed)
        box1line1.addWidget(self.lineEditFirstDiagnosed)
        box1line1.addStretch()
        box1line1.addWidget(self.OutpatientContact)
        box1line1.addWidget(self.lineEditOutpatientContact)
        box1line1.addStretch()

        box1line2 = QHBoxLayout()
        box1line2.addWidget(self.AdmNeurIndCheckLabel)
        box1line2.addWidget(self.lineEditAdmNeurIndCheck)
        box1line2.addStretch()
        box1line2.addWidget(self.NChContact)
        box1line2.addWidget(self.lineEditNChContact)
        box1line2.addStretch()

        box1line3 = QHBoxLayout()
        box1line3.addWidget(self.DismNeurIndCheck)
        box1line3.addWidget(self.DismNeurIndCheckLabel)
        box1line3.addStretch()
        box1line3.addWidget(self.DBSconferenceDate)
        box1line3.addWidget(self.lineEditDBSconferenceDate)
        box1line3.addStretch()

        self.optionbox1Content.addLayout(box1line1)
        self.optionbox1Content.addLayout(box1line2)
        self.optionbox1Content.addLayout(box1line3)
        self.optionbox1.setLayout(self.optionbox1Content)

        # ====================    Optionbox (2) middle, high       ====================
        self.optionbox2 = QGroupBox('Reports and study participation:')
        self.optionbox2Content = QVBoxLayout(self.optionbox2)
        layout_general.addWidget(self.optionbox2, 1, 0)

        self.Report_preop = QCheckBox()
        self.Report_preop_Label = QLabel('Report\t\t')
        self.Report_preop_Label.setAlignment(QtCore.Qt.AlignLeft)
        self.Decision_DBS_preop = QCheckBox()
        self.Decision_DBS_preop_Label = QLabel('Decision for lead placement\t\t')
        self.Decision_DBS_preop_Label.setAlignment(QtCore.Qt.AlignLeft)
        self.icVRCS_preop = QCheckBox()
        self.icVRCS_preop_Label = QLabel('Consent VERCISE DBS\t\t')
        self.icVRCS_preop_Label.setAlignment(QtCore.Qt.AlignLeft)
        self.inexVRCS_preop = QCheckBox()
        self.inexVRCS_preop_Label = QLabel('In-/Exclusion criteria VERCISE-DBS\t\t')
        self.inexVRCS_preop_Label.setAlignment(QtCore.Qt.AlignLeft)

        box2line1 = QHBoxLayout()
        box2line1.addWidget(self.Report_preop)
        box2line1.addWidget(self.Report_preop_Label)
        box2line1.addWidget(self.Decision_DBS_preop)
        box2line1.addWidget(self.Decision_DBS_preop_Label)
        box2line1.addWidget(self.icVRCS_preop)
        box2line1.addWidget(self.icVRCS_preop_Label)
        box2line1.addWidget(self.inexVRCS_preop)
        box2line1.addWidget(self.inexVRCS_preop_Label)
        box2line1.addStretch()

        self.optionbox2Content.addLayout(box2line1)
        self.optionbox2.setLayout(self.optionbox2Content)

        # ====================    Optionbox (3), middle lower       ====================
        self.optionbox3 = QGroupBox('Scales and questionnaires:')
        self.optionbox3Content = QHBoxLayout(self.optionbox3)
        layout_general.addWidget(self.optionbox3, 2, 0)

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
        self.optionbox3Content.addStretch()
        self.optionbox3Content.addLayout(self.GridCoordinatesLeft)
        self.optionbox3Content.addStretch()

        # ====================    Optionbox (4) middle, lowest       ====================
        self.optionbox4 = QGroupBox('Other:')
        self.optionbox4Content = QVBoxLayout(self.optionbox4)
        layout_general.addWidget(self.optionbox4, 3, 0)

        self.Video_File_preop = QCheckBox()
        self.Video_File_preop_Label = QLabel('Video')
        self.Video_File_preop_Label.setAlignment(QtCore.Qt.AlignLeft)
        self.MRI_preop = QCheckBox()
        self.MRI_preop_Label = QLabel('MRI')
        self.MRI_preop_Label.setAlignment(QtCore.Qt.AlignLeft)
        self.fpcit_spect_preop = QCheckBox()
        self.fpcit_spect_preop_Label = QLabel('FP-CIT SPECT')
        self.fpcit_spect_preop_Label.setAlignment(QtCore.Qt.AlignLeft)

        box4line1 = QHBoxLayout()
        box4line1.addWidget(self.Video_File_preop)
        box4line1.addWidget(self.Video_File_preop_Label)
        box4line1.addWidget(self.MRI_preop)
        box4line1.addWidget(self.MRI_preop_Label)
        box4line1.addWidget(self.fpcit_spect_preop)
        box4line1.addWidget(self.fpcit_spect_preop_Label)
        box4line1.addStretch(1)

        self.optionbox4Content.addLayout(box4line1)
        self.optionbox4.setLayout(self.optionbox4Content)

        # ====================   Adds buttons at the bottom of the GUI      ====================
        self.ButtonEnterMedication = QPushButton('Open GUI \nMedication')
        self.button_save = QPushButton('Save and \nReturn')

        hlay_bottom = QHBoxLayout()
        hlay_bottom.addStretch(5)
        hlay_bottom.addWidget(self.ButtonEnterMedication)
        hlay_bottom.addWidget(self.button_save)
        hlay_bottom.addStretch(1)
        layout_general.addLayout(hlay_bottom, 4, 0, 1, 3)

        self.updatePreoperativeData()

        # ====================   Actions when buttons are pressed      ====================
        self.ButtonEnterMedication.clicked.connect(self.onClickedMedication)
        self.button_save.clicked.connect(self.onClickedSaveReturn)

    def updatePreoperativeData(self):
        """Displays all the information that has been stored already in the csv files"""

        df_subj = Content.extract_saved_data(self.date)
        if not df_subj["ID"]:  # this is only for when no information could be found
            return

        self.lineEditFirstDiagnosed.setText(str(df_subj["First_Diagnosed_preop"][0])) \
            if str(df_subj["First_Diagnosed_preop"][0]) != 'nan' else self.lineEditFirstDiagnosed.setText('')
        self.lineEditAdmNeurIndCheck.setText(str(df_subj['Admission_preop'][0])) \
            if str(df_subj["Admission_preop"][0]) != 'nan' else self.lineEditAdmNeurIndCheck.setText('')
        self.DismNeurIndCheckLabel.setText(str(df_subj['Dismissal_preop'][0])) \
            if str(df_subj["Dismissal_preop"][0]) != 'nan' else self.DismNeurIndCheckLabel.setText('')
        self.lineEditOutpatientContact.setText(str(df_subj['Outpat_Contact_preop'][0])) \
            if str(df_subj["Outpat_Contact_preop"][0]) != 'nan' else self.lineEditOutpatientContact.setText('')
        self.lineEditNChContact.setText(str(df_subj['nch_preop'][0])) \
            if str(df_subj["nch_preop"][0]) != 'nan' else self.lineEditNChContact.setText('')
        self.lineEditDBSconferenceDate.setText(str(df_subj['DBS_Conference_preop'][0])) \
            if str(df_subj["DBS_Conference_preop"][0]) != 'nan' else self.lineEditDBSconferenceDate.setText('')

        self.hy.setText(str(df_subj["H&Y_preop"][0])) \
            if str(df_subj["H&Y_preop"][0]) != 'nan' else self.hy.setText('')
        self.updrsON.setText(str(df_subj["UPDRS_On_preop"][0])) \
            if str(df_subj["UPDRS_On_preop"][0]) != 'nan' else self.updrsON.setText('')
        self.updrsOFF.setText(str(df_subj["UPDRS_Off_preop"][0])) \
            if str(df_subj["UPDRS_Off_preop"][0]) != 'nan' else self.updrsOFF.setText('')
        self.updrsII.setText(str(df_subj["UPDRSII_preop"][0])) \
            if str(df_subj["UPDRSII_preop"][0]) != 'nan' else self.updrsII.setText('')
        self.hruq.setText(str(df_subj["HRUQ_preop"][0])) \
            if str(df_subj["HRUQ_preop"][0]) != 'nan' else self.hruq.setText('')
        self.moca.setText(str(df_subj["MoCa_preop"][0])) \
            if str(df_subj["MoCa_preop"][0]) != 'nan' else self.moca.setText('')
        self.mmst.setText(str(df_subj["MMST_preop"][0])) \
            if str(df_subj["MMST_preop"][0]) != 'nan' else self.mmst.setText('')
        self.bdi2.setText(str(df_subj["BDI2_preop"][0])) \
            if str(df_subj["BDI2_preop"][0]) != 'nan' else self.bdi2.setText('')
        self.nmsq.setText(str(df_subj["NMSQ_preop"][0])) \
            if str(df_subj["NMSQ_preop"][0]) != 'nan' else self.nmsq.setText('')
        self.eq5d.setText(str(df_subj["EQ5D_preop"][0])) \
            if str(df_subj["EQ5D_preop"][0]) != 'nan' else self.eq5d.setText('')
        self.demtect.setText(str(df_subj["DemTect_preop"][0])) \
            if str(df_subj["DemTect_preop"][0]) != 'nan' else self.demtect.setText('')
        self.pdq8.setText(str(df_subj["PDQ8_preop"][0])) \
            if str(df_subj["PDQ8_preop"][0]) != 'nan' else self.pdq8.setText('')
        self.pdq39.setText(str(df_subj["PDQ39_preop"][0])) \
            if str(df_subj["PDQ39_preop"][0]) != 'nan' else self.pdq39.setText('')
        self.se.setText(str(df_subj["S&E_preop"][0])) \
            if str(df_subj["S&E_preop"][0]) != 'nan' else self.se.setText('')

        # Edit Upper CheckBoxes with content using a ternary operator
        self.Report_preop.setChecked(True) if df_subj["Report_preop"][0] != 0 else self.Report_preop.setChecked(False)
        self.Decision_DBS_preop.setChecked(True) if df_subj["Decision_DBS_preop"][0] != 0 else self.Decision_DBS_preop.setChecked(False)
        self.icVRCS_preop.setChecked(True) if df_subj["icVRCS_preop"][0] != 0 else self.icVRCS_preop.setChecked(False)
        self.inexVRCS_preop.setChecked(True) if df_subj["inexVRCS_preop"][0] != 0 else self.inexVRCS_preop.setChecked(False)

        # Edit Lower CheckBoxes with content using a ternary operator
        self.Video_File_preop.setChecked(True) if df_subj["Video_preop"][0] != 0 else self.Video_File_preop.setChecked(False)
        self.MRI_preop.setChecked(True) if df_subj["MRI_preop"][0] != 0 else self.MRI_preop.setChecked(False)
        self.fpcit_spect_preop.setChecked(True) if df_subj["fpcit_spect_preop"][0] != 0 else self.fpcit_spect_preop.setChecked(False)

        return

    # ====================   Defines actions when buttons are pressed      ====================
    @QtCore.pyqtSlot()
    def onClickedMedication(self):
        """Shows medication dialog ; former implementation with creating GUI was replaced with show/hide GUI which is
        initiated at beginning at the disadvantage of not being saved until GUIpreoperative is closed"""
        self.dialog_medication.show()

    def onClickedSaveReturn(self):
        """closes GUI and returns to calling (main) GUI"""

        subj_id = General.read_current_subj().id[0]  # reads data from current_subj (saved in ./tmp)
        df_general = Clean.extract_subject_data(subj_id)

        # First of all, read general data so that pre-/intra- and postoperative share these
        try:
            df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=',')
            df_subj = df.iloc[df.index[df['ID'] == subj_id][0], :].to_dict()
        except IndexError:
            df_subj = {k: '' for k in Content.extract_saved_data(self.date).keys()}  # create empty dictionary

        # Start filling the dataframe [df_subj] with data from the entries in the GUI
        df_general.reset_index(inplace=True, drop=True)

        # Compare with general_data.csv
        df_subj['ID'] = General.read_current_subj().id[0]
        df_subj['PID'] = df_general['PID_ORBIS'][0]
        df_subj['Gender'] = df_general['Gender'][0]
        df_subj['Diagnosis_preop'] = df_general['diagnosis'][0]

        # Now extract changed data from the GUI
        df_subj["First_Diagnosed_preop"] = self.lineEditFirstDiagnosed.text()
        df_subj['Admission_preop'] = self.lineEditAdmNeurIndCheck.text()
        df_subj['Dismissal_preop'] = self.DismNeurIndCheckLabel.text()
        df_subj['Outpat_Contact_preop'] = self.lineEditOutpatientContact.text()
        df_subj['nch_preop'] = self.lineEditNChContact.text()
        df_subj['DBS_Conference_preop'] = self.lineEditDBSconferenceDate.text()
        df_subj["H&Y_preop"] = self.hy.text()
        df_subj["UPDRS_On_preop"] = self.updrsON.text()
        df_subj["UPDRS_Off_preop"] = self.updrsOFF.text()
        df_subj["UPDRSII_preop"] = self.updrsII.text()
        df_subj["HRUQ_preop"] = self.hruq.text()
        df_subj["MoCa_preop"] = self.moca.text()
        df_subj["MMST_preop"] = self.mmst.text()
        df_subj["BDI2_preop"] = self.bdi2.text()
        df_subj["NMSQ_preop"] = self.nmsq.text()
        df_subj["EQ5D_preop"] = self.eq5d.text()
        df_subj["DemTect_preop"] = self.demtect.text()
        df_subj["PDQ8_preop"] = self.pdq8.text()
        df_subj["PDQ39_preop"] = self.pdq39.text()
        df_subj["S&E_preop"] = self.se.text()

        # df_subj["Video_preop"], df_subj["MRI_preop"], df_subj["fpcit_spect_preop"] = 0, 0, 0
        # if self.VideoFile.isChecked():
        #     df_subj["Video_preop"] = 1
        # if self.MRIpreop.isChecked():
        #     df_subj["MRI_preop"] = 1
        # if self.FPCITpreop.isChecked():
        #     df_subj["fpcit_spect_preop"] = 1
        #
        # df_subj["Report_preop"], df_subj["Decision_DBS_preop"], \
        #     df_subj["icVRCS_preop"], df_subj["inexVRCS_preop"] = 0, 0, 0, 0
        # if self.Report.isChecked():
        #     df_subj["Report_preop"] = 1
        # if self.DecisionDBS.isChecked():
        #     df_subj["Decision_DBS_preop"] = 1
        # if self.ConsentVercise.isChecked():
        #     df_subj["icVRCS_preop"] = 1
        # if self.In_ExclusionCheckVercise.isChecked():
        #     df_subj["inexVRCS_preop"] = 1

        checkboxes = ["Video_File_preop", "MRI_preop", "fpcit_spect_preop", "Report_preop",
                      "Decision_DBS_preop", "icVRCS_preop", "inexVRCS_preop"]
        for checkbox in checkboxes:
            df_subj[checkbox] = 1 if getattr(self, checkbox).isChecked() else 0

        # Incorporate the [df_subj] dataframe into the entire dataset and save as csv
        idx2replace = df.index[df['ID'] == subj_id][0]
        df.iloc[idx2replace, :] = df_subj
        df = df.replace(['nan', ''], [np.nan, np.nan])
        df.to_csv(Path(f"{FILEDIR}/{self.date}.csv"), index=False)

        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = PreoperativeDialog()
    dlg.show()
    sys.exit(app.exec_())
