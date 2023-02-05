#!/usr/bin/env python3
import os, sys, re

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QFileDialog, QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QCheckBox
from GUI.GUImedication import MedicationDialog
from utils.helper_functions import General, Content, Clean, Output
from dependencies import FILEDIR


class PostoperativeDialog(QDialog):
    """Dialog to introduce all important information of postoperative patients."""

    def __init__(self, parent=None):
        """Initializer."""
        super(PostoperativeDialog, self).__init__(parent)
        self.date = 'postoperative_test'  # next two lines define the postoperative date data stem from/are saved at
        self.postoperative_date = ''

        subj_details = General.read_current_subj()
        General.synchronize_data_with_general(self.date, subj_details.id[0],
                                              messagebox=False)
        #Todo: can't run the code with these two lines:
        #self.dialog_medication = MedicationDialog(parent=self, visit=self.date)  # create medication dialog
        #self.dialog_medication.hide()

        # ====================    Create General Layout      ====================
        self.setWindowTitle('Postoperative Information (PID: {})'.format(str(int(subj_details.pid))))  # not necessary
        self.setGeometry(200, 100, 280, 170)
        self.move(400, 200)

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # Create one optionbox for the time being left
        self.optionbox1 = QGroupBox('Important Dates')
        self.optionbox1Content = QVBoxLayout(self.optionbox1)
        layout_general.addWidget(self.optionbox1, 0, 0)

        self.subj_Admission_Nch = QLabel('Admission Neurosurgery (dd/mm/yyyy):\t')
        self.lineEditAdmission_Nch = QLineEdit()
        lay1 = QHBoxLayout()
        lay1.addWidget(self.subj_Admission_Nch)
        lay1.addWidget(self.lineEditAdmission_Nch)
        lay1.addStretch()

        self.subj_Admission_NR = QLabel('Admission Neurology (dd/mm/yyyy):\t')
        self.lineEditAdmission_NR = QLineEdit()
        lay2 = QHBoxLayout()
        lay2.addWidget(self.subj_Admission_NR)
        lay2.addWidget(self.lineEditAdmission_NR)
        lay2.addStretch()

        self.subj_Dismission_Nch = QLabel('Dismission Neurosurgery (dd/mm/yyyy):')
        self.lineEditDismission_Nch = QLineEdit()
        lay3 = QHBoxLayout()
        lay3.addWidget(self.subj_Dismission_Nch)
        lay3.addWidget(self.lineEditDismission_Nch)
        lay3.addStretch()

        self.subj_Dismission_NR = QLabel('Dismission Neurology (dd/mm/yyyy):\t')
        self.lineEditDismission_NR = QLineEdit()
        lay4 = QHBoxLayout()
        lay4.addWidget(self.subj_Dismission_NR)
        lay4.addWidget(self.lineEditDismission_NR)
        lay4.addStretch()

        self.subj_Surgery = QLabel('Surgery Date (dd/mm/yyyy):\t\t')
        self.lineEditSurgery = QLineEdit()
        lay5 = QHBoxLayout()
        lay5.addWidget(self.subj_Surgery)
        lay5.addWidget(self.lineEditSurgery)
        lay5.addStretch()

        self.subj_Last_Revision = QLabel('Last Revision (dd/mm/yyyy):\t\t')
        self.lineEditLast_Revision = QLineEdit()
        lay6 = QHBoxLayout()
        lay6.addWidget(self.subj_Last_Revision)
        lay6.addWidget(self.lineEditLast_Revision)
        lay6.addStretch()

        self.subj_Outpatient_Contact = QLabel('Outpatient Contact (dd/mm/yyyy):\t')
        self.lineEditOutpatient_Contact = QLineEdit()
        lay7 = QHBoxLayout()
        lay7.addWidget(self.subj_Outpatient_Contact)
        lay7.addWidget(self.lineEditOutpatient_Contact)
        lay7.addStretch()

        self.optionbox1Content.addLayout(lay1)
        self.optionbox1Content.addLayout(lay2)
        self.optionbox1Content.addLayout(lay3)
        self.optionbox1Content.addLayout(lay4)
        self.optionbox1Content.addLayout(lay5)
        self.optionbox1Content.addLayout(lay6)
        self.optionbox1Content.addLayout(lay7)
        self.optionbox1.setLayout(self.optionbox1Content)

        # Create second optionbox top right
        self.optionbox2 = QGroupBox('Reason')
        self.optionbox2Content = QVBoxLayout(self.optionbox2)
        layout_general.addWidget(self.optionbox2, 0, 1)

        self.subj_reason = QLabel('Reason:\t\t')
        self.lineEditreason = QComboBox()
        self.fill_combobox()
        self.lineEditreason.currentIndexChanged.connect(self.update_context)
        self.lineEditreason.setFixedHeight(20)

        lay8 = QHBoxLayout()
        lay8.addWidget(self.subj_reason)
        lay8.addWidget(self.lineEditreason)
        lay8.addStretch()

        self.subj_Adverse_Event = QLabel('Adverse Events:\t')
        self.lineEditAdverse_Event = QLineEdit()
        self.lineEditAdverse_Event.setFixedWidth(300)
        self.lineEditAdverse_Event.setFixedHeight(50)
        lay9 = QHBoxLayout()
        lay9.addWidget(self.subj_Adverse_Event)
        lay9.addWidget(self.lineEditAdverse_Event)
        lay9.addStretch()

        self.optionbox2Content.addLayout(lay8)
        self.optionbox2Content.addLayout(lay9)
        self.optionbox2.setLayout(self.optionbox2Content)

        # Create third optionbox on the second row left
        self.optionbox3 = QGroupBox('Reports')
        self.optionbox3Content = QVBoxLayout(self.optionbox3)
        layout_general.addWidget(self.optionbox3, 1, 0)

        self.ReportNeurCheck = QCheckBox()
        self.ReportNeur = QLabel('Report Neurology \t\t')
        self.ReportNeurosurgeryCheck = QCheckBox()
        self.ReportNeurosurgery = QLabel('Report Neurosurgery\t')
        self.PatProgrammerCheck = QCheckBox()
        self.PatProgrammer = QLabel('Patient Programmer in use')

        box2line1 = QHBoxLayout()
        box2line1.addWidget(self.ReportNeurCheck)
        box2line1.addWidget(self.ReportNeur)
        box2line1.addWidget(self.ReportNeurosurgeryCheck)
        box2line1.addWidget(self.ReportNeurosurgery)
        box2line1.addWidget(self.PatProgrammerCheck)
        box2line1.addWidget(self.PatProgrammer)
        box2line1.addStretch()

        self.PostopCTCheck = QCheckBox()
        self.PostopCT = QLabel('Postoperative CT Scan\t')
        self.BatteryReplacementCheck = QCheckBox()
        self.BatteryReplacement = QLabel('Battery Replacement\t')
        self.PlannedVisitCheck = QCheckBox()
        self.PlannedVisit = QLabel('Planned Visit')

        box2line2 = QHBoxLayout()
        box2line2.addWidget(self.PostopCTCheck)
        box2line2.addWidget(self.PostopCT)
        box2line2.addWidget(self.BatteryReplacementCheck)
        box2line2.addWidget(self.BatteryReplacement)
        box2line2.addWidget(self.PlannedVisitCheck)
        box2line2.addWidget(self.PlannedVisit)
        box2line2.addStretch()

        self.QualiPaCheck = QCheckBox()
        self.QualiPa = QLabel('QualiPa Visit')

        box2line3 = QHBoxLayout()
        box2line3.addWidget(self.QualiPaCheck)
        box2line3.addWidget(self.QualiPa)
        box2line3.addStretch()

        self.optionbox3Content.addLayout(box2line1)
        self.optionbox3Content.addLayout(box2line2)
        self.optionbox3Content.addLayout(box2line3)
        self.optionbox3.setLayout(self.optionbox3Content)

        # optionbox 4: 2th row, right

        self.optionbox4 = QGroupBox('Tests')
        self.optionbox4Content = QVBoxLayout(self.optionbox4)
        layout_general.addWidget(self.optionbox4, 1, 1)

        self.UPDRSI = QLabel('UPDRS I:')
        self.lineEditUPDRSI = QLineEdit()
        self.lineEditUPDRSI.setFixedWidth(50)
        self.UPDRSIV = QLabel('UPDRS IV:')
        self.lineEditUPDRSIV = QLineEdit()
        self.lineEditUPDRSIV.setFixedWidth(50)
        self.TSS = QLabel('TSS:')
        self.lineEditTSS = QLineEdit()
        self.lineEditTSS.setFixedWidth(50)
        self.CGICPat = QLabel('CGIC patient:')
        self.lineEditCGICPat = QLineEdit()
        self.lineEditCGICPat.setFixedWidth(50)
        self.CGICClinician = QLabel('CGIC clinician and cargiver:')
        self.lineEditCGICClinician = QLineEdit()
        self.lineEditCGICClinician.setFixedWidth(50)

        box4line1 = QHBoxLayout()
        box4line1.addWidget(self.UPDRSI)
        box4line1.addWidget(self.lineEditUPDRSI)
        box4line1.addWidget(self.UPDRSIV)
        box4line1.addWidget(self.lineEditUPDRSIV)
        box4line1.addWidget(self.TSS)
        box4line1.addWidget(self.lineEditTSS)
        box4line1.addWidget(self.CGICPat)
        box4line1.addWidget(self.lineEditCGICPat)
        box4line1.addWidget(self.CGICClinician)
        box4line1.addWidget(self.lineEditCGICClinician)
        box4line1.addStretch()

        self.UPDRSON = QLabel('UPDRS On:')
        self.lineEditUPDRSON = QLineEdit()
        self.lineEditUPDRSON.setFixedWidth(50)
        self.UPDRSII = QLabel('UPDRS II:')
        self.lineEditUPDRSII = QLineEdit()
        self.lineEditUPDRSII.setFixedWidth(50)
        self.HRUQ = QLabel('HRUQ:')
        self.lineEditHRUQ = QLineEdit()
        self.lineEditHRUQ.setFixedWidth(50)
        self.MoCa = QLabel('MoCa:')
        self.lineEditMoCa = QLineEdit()
        self.lineEditMoCa.setFixedWidth(50)
        self.MMST = QLabel('MMST:')
        self.lineEditMMST = QLineEdit()
        self.lineEditMMST.setFixedWidth(50)
        self.BDIII = QLabel('BDI-II:')
        self.lineEditBDIII = QLineEdit()
        self.lineEditBDIII.setFixedWidth(50)
        self.NMSQ = QLabel('NMSQ:')
        self.lineEditNMSQ = QLineEdit()
        self.lineEditNMSQ.setFixedWidth(50)

        box4line2 = QHBoxLayout()
        box4line2.addWidget(self.UPDRSON)
        box4line2.addWidget(self.lineEditUPDRSON)
        box4line2.addWidget(self.UPDRSII)
        box4line2.addWidget(self.lineEditUPDRSII)
        box4line2.addWidget(self.HRUQ)
        box4line2.addWidget(self.lineEditHRUQ)
        box4line2.addWidget(self.MoCa)
        box4line2.addWidget(self.lineEditMoCa)
        box4line2.addWidget(self.MMST)
        box4line2.addWidget(self.lineEditMMST)
        box4line2.addWidget(self.BDIII)
        box4line2.addWidget(self.lineEditBDIII)
        box4line2.addWidget(self.NMSQ)
        box4line2.addWidget(self.lineEditNMSQ)
        box4line2.addStretch()

        self.UPDRSOff = QLabel('UPDRS Off:')
        self.lineEditUPDRSOff = QLineEdit()
        self.lineEditUPDRSOff.setFixedWidth(50)
        self.HY = QLabel('H&Y:')
        self.lineEditHY = QLineEdit()
        self.lineEditHY.setFixedWidth(50)
        self.EQ5D = QLabel('EQ5D:')
        self.lineEditEQ5D = QLineEdit()
        self.lineEditEQ5D.setFixedWidth(50)
        self.DemTect = QLabel('DemTect:\t')
        self.lineEditDemTect = QLineEdit()
        self.lineEditDemTect.setFixedWidth(50)
        self.PDQ8 = QLabel('PDQ8:')
        self.lineEditPDQ8 = QLineEdit()
        self.lineEditPDQ8.setFixedWidth(50)
        self.PDQ39 = QLabel('PDQ39:')
        self.lineEditPDQ39 = QLineEdit()
        self.lineEditPDQ39.setFixedWidth(50)
        self.SE = QLabel('S&E:')
        self.lineEditSE = QLineEdit()
        self.lineEditSE.setFixedWidth(50)

        box4line3 = QHBoxLayout()
        box4line3.addWidget(self.UPDRSOff)
        box4line3.addWidget(self.lineEditUPDRSOff)
        box4line3.addWidget(self.HY)
        box4line3.addWidget(self.lineEditHY)
        box4line3.addWidget(self.EQ5D)
        box4line3.addWidget(self.lineEditEQ5D)
        box4line3.addWidget(self.DemTect)
        box4line3.addWidget(self.lineEditDemTect)
        box4line3.addWidget(self.PDQ8)
        box4line3.addWidget(self.lineEditPDQ8)
        box4line3.addWidget(self.PDQ39)
        box4line3.addWidget(self.lineEditPDQ39)
        box4line3.addWidget(self.SE)
        box4line3.addWidget(self.lineEditSE)
        box4line3.addStretch()

        self.UDDRSOn = QLabel('UDDRS On:')
        self.lineEditUDDRSOn = QLineEdit()
        self.lineEditUDDRSOn.setFixedWidth(50)
        self.TRSOn = QLabel('TRS On:\t')
        self.lineEditTRSOn = QLineEdit()
        self.lineEditTRSOn.setFixedWidth(50)

        box4line4 = QHBoxLayout()
        box4line4.addWidget(self.UDDRSOn)
        box4line4.addWidget(self.lineEditUDDRSOn)
        box4line4.addWidget(self.TRSOn)
        box4line4.addWidget(self.lineEditTRSOn)
        box4line4.addStretch()

        self.UDDRSOff = QLabel('UDDRS Off:')
        self.lineEditUDDRSOff = QLineEdit()
        self.lineEditUDDRSOff.setFixedWidth(50)
        self.TRSOff = QLabel('TRS Off:\t')
        self.lineEditTRSOff = QLineEdit()
        self.lineEditTRSOff.setFixedWidth(50)

        box4line5 = QHBoxLayout()
        box4line5.addWidget(self.UDDRSOff)
        box4line5.addWidget(self.lineEditUDDRSOff)
        box4line5.addWidget(self.TRSOff)
        box4line5.addWidget(self.lineEditTRSOff)
        box4line5.addStretch()

        self.optionbox4Content.addLayout(box4line1)
        self.optionbox4Content.addLayout(box4line2)
        self.optionbox4Content.addLayout(box4line3)
        self.optionbox4Content.addLayout(box4line4)
        self.optionbox4Content.addLayout(box4line5)
        self.optionbox4.setLayout(self.optionbox4Content)

        # ====================    Optionbox (5) lower left      ====================
        self.optionbox5 = QGroupBox('DBS settings after dismissal')
        self.optionbox5Content = QVBoxLayout(self.optionbox5)
        layout_general.addWidget(self.optionbox5, 3, 0)

        self.DBSpercentageLeft = QGridLayout()
        for i in range(0, 1):
            if i == 0:
                self.DBSpercentageLeft.addWidget(QLabel('Left:\t'), i, 0)
            for j in range(0, 8):
                self.DBSpercentageLeft.addWidget(QLineEdit(), i, j + 1)

        self.DBSpercentageRight = QGridLayout()
        for i in range(0, 1):
            if i == 0:
                self.DBSpercentageRight.addWidget(QLabel('Right:\t'), i, 0)
            for j in range(0, 8):
                self.DBSpercentageRight.addWidget(QLineEdit(), i, j + 1)

        self.optionbox5Content.addStretch(2)
        self.optionbox5Content.addLayout(self.DBSpercentageLeft)
        self.optionbox5Content.addLayout(self.DBSpercentageRight)

        # ====================    Optionbox (8) lower right      ====================
        self.optionbox6 = QGroupBox('Amplitude, Pulse and Frequency')
        self.optionbox6Content = QVBoxLayout(self.optionbox6)
        layout_general.addWidget(self.optionbox6, 3, 1)

        self.gridDBSsettings = QGridLayout()
        self.gridDBSsettings.addWidget(QLabel('Left:\t'), 1, 0)
        self.gridDBSsettings.addWidget(QLabel('Right:\t'), 2, 0)
        self.gridDBSsettings.addWidget(QLabel('Amplitude [mA]'), 0, 1)
        self.gridDBSsettings.addWidget(QLabel('Pulse Width [µs]:'), 0, 2)
        self.gridDBSsettings.addWidget(QLabel('Frequency [Hz]'), 0, 3)

        for i in range(1, 3):
            for j in range(1, 4):
                self.gridDBSsettings.addWidget(QLineEdit(), i, j)
        self.optionbox6Content.addLayout(self.gridDBSsettings)

        self.optionbox6.setLayout(self.optionbox6Content)

        # ====================   Adds buttons at the bottom of the GUI      ====================
        self.ButtonEnterMedication = QPushButton('Open GUI \nMedication')
        self.button_save = QPushButton('Save and \nReturn')

        hlay_bottom = QHBoxLayout()
        hlay_bottom.addStretch(5)
        hlay_bottom.addWidget(self.ButtonEnterMedication)
        hlay_bottom.addWidget(self.button_save)
        hlay_bottom.addStretch(1)
        layout_general.addLayout(hlay_bottom, 4, 0, 1, 3)

        self.read_content_csv()

        # ====================   Actions when buttons are pressed      ====================
        self.ButtonEnterMedication.clicked.connect(self.on_clickedMedication)
        self.button_save.clicked.connect(self.onClickedSaveReturn)

    def fill_combobox(self):
        """fills the ComboBox for the postoperative dates and performs some additional steps to maintain code tidy"""

        items_available = Content.extract_postoperative_dates()
        items_available = ['Please select', 'Enter data'] if not items_available else items_available + ['Enter data']

        #        result = [''.join(map(str, element)) if isinstance(element, list) else element for element in
        #                           items_available]

        # Remove duplicates using a set
        items_available = list(set(items_available))

        # Convert items to strings and remove "nan" values
        items_available = [str(item) for item in items_available]
        items_available = [item for item in items_available if item != "nan"]

        # Remove empty items
        items_available = list(filter(None, items_available))

        # Add items to ComboBox
        self.lineEditreason.addItems(items_available)
        self.comboBox = self.lineEditreason
        self.comboBox.currentTextChanged.connect(self.read_content_csv)

        # def update_text_notworking(self):
        """I renamed this part as it was not working with my version, DP"""

    # ====================   Defines what happens when ComboBox is modified      ====================


    def read_content_csv(self):
        """dummy part of update text that served only to make it run; all parts of [update_text_notworking] should be
        moved here"""
        print('updating content ...')
        df_subj = General.import_dataframe(f"{self.date}.csv", separator_csv=',')
        if df_subj.empty:
            return

        df_subj = df_subj[df_subj['PID'] == General.read_current_subj().pid[0]]
        df_subj_filtered = df_subj[df_subj['Reason_postop'] == self.lineEditreason.currentText()]
        if df_subj.empty:
            return
        if df_subj_filtered.empty:
            return
            # do something if no rows are found
        else:
            row = df_subj_filtered.iloc[0]
            self.lineEditAdmission_Nch.setText(str(row["Admission_NCh_postop"])) \
                if str(row["Admission_NCh_postop"]) != 'nan' else self.lineEditAdmission_Nch.setText('')
            self.lineEditAdmission_NR.setText(str(row["Admission_NR_postop"])) \
                if str(row["Admission_NR_postop"]) != 'nan' else self.lineEditAdmission_NR.setText('')
            self.lineEditDismission_Nch.setText(str(row["Dismissal_NCh_postop"])) \
                if str(row["Dismissal_NCh_postop"]) != 'nan' else self.lineEditDismission_Nch.setText('')
            self.lineEditDismission_NR.setText(str(row["Dismissal_NR_postop"])) \
                if str(row["Dismissal_NR_postop"]) != 'nan' else self.lineEditDismission_NR.setText('')
            self.lineEditSurgery.setText(str(row["Surgery_Date_postop"])) \
                if str(row["Surgery_Date_postop"]) != 'nan' else self.lineEditSurgery.setText('')
            # self.lineEditLast_Revision.setText(str(df_subj[""][0]))\
            # if str(df_subj[""][0]) != 'nan' else self.lineEditLast_Revision.setText('')
            # self.lineEditOutpatient_Contact.setText(str(df_subj[""][0]))\
            # if str(df_subj[""][0]) != 'nan' else self.lineEditOutpatient_Contact.setText('')

            # upper right

            self.lineEditAdverse_Event.setText(str(row["AE_postop"])) \
                if str(row["AE_postop"]) != 'nan' else self.lineEditAdverse_Event.setText('')

            # middle right
            self.lineEditUPDRSI.setText(str(row["UPDRS1_postop"])) \
                if str(row["UPDRS1_postop"]) != 'nan' else self.lineEditUPDRSI.setText('')
            self.lineEditUPDRSIV.setText(str(row["UPDRS4_postop"])) \
                if str(row["UPDRS4_postop"]) != 'nan' else self.lineEditUPDRSIV.setText('')
            self.lineEditTSS.setText(str(row["TSS_postop"])) \
                if str(row["TSS_postop"]) != 'nan' else self.lineEditTSS.setText('')
            self.lineEditCGICPat.setText(str(row["CGIG_patient_postop"])) \
                if str(row["CGIG_patient_postop"]) != 'nan' else self.lineEditCGICPat.setText('')
            self.lineEditCGICClinician.setText(str(row["CGIG_clinician_cargiver_postop"])) \
                if str(row["CGIG_clinician_cargiver_postop"]) != 'nan' else self.lineEditCGICClinician.setText('')
            self.lineEditUPDRSON.setText(str(row["UPDRSon_postop"])) \
                if str(row["UPDRSon_postop"]) != 'nan' else self.lineEditUPDRSON.setText('')
            self.lineEditUPDRSII.setText(str(row["UPDRSII_postop"])) \
                if str(row["UPDRSII_postop"]) != 'nan' else self.lineEditUPDRSII.setText('')
            # self.lineEditHRUQ.setText(str(row[""]))
            # if str(row[""]) != 'nan' else self.lineEditHRUQ.setText('')
            self.lineEditMoCa.setText(str(row["MoCa_postop"])) \
                if str(row["MoCa_postop"]) != 'nan' else self.lineEditMoCa.setText('')
            self.lineEditMMST.setText(str(row["MMST_postop"])) \
                if str(row["MMST_postop"]) != 'nan' else self.lineEditMMST.setText('')
            self.lineEditBDIII.setText(str(row["BDI2_postop"])) \
                if str(row["BDI2_postop"]) != 'nan' else self.lineEditBDIII.setText('')
            self.lineEditNMSQ.setText(str(row["NMSQ_postop"])) \
                if str(row["NMSQ_postop"]) != 'nan' else self.lineEditNMSQ.setText('')
            # self.lineEditUPDRSOff.setText(str(row[""])) \
            # if str(row[""]) != 'nan' else self.lineEditUPDRSOff.setText('')
            self.lineEditHY.setText(str(row["H&Y_postop"])) \
                if str(row["H&Y_postop"]) != 'nan' else self.lineEditHY.setText('')
            self.lineEditEQ5D.setText(str(row["EQ5D_postop"])) \
                if str(row["EQ5D_postop"]) != 'nan' else self.lineEditEQ5D.setText('')
            self.lineEditDemTect.setText(str(row["DemTect_postop"])) \
                if str(row["DemTect_postop"]) != 'nan' else self.lineEditDemTect.setText('')
            self.lineEditPDQ8.setText(str(row["PDQ8_postop"])) \
                if str(row["PDQ8_postop"]) != 'nan' else self.lineEditPDQ8.setText('')
            self.lineEditPDQ39.setText(str(row["PDQ39_postop"])) \
                if str(row["PDQ39_postop"]) != 'nan' else self.lineEditPDQ39.setText('')
            self.lineEditSE.setText(str(row["S&E_postop"])) \
                if str(row["S&E_postop"]) != 'nan' else self.lineEditSE.setText('')
            # self.lineEditUDDRSOn.setText(str(row[""])) \
            # if str(row[""]) != 'nan' else self.lineEditUDDRSOn.setText('')
            self.lineEditTRSOn.setText(str(row["TRSon_postop"])) \
                if str(row["TRSon_postop"]) != 'nan' else self.lineEditTRSOn.setText('')
            self.lineEditUDDRSOff.setText(str(row["UDDRSoff_postop"])) \
                if str(row["UDDRSoff_postop"]) != 'nan' else self.lineEditUDDRSOff.setText('')
            self.lineEditTRSOff.setText(str(row["TRSoff_postop"])) \
                if str(row["TRSoff_postop"]) != 'nan' else self.lineEditTRSOff.setText('')

            # Edit CheckBoxes with content
            # middle left
            if row["Report_File_NCh_postop"] != 0:
                self.ReportNeurCheck.setChecked(True)
            if row["Report_File_NR_postop"] != 0:
                self.ReportNeurosurgeryCheck.setChecked(True)
            if row["Using_Programmer_postop"] != 0:
                self.PatProgrammerCheck.setChecked(True)
            if row["CTscan_postop"] != 0:
                self.PostopCTCheck.setChecked(True)
            if row["Battery_Replacement_postop"] != 0:
                self.BatteryReplacementCheck.setChecked(True)
            if row["Planned_Visit_postop"] != 0:
                self.PlannedVisitCheck.setChecked(True)
            if row["Qualipa_Visit_postop"] != 0:
                self.QualiPaCheck.setChecked(True)

            # bottom left
            # DBS left

            # TODO: add if-statement for empty values.

            DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 1).widget()
            DBSleft.setText(str(row["Perc1_postop"]))
            DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 2).widget()
            DBSleft.setText(str(row["Perc2_postop"]))
            DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 3).widget()
            DBSleft.setText(str(row["Perc3_postop"]))
            DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 4).widget()
            DBSleft.setText(str(row["Perc4_postop"]))
            DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 5).widget()
            DBSleft.setText(str(row["Perc5_postop"]))
            DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 6).widget()
            DBSleft.setText(str(row["Perc6_postop"]))
            DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 7).widget()
            DBSleft.setText(str(row["Perc7_postop"]))
            DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 8).widget()
            DBSleft.setText(str(row["Perc8_postop"]))

            # DBS right

            DBSright = self.DBSpercentageRight.itemAtPosition(0, 1).widget()
            DBSright.setText(str(row["Perc9_postop"]))
            DBSright = self.DBSpercentageRight.itemAtPosition(0, 2).widget()
            DBSright.setText(str(row["Perc10_postop"]))
            DBSright = self.DBSpercentageRight.itemAtPosition(0, 3).widget()
            DBSright.setText(str(row["Perc11_postop"]))
            DBSright = self.DBSpercentageRight.itemAtPosition(0, 4).widget()
            DBSright.setText(str(row["Perc12_postop"]))
            DBSright = self.DBSpercentageRight.itemAtPosition(0, 5).widget()
            DBSright.setText(str(row["Perc13_postop"]))
            DBSright = self.DBSpercentageRight.itemAtPosition(0, 6).widget()
            DBSright.setText(str(row["Perc14_postop"]))
            DBSright = self.DBSpercentageRight.itemAtPosition(0, 7).widget()
            DBSright.setText(str(row["Perc15_postop"]))
            DBSright = self.DBSpercentageRight.itemAtPosition(0, 8).widget()
            DBSright.setText(str(row["Perc16_postop"]))

            # Bottom right
            # setting left

            # Get a reference to the Amplitude widget for the left side
            amplitudeLeftWidget = self.gridDBSsettings.itemAtPosition(1, 1).widget()
            amplitudeLeftWidget.setText(str(row["AmplL_postop"]))

            pulseWidthLeftWidget = self.gridDBSsettings.itemAtPosition(1, 2).widget()
            pulseWidthLeftWidget.setText(str(row["PWL_postop"]))

            frequencyLeftWidget = self.gridDBSsettings.itemAtPosition(1, 3).widget()
            frequencyLeftWidget.setText(str(row["FreqL_postop"]))

            amplitudeRightWidget = self.gridDBSsettings.itemAtPosition(2, 1).widget()
            amplitudeRightWidget.setText(str(row["AmplR_postop"]))

            pulseWidthRightWidget = self.gridDBSsettings.itemAtPosition(2, 2).widget()
            pulseWidthRightWidget.setText(str(row["PWR_postop"]))

            frequencyRightWidget = self.gridDBSsettings.itemAtPosition(2, 3).widget()
            frequencyRightWidget.setText(str(row["FreqR_postop"]))

    def update_context(self):
        """updates the context according to what was elected in the ComboBox"""
        if self.lineEditreason.currentText() == 'Please select':
            pass
        elif self.lineEditreason.currentText() == 'Enter data':
            Output.open_input_dialog_postoperative(self)
            data_frame = General.import_dataframe(f"{self.date}.csv", separator_csv=',')
            subj_details = General.read_current_subj()

            match = re.search(r'^(pre|intra|post)op', self.date)
            data_frame.loc[len(data_frame), ['ID', 'PID', 'Reason_{}'.format(match.group())]] = [subj_details.id[0], subj_details.pid[0],
                                                                               self.postoperative_date]
            data_frame = data_frame.replace(['nan', ''], [np.nan, np.nan])
            data_frame = data_frame.applymap(lambda x: str(x).replace(';', ' -'))
            data_frame.to_csv(os.path.join(FILEDIR, f"{self.date}.csv"), index=False)

            self.lineEditreason.clear()
            self.fill_combobox()
            self.read_content_csv()
        else:
            self.postoperative_date = self.lineEditreason.currentText()
            self.read_content_csv()
            print('something should happen here')

    # ====================   Defines actions when buttons are pressed      ====================

    @QtCore.pyqtSlot()
    def on_clickedMedication(self):
        """shows the medication dialog when button is pressed; former implementation with creating GUI was replaced with
        show/hide GUI which is initiated at beginning"""
        self.dialog_medication.show()

    def onClickedSaveReturn(self):


        # df_general = Clean.extract_subject_data()
        current_subj = General.read_current_subj()
        subject_id = current_subj['id'][0]
        df_general = Clean.extract_subject_data(subject_id)
        match = re.search(r'^(pre|intra|post)op', self.date)

        # First of all, read general data so that pre-/intra- and postoperative share these
        try:
            subj_id = General.read_current_subj().id[0]  # reads data from current_subj (saved in ./tmp)
            df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=',')
            if df.shape[1] == 1:
                df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=';')
            df_subj = df.iloc[df.index[df['ID'] == subj_id][0], :].to_dict()
        except IndexError:
            df_subj = {k: '' for k in Content.extract_saved_data(self.date).keys()}  # create empty dictionary

        # Drop rows with empty values in columns 3 through 9
        df.drop(df[df.iloc[:, 2:9].isnull().any(axis=1)].index, inplace=True)

        df_general.reset_index(inplace=True, drop=True)

        df_subj['ID'] = General.read_current_subj().id[0]
        df_subj['PID'] = df_general.iloc[0, :]['PID_ORBIS']
        df_subj['Gender'] = df_general['Gender'][0]
        df_subj['Diagnosis_{}'.format(match.group())] = df_general['diagnosis'][0]

        # Now extract teh changed data from the GUI

        # upper left
        df_subj['Admission_NCh_{}'.format(match.group())] = self.lineEditAdmission_Nch.text()
        df_subj['Admission_NR_{}'.format(match.group())] = self.lineEditAdmission_NR.text()
        df_subj['Dismissal_NCh_{}'.format(match.group())] = self.lineEditDismission_Nch.text()
        df_subj['Dismissal_NR_{}'.format(match.group())] = self.lineEditDismission_NR.text()
        df_subj['Surgery_Date_{}'.format(match.group())] = self.lineEditSurgery.text()
        # df_subj[''] = self.lineEditLast_Revision.text()
        # df_subj[''] = self.lineEditOutpatient_Contact.text()

        # upper right
        df_subj['AE_{}'.format(match.group())] = self.lineEditAdverse_Event.text()

        # middle right
        df_subj['UPDRS1_{}'.format(match.group())] = self.lineEditUPDRSI.text()
        df_subj['UPDRS4_{}'.format(match.group())] = self.lineEditUPDRSIV.text()
        df_subj['TSS_postop'] = self.lineEditTSS.text()
        df_subj['CGIG_patient_postop'] = self.lineEditCGICPat.text()
        df_subj['CGIG_clinician_cargiver_postop'] = self.lineEditCGICClinician.text()
        df_subj["UPDRSon_postop"] = self.lineEditUPDRSON.text()
        df_subj["UPDRSII_postop"] = self.lineEditUPDRSII.text()
        # df_subj[""] = self.lineEditHRUQ.text()
        df_subj["MoCa_postop"] = self.lineEditMoCa.text()
        df_subj["MMST_postop"] = self.lineEditMMST.text()
        df_subj["BDI2_postop"] = self.lineEditBDIII.text()
        df_subj["NMSQ_postop"] = self.lineEditNMSQ.text()
        # df_subj[""] = self.lineEditUPDRSOff.text()
        df_subj["H&Y_postop"] = self.lineEditHY.text()
        df_subj["EQ5D_postop"] = self.lineEditEQ5D.text()
        df_subj["DemTect_postop"] = self.lineEditDemTect.text()
        df_subj["PDQ8_postop"] = self.lineEditPDQ8.text()
        df_subj["PDQ39_postop"] = self.lineEditPDQ39.text()
        df_subj["S&E_postop"] = self.lineEditSE.text()
        # df_subj[""] = self.lineEditUDDRSOn.text()
        df_subj["TRSon_postop"] = self.lineEditTRSOn.text()
        df_subj["UDDRSoff_postop"] = self.lineEditUDDRSOff.text()
        df_subj["TRSoff_postop"] = self.lineEditTRSOff.text()

        # middle left

        idx2replace = df[df['ID'] == subj_id].index[0]
        df.iloc[idx2replace, :] = df_subj
        df = df.replace(['nan', ''], [np.nan, np.nan])
        df.to_csv(os.path.join(FILEDIR, "{}.csv".format(self.date)), index=False)

        self.close()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "test.txt",
                                                  "All Files(*)", options=options)
        print(fileName)

    # for opening
    def open_dialog_box(self):
        option = QFileDialog.Options()
        # first parameter is self; second is the Window Title, third title is Default File Name, fourth is FileType,
        # fifth is options
        file = QFileDialog.getOpenFileName(self, "Save File Window Title", "default.txt",
                                           "All Files (*)", options=option)
        print(file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = PostoperativeDialog()
    dlg.show()
    sys.exit(app.exec_())
