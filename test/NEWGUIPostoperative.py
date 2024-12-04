#!/usr/bin/env python3
import os, sys, re
import pandas as pd
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QFileDialog, QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QCheckBox
from test.GUImedication import MedicationDialog
from utils.helper_functions import General, Content, Clean, Output, check_nan
from dependencies import FILEDIR
from utils.logger import logger
from test.LoadDatafromCSV import Postoperative_data
data = Postoperative_data


# TODO's: needs fix: go on 'save and return' after entering data before entering medicationGUI,
#  or else on 'return' all windows close and data will be deleted

# LE: changes work with python 3.11


class PostoperativeDialog(QtWidgets.QDialog):
    """Dialog to introduce all important information of postoperative patients."""

    def __init__(self, parent=None):
        """Initializer."""
        super(PostoperativeDialog, self).__init__(parent)
        self.date = 'postoperative'  # next two lines define the postoperative date data stem from/are saved at
        self.postoperative_date = ''
        subj_details = General.read_current_subj()
        General.synchronize_data_with_general(self.date, subj_details.id[0],
                                              messagebox=False)
        # creates medication dialog
        self.dialog_medication = MedicationDialog(parent=self, visit=self.date)
        self.dialog_medication.hide()

        # ====================    Create General Layout      ====================
        self.setWindowTitle('Postoperative Information (PID: {})'.format(str(int(subj_details.pid))))  # not necessary
        self.setGeometry(200, 100, 280, 170)
        self.move(400, 200)

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # Create optionbox1 ==Important Dates==, top left #
        ########################################
        self.optionbox1 = QGroupBox('Important Dates')
        self.optionbox1Content = QVBoxLayout(self.optionbox1)
        layout_general.addWidget(self.optionbox1, 0, 0)
        # lines to enter dates ff
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

        # Create optionbox2 ==Reason==, top right #
        #######################################
        self.optionbox2 = QGroupBox('Reason')
        self.optionbox2Content = QVBoxLayout(self.optionbox2)
        layout_general.addWidget(self.optionbox2, 0, 1)
        # Enter Data for reason
        self.subj_reason = QLabel('Reason:\t\t')
        self.lineEditreason = QComboBox()
        self.fill_combobox()
        self.lineEditreason.currentIndexChanged.connect(self.update_context)
        self.lineEditreason.setFixedHeight(20)

        lay8 = QHBoxLayout()
        lay8.addWidget(self.subj_reason)
        lay8.addWidget(self.lineEditreason)
        lay8.addStretch()
        # Textfield for Adverse Events
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

        # Create optionbox3 ==Report==, Checkboxes on the second row left #
        ###################################################################
        self.optionbox3 = QGroupBox('Reports')
        self.optionbox3Content = QVBoxLayout(self.optionbox3)
        layout_general.addWidget(self.optionbox3, 1, 0)
        # first row
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
        # second row
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
        # third row
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

        # optionbox4 ==Tests== 2th row, right #
        #######################################

        self.optionbox4 = QGroupBox('Tests')
        self.optionbox4Content = QVBoxLayout(self.optionbox4)
        layout_general.addWidget(self.optionbox4, 1, 1)
        # first row
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
        # second row
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
        # third row
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
        # forth row
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
        # fifth row
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

        # ====================Optionbox(5) ==DBS settings after dismissal== lower left ====================#
        ####################################################################################################

        self.optionbox5 = QGroupBox('DBS settings after dismissal')
        self.optionbox5Content = QVBoxLayout(self.optionbox5)
        layout_general.addWidget(self.optionbox5, 3, 0)
        # left side row
        self.DBSpercentageLeft = QGridLayout()
        for i in range(0, 1):
            if i == 0:
                self.DBSpercentageLeft.addWidget(QLabel('Left:\t'), i, 0)
            for j in range(0, 8):
                self.DBSpercentageLeft.addWidget(QLineEdit(), i, j + 1)
        # right side row
        self.DBSpercentageRight = QGridLayout()
        for i in range(0, 1):
            if i == 0:
                self.DBSpercentageRight.addWidget(QLabel('Right:\t'), i, 0)
            for j in range(0, 8):
                self.DBSpercentageRight.addWidget(QLineEdit(), i, j + 1)

        self.optionbox5Content.addStretch(2)
        self.optionbox5Content.addLayout(self.DBSpercentageLeft)
        self.optionbox5Content.addLayout(self.DBSpercentageRight)

        # ====================Optionbox(6) ==Amplitude,Pulse,Frequency== lower right====================#
        #################################################################################################
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

        data = Postoperative_data(r'C:\Users\toast\OneDrive\Desktop\GitHub\dbsPatients\data\postoperative.csv',
                                  int(subj_details.pid))
        self.read_content_csv(data)

# ==================== Actions when buttons are pressed, open medication window or save and close window  ====================
        self.ButtonEnterMedication.clicked.connect(self.on_clickedMedication)
        self.button_save.clicked.connect(self.onClickedSaveReturn)

    # Reason-> Enter data select field = combobox
    def fill_combobox(self):
        """fills the ComboBox for the postoperative dates and performs some additional steps to maintain code tidy"""

        items_available = Content.extract_postoperative_dates()
        items_available = ['Please select', 'Enter data'] if not items_available else items_available + ['Enter data']

        # result = [''.join(map(str, element)) if isinstance(element, list) else element for element in
        #                   items_available]

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

    # ====================   Updates and loads existing data from csv file      ====================

    def read_content_csv(self, data: Postoperative_data):
        """reads content from csv using the Posterperative_data class defined in LoadDatafromCSV.py """
        # Create an instance of the Postoperative_data class
#     postoperative_dialog = PostoperativeDialog()   # without these 2 line => attribute error (when different reason
        #     selected in combobox), with them => infinite loop
#     postoperative_dialog.read_content_csv(data)

     #   if isinstance(data, Postoperative_data):
            # Access the attributes of the data object
     #       if not check_nan(data.Admission_NCh_postop):
     #           self.lineEditAdmission_Nch.setText(str(data.Admission_NCh_postop))
     #   else:
            # Handle the case when the data object is not an instance of Postoperative_data
      #      print("Invalid data object")


        ################### Important Dates, optionbox1  #####################

        if not check_nan(data.Admission_NCh_postop):
            self.lineEditAdmission_Nch.setText(str(data.Admission_NCh_postop))
        else:
            self.lineEditAdmission_Nch.setText('')

        if not check_nan(data.Admission_NR_postop):
            self.lineEditAdmission_NR.setText(str(data.Admission_NR_postop))
        else:
            self.lineEditAdmission_NR.setText('')

        if not check_nan(data.Dismissal_NCh_postop):
            self.lineEditDismission_Nch.setText(str(data.Dismissal_NCh_postop))
        else:
            self.lineEditDismission_Nch.setText('')

        if not check_nan(data.Dismissal_NR_postop):
            self.lineEditDismission_NR.setText(str(data.Dismissal_NR_postop))
        else:
            self.lineEditDismission_NR.setText('')

        if not check_nan(data.Surgery_Date_postop):
            self.lineEditSurgery.setText(str(data.Surgery_Date_postop))
        else:
            self.lineEditSurgery.setText('')

        if not check_nan(data.Last_Revision_postop):
            self.lineEditLast_Revision.setText(str(data.Last_Revision_postop))
        else:
            self.lineEditLast_Revision.setText('')

        if not check_nan(data.Outpatient_Contact_postop):
            self.lineEditOutpatient_Contact.setText(str(data.Outpatient_Contact_postop))
        else:
            self.lineEditOutpatient_Contact.setText('')

        # ==Reason== upper right #
        #########################
        # Adverse Events Textfield
        self.lineEditAdverse_Event.setText(str(data.AE_postop)) if not check_nan(
            data.AE_postop) else self.lineEditAdverse_Event.setText('')

        # ==Test==, middle right #
        ######################
        self.lineEditUPDRSI.setText(str(data.UPDRS1_postop)) \
            if not check_nan(data.UPDRS1_postop) else self.lineEditUPDRSI.setText('')
        self.lineEditUPDRSIV.setText(str(data.UPDRS4_postop)) \
            if not check_nan(data.UPDRS4_postop) else self.lineEditUPDRSIV.setText('')
        self.lineEditTSS.setText(str(data.TSS_postop)) \
            if not check_nan(data.TSS_postop) else self.lineEditTSS.setText('')
        self.lineEditCGICPat.setText(str(data.CGIG_patient_postop)) \
            if not check_nan(data.CGIG_patient_postop) else self.lineEditCGICPat.setText('')
        self.lineEditCGICClinician.setText(str(data.CGIG_clinician_cargiver_postop)) \
            if not check_nan(data.CGIG_clinician_cargiver_postop) else self.lineEditCGICClinician.setText('')
        self.lineEditUPDRSON.setText(str(data.UPDRSon_postop)) \
            if not check_nan(data.UPDRSon_postop) else self.lineEditUPDRSON.setText('')
        self.lineEditUPDRSII.setText(str(data.UPDRSII_postop)) \
            if not check_nan(data.UPDRSII_postop) else self.lineEditUPDRSII.setText('')
        self.lineEditHRUQ.setText(str(data.HRUQ_postop)) \
            if not check_nan(data.HRUQ_postop) else self.lineEditHRUQ.setText('')
        self.lineEditMoCa.setText(str(data.MoCa_postop)) \
            if not check_nan(data.MoCa_postop) else self.lineEditMoCa.setText('')
        self.lineEditMMST.setText(str(data.MMST_postop)) \
            if not check_nan(data.MMST_postop) else self.lineEditMMST.setText('')
        self.lineEditBDIII.setText(str(data.BDI2_postop)) \
            if not check_nan(data.BDI2_postop) else self.lineEditBDIII.setText('')
        self.lineEditNMSQ.setText(str(data.NMSQ_postop)) \
            if not check_nan(data.NMSQ_postop) else self.lineEditNMSQ.setText('')
        self.lineEditUPDRSOff.setText(str(data.UPDRSOff_postop)) \
            if not check_nan(data.UPDRSOff_postop) else self.lineEditUPDRSOff.setText('')
        self.lineEditHY.setText(str(data.HuY_postop)) \
            if not check_nan(data.HuY_postop) else self.lineEditHY.setText('')
        self.lineEditEQ5D.setText(str(data.EQ5D_postop)) \
            if not check_nan(data.EQ5D_postop) else self.lineEditEQ5D.setText('')
        self.lineEditDemTect.setText(str(data.DemTect_postop)) \
            if not check_nan(data.DemTect_postop) else self.lineEditDemTect.setText('')
        self.lineEditPDQ8.setText(str(data.PDQ8_postop)) \
            if not check_nan(data.PDQ8_postop) else self.lineEditPDQ8.setText('')
        self.lineEditPDQ39.setText(str(data.PDQ39_postop)) \
            if not check_nan(data.PDQ39_postop) else self.lineEditPDQ39.setText('')
        self.lineEditSE.setText(str(data.SuE_postop)) \
            if not check_nan(data.SuE_postop) else self.lineEditSE.setText('')
        self.lineEditUDDRSOn.setText(str(data.UDDRSOn_postop)) \
            if not check_nan(data.UDDRSOn_postop) else self.lineEditUDDRSOn.setText('')
        self.lineEditTRSOn.setText(str(data.TRSon_postop)) \
            if not check_nan(data.TRSon_postop) else self.lineEditTRSOn.setText('')
        self.lineEditUDDRSOff.setText(str(data.UDDRSoff_postop)) \
            if not check_nan(data.UDDRSoff_postop) else self.lineEditUDDRSOff.setText('')
        self.lineEditTRSOff.setText(str(data.TRSoff_postop)) \
            if not check_nan(data.TRSoff_postop) else self.lineEditTRSOff.setText('')

        # ==Report== Checkboxes, middle left #
        ######################################

        # pandas liest leere daten als nan ==> nan != 0 ist True
        # ==> wenn checkbox in datensatz nicht angegeben wird hier fälschlicherweise auf True gesetzt.
        # LE: daher code Anpassung

        if not pd.isnull(data.Report_File_NCh_postop) and data.Report_File_NCh_postop != 0:
            self.ReportNeurCheck.setChecked(True)
        if not pd.isnull(data.Report_File_NR_postop) and data.Report_File_NR_postop != 0:
            self.ReportNeurosurgeryCheck.setChecked(True)
        if not pd.isnull(data.Using_Programmer_postop) and data.Using_Programmer_postop != 0:
            self.PatProgrammerCheck.setChecked(True)
        if not pd.isnull(data.CTscan_postop) and data.CTscan_postop != 0:
            self.PostopCTCheck.setChecked(True)
        if not pd.isnull(data.Battery_Replacement_postop) and data.Battery_Replacement_postop != 0:
            self.BatteryReplacementCheck.setChecked(True)
        if not pd.isnull(data.Planned_Visit_postop) and data.Planned_Visit_postop != 0:
            self.PlannedVisitCheck.setChecked(True)
        if not pd.isnull(data.Qualipa_Visit_postop) and data.Qualipa_Visit_postop != 0:
            self.QualiPaCheck.setChecked(True)
            # previously
            #        if data.Report_File_NCh_postop != 0:
            #            self.ReportNeurCheck.setChecked(True)
            #        if data.Report_File_NR_postop != 0:
            #            self.ReportNeurosurgeryCheck.setChecked(True)
            #        if data.Using_Programmer_postop != 0:
            #            self.PatProgrammerCheck.setChecked(True)
            #        if data.CTscan_postop != 0:
            #            self.PostopCTCheck.setChecked(True)
            #        if data.Battery_Replacement_postop != 0:
            #            self.BatteryReplacementCheck.setChecked(True)
            #        if data.Planned_Visit_postop != 0:
            #            self.PlannedVisitCheck.setChecked(True)
            #        if data.Qualipa_Visit_postop != 0:
            #            self.QualiPaCheck.setChecked(True)

            # == DBS settings after dismissal == bottom left #
            ##################################################

            # Edit LE: simplified code and added if-statement for empty values
            # Populating left DBS fields
            for i in range(1, 9):
                DBSleft = self.DBSpercentageLeft.itemAtPosition(0, i).widget()
                column_name = "Perc{}_postop".format(i)

                if column_name in data.d.columns:
                    value = data.d.loc[data.d.index[0], column_name]
                    if not pd.isna(value):  # Überprüfen, ob der Wert nicht NaN ist
                        DBSleft.setText(str(value))
                    else:
                        DBSleft.clear()
                else:
                    DBSleft.clear()  # Leerfeld, wenn der Wert NaN ist oder leer

                #  for i in range(0, 8):  had index issues with label not being displayed for rows, instead data of perc1+9 was
                #     DBSleft = self.DBSpercentageLeft.itemAtPosition(0, i).widget()
                #    column_name = "Perc{}_postop".format(i)
                #   value = data.Perc_postop[i]

                #  if not pd.isna(value):  # Überprüfen, ob der Wert nicht NaN ist
                #    DBSleft.setText(str(value))
                # else:
                #    DBSleft.clear()  # Leerfeld, wenn der Wert NaN ist oder leer

                # previously
                #    DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 1).widget()
                #    DBSleft.setText(str(row["Perc1_postop"]))
                #    DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 2).widget()
                #    DBSleft.setText(str(row["Perc2_postop"]))
                #    DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 3).widget()
                #    DBSleft.setText(str(row["Perc3_postop"]))
                #    DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 4).widget()
                #    DBSleft.setText(str(row["Perc4_postop"]))
                #    DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 5).widget()
                #    DBSleft.setText(str(row["Perc5_postop"]))
                #    DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 6).widget()
                #    DBSleft.setText(str(row["Perc6_postop"]))
                #    DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 7).widget()
                #    DBSleft.setText(str(row["Perc7_postop"]))
                #    DBSleft = self.DBSpercentageLeft.itemAtPosition(0, 8).widget()
                #    DBSleft.setText(str(row["Perc8_postop"]))

                # Populating right DBS fields
                for i in range(9, 17):
                    DBSright = self.DBSpercentageRight.itemAtPosition(0, i - 8).widget()
                    column_name = "Perc{}_postop".format(i)

                    if column_name in data.d.columns:
                        value = data.d.loc[data.d.index[0], column_name]
                        if not pd.isna(value):  # Überprüfen, ob der Wert nicht NaN ist
                            DBSright.setText(str(value))
                        else:
                            DBSright.clear()
                    else:
                        DBSright.clear()  # Leerfeld, wenn der Wert NaN ist oder leer
        # for i in range(8, 16): had index issues with label not being displayed for rows, instead data of perc1+9 was
        #    DBSright = self.DBSpercentageRight.itemAtPosition(0, i - 8).widget()
        #   column_name = "Perc{}_postop".format(i)
        #  value = data.Perc_postop[i]

        # if not pd.isna(value):  # Überprüfen, ob der Wert nicht NaN ist
        #    DBSright.setText(str(value))
        # else:
        #    DBSright.clear()  # Leerfeld, wenn der Wert NaN ist oder leer

        # previously
        #    DBSright = self.DBSpercentageRight.itemAtPosition(0, 1).widget()
        #    DBSright.setText(str(row["Perc9_postop"]))
        #    DBSright = self.DBSpercentageRight.itemAtPosition(0, 2).widget()
        #    DBSright.setText(str(row["Perc10_postop"]))
        #    DBSright = self.DBSpercentageRight.itemAtPosition(0, 3).widget()
        #    DBSright.setText(str(row["Perc11_postop"]))
        #    DBSright = self.DBSpercentageRight.itemAtPosition(0, 4).widget()
        #    DBSright.setText(str(row["Perc12_postop"]))
        #    DBSright = self.DBSpercentageRight.itemAtPosition(0, 5).widget()
        #    DBSright.setText(str(row["Perc13_postop"]))
        #    DBSright = self.DBSpercentageRight.itemAtPosition(0, 6).widget()
        #    DBSright.setText(str(row["Perc14_postop"]))
        #    DBSright = self.DBSpercentageRight.itemAtPosition(0, 7).widget()
        #    DBSright.setText(str(row["Perc15_postop"]))
        #    DBSright = self.DBSpercentageRight.itemAtPosition(0, 8).widget()
        #    DBSright.setText(str(row["Perc16_postop"]))

        # == Amplitude,Pulse;Frequency == Bottom right #
        ################################################
        # LE: Edited code to show empty fields when 'nan'
        # setting left
        # Get a reference to the Amplitude widget for the left side
        amplitudeLeftWidget = self.gridDBSsettings.itemAtPosition(1, 1).widget()
        amplitudeLeftWidget.setText(str(data.AmplL_postop) if not pd.isnull(data.AmplL_postop) else "")

        pulseWidthLeftWidget = self.gridDBSsettings.itemAtPosition(1, 2).widget()
        pulseWidthLeftWidget.setText(str(data.PWL_postop) if not pd.isnull(data.PWL_postop) else "")

        frequencyLeftWidget = self.gridDBSsettings.itemAtPosition(1, 3).widget()
        frequencyLeftWidget.setText(str(data.FreqL_postop) if not pd.isnull(data.FreqL_postop) else "")

        # setting right
        # Get a reference to the Amplitude widget for the right side
        amplitudeRightWidget = self.gridDBSsettings.itemAtPosition(2, 1).widget()
        amplitudeRightWidget.setText(str(data.AmplR_postop) if not pd.isnull(data.AmplR_postop) else "")

        pulseWidthRightWidget = self.gridDBSsettings.itemAtPosition(2, 2).widget()
        pulseWidthRightWidget.setText(str(data.PWR_postop) if not pd.isnull(data.PWR_postop) else "")

        frequencyRightWidget = self.gridDBSsettings.itemAtPosition(2, 3).widget()
        frequencyRightWidget.setText(str(data.FreqR_postop) if not pd.isnull(data.FreqR_postop) else "")


    # LE: Empty fields where writing out 'nan'
    # setting left
    # Get a reference to the Amplitude widget for the left side
    #        amplitudeLeftWidget = self.gridDBSsettings.itemAtPosition(1, 1).widget()
    #        amplitudeLeftWidget.setText(str(data.AmplL_postop))

    #        pulseWidthLeftWidget = self.gridDBSsettings.itemAtPosition(1, 2).widget()
    #        pulseWidthLeftWidget.setText(str(data.PWL_postop))

    #        frequencyLeftWidget = self.gridDBSsettings.itemAtPosition(1, 3).widget()
    #        frequencyLeftWidget.setText(str(data.FreqL_postop))
    # setting right
    # Get a reference to the Amplitude widget for the right side
    #        amplitudeRightWidget = self.gridDBSsettings.itemAtPosition(2, 1).widget()
    #        amplitudeRightWidget.setText(str(data.AmplR_postop))

    #        pulseWidthRightWidget = self.gridDBSsettings.itemAtPosition(2, 2).widget()
    #        pulseWidthRightWidget.setText(str(data.PWR_postop))

    #        frequencyRightWidget = self.gridDBSsettings.itemAtPosition(2, 3).widget()
    #        frequencyRightWidget.setText(str(data.FreqR_postop))

    # ==Reason== Enter Data field, ComboBox #      TODO: Attribute Error, run fails when different reason selected
    def update_context(self, data=None):
        """updates the context according to what was elected in the ComboBox"""
        if data is None:
            data = Postoperative_data(r'C:\Users\toast\OneDrive\Desktop\GitHub\dbsPatients\data\postoperative.csv',
                                      1399948)
        #               data = self.Postoperative_data(Data)
        if self.lineEditreason.currentText() == 'Please select':
            pass
        elif self.lineEditreason.currentText() == 'Enter data':
            Output.open_input_dialog_postoperative(self)
            data_frame = General.import_dataframe(f"{self.date}.csv", separator_csv=',')
            subj_details = General.read_current_subj()

            match = re.search(r'^(pre|intra|post)op', self.date)
            data_frame.loc[len(data_frame), ['ID', 'PID', 'Reason_{}'.format(match.group())]] = [subj_details.id[0],
                                                                                                 subj_details.pid[0],
                                                                                                 self.postoperative_date]
            data_frame = data_frame.replace(['nan', ''], [np.nan, np.nan])
            data_frame = data_frame.applymap(lambda x: str(x).replace(';', ' -'))
            data_frame.to_csv(os.path.join(FILEDIR, f"{self.date}.csv"), index=False)

            self.lineEditreason.clear()
            self.fill_combobox()
            self.read_content_csv()
        else:
            self.postoperative_date = self.lineEditreason.currentText()
            #            self.update_context()
            return

    # ====================   Defines actions when buttons are pressed, saving part   ====================

    @QtCore.pyqtSlot()
    def on_clickedMedication(self):
        """shows the medication dialog when button is pressed; former implementation with creating GUI was replaced with
        show/hide GUI which is initiated at beginning"""
        self.dialog_medication.show()

    @QtCore.pyqtSlot()
    def onClickedSaveReturn(self, pds=None):
        """
        Saves the data passed into the GUI form and returns to previous Window.

        Args:
            pds: dataframe to safe??

        Returns: None

        """

        current_subj = General.read_current_subj()
        subject_id = current_subj['id'][0]
        df_general = Clean.extract_subject_data(subject_id)
        match = re.search(r'^(pre|intra|post)op', self.date)

        # read general data so that pre-/intra- and postoperative share these
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

        # Now extract the changed data from the GUI

        # == Important Dates == upper left #
        ####################################
        df_subj['Admission_NCh_{}'.format(match.group())] = self.lineEditAdmission_Nch.text()
        df_subj['Admission_NR_{}'.format(match.group())] = self.lineEditAdmission_NR.text()
        df_subj['Dismissal_NCh_{}'.format(match.group())] = self.lineEditDismission_Nch.text()
        df_subj['Dismissal_NR_{}'.format(match.group())] = self.lineEditDismission_NR.text()
        df_subj['Surgery_Date_{}'.format(match.group())] = self.lineEditSurgery.text()
        df_subj['Last_Revision_postop'] = self.lineEditLast_Revision.text()
        df_subj['Outpatient_Contact_postop'] = self.lineEditOutpatient_Contact.text()

        # == Reason == upper right #
        ############################
        # Adverse Events textfield
        df_subj['AE_{}'.format(match.group())] = self.lineEditAdverse_Event.text()

        # == Tests == middle right #
        ############################
        df_subj['UPDRS1_{}'.format(match.group())] = self.lineEditUPDRSI.text()
        df_subj['UPDRS4_{}'.format(match.group())] = self.lineEditUPDRSIV.text()
        df_subj['TSS_postop'] = self.lineEditTSS.text()
        df_subj['CGIG_patient_postop'] = self.lineEditCGICPat.text()
        df_subj['CGIG_clinician_cargiver_postop'] = self.lineEditCGICClinician.text()
        df_subj["UPDRSon_postop"] = self.lineEditUPDRSON.text()
        df_subj["UPDRSII_postop"] = self.lineEditUPDRSII.text()
        df_subj["HRUQ_postop"] = self.lineEditHRUQ.text()
        df_subj["MoCa_postop"] = self.lineEditMoCa.text()
        df_subj["MMST_postop"] = self.lineEditMMST.text()
        df_subj["BDI2_postop"] = self.lineEditBDIII.text()
        df_subj["NMSQ_postop"] = self.lineEditNMSQ.text()
        df_subj["UPDRSOff_postop"] = self.lineEditUPDRSOff.text()
        df_subj["H&Y_postop"] = self.lineEditHY.text()
        df_subj["EQ5D_postop"] = self.lineEditEQ5D.text()
        df_subj["DemTect_postop"] = self.lineEditDemTect.text()
        df_subj["PDQ8_postop"] = self.lineEditPDQ8.text()
        df_subj["PDQ39_postop"] = self.lineEditPDQ39.text()
        df_subj["S&E_postop"] = self.lineEditSE.text()
        df_subj["UDDRSOn_postop"] = self.lineEditUDDRSOn.text()
        df_subj["TRSon_postop"] = self.lineEditTRSOn.text()
        df_subj["UDDRSoff_postop"] = self.lineEditUDDRSOff.text()
        df_subj["TRSoff_postop"] = self.lineEditTRSOff.text()

        # ==Report== Checkboxes, middle left #
        ######################################
        checkbox_cols = [("ReportNeurCheck", "Report_File_NCh_postop"),
                         ("ReportNeurosurgeryCheck", "Report_File_NR_postop"),
                         ("PatProgrammerCheck", "Using_Programmer_postop"), ("PostopCTCheck", "CTscan_postop"),
                         ("BatteryReplacementCheck", "Battery_Replacement_postop"),
                         ("PlannedVisitCheck", "Planned_Visit_postop"), ("QualiPaCheck", "Qualipa_Visit_postop")]

        for checkbox, col_name in checkbox_cols:
            if getattr(self, checkbox).isChecked():
                df_subj[col_name] = 1
            else:
                df_subj[col_name] = 0

            # ==DBS settings after dismissal==, bottom left # LE: Added lines to safe data
            #################################################
        left_data = []
        right_data = []

        for j in range(1, 9):
            left_line_edit = self.DBSpercentageLeft.itemAtPosition(0, j).widget()
            right_line_edit = self.DBSpercentageRight.itemAtPosition(0, j).widget()
            left_data.append(left_line_edit.text())
            right_data.append(right_line_edit.text())

        df_subj['Perc1_postop'] = left_data[0]
        df_subj['Perc2_postop'] = left_data[1]
        df_subj['Perc3_postop'] = left_data[2]
        df_subj['Perc4_postop'] = left_data[3]
        df_subj['Perc5_postop'] = left_data[4]
        df_subj['Perc6_postop'] = left_data[5]
        df_subj['Perc7_postop'] = left_data[6]
        df_subj['Perc8_postop'] = left_data[7]

        df_subj['Perc9_postop'] = right_data[0]
        df_subj['Perc10_postop'] = right_data[1]
        df_subj['Perc11_postop'] = right_data[2]
        df_subj['Perc12_postop'] = right_data[3]
        df_subj['Perc13_postop'] = right_data[4]
        df_subj['Perc14_postop'] = right_data[5]
        df_subj['Perc15_postop'] = right_data[6]
        df_subj['Perc16_postop'] = right_data[7]

        # == Amplitude,Pulse,Frequency==, bottom right # LE: Added lines to safe data
        ################################################
        # Extract data from QLineEdit-Widgets in gridDBSsettings-Layout
        left_amplitude = self.gridDBSsettings.itemAtPosition(1, 1).widget().text()
        right_amplitude = self.gridDBSsettings.itemAtPosition(2, 1).widget().text()

        left_pulse_width = self.gridDBSsettings.itemAtPosition(1, 2).widget().text()
        right_pulse_width = self.gridDBSsettings.itemAtPosition(2, 2).widget().text()

        left_frequency = self.gridDBSsettings.itemAtPosition(1, 3).widget().text()
        right_frequency = self.gridDBSsettings.itemAtPosition(2, 3).widget().text()

        df_subj['AmplL_postop'] = left_amplitude
        df_subj['AmplR_postop'] = right_amplitude

        df_subj['PWL_postop'] = left_pulse_width
        df_subj['PWR_postop'] = right_pulse_width

        df_subj['FreqL_postop'] = left_frequency
        df_subj['FreqR_postop'] = right_frequency

        # Incorporate the [df_subj] dataframe into the entire dataset and save as csv
        try:
            idx2replace = df.index[df['ID'] == subj_id][0]
            df.loc[idx2replace, :] = df_subj
            df = df.replace(['nan', ''], [np.nan, np.nan])
        except IndexError:
            df_subj = pd.DataFrame(df_subj, index=[df.index.shape[0]])
            df = pd.concat([df, df_subj], ignore_index=True)
            df = df.replace('nan', np.nan)

        df.to_csv(os.path.join(FILEDIR, "postoperative.csv"), index=False)

        # LE: replaced code due to issues with pandas
        #   try:
        #     idx2replace = df[df['ID'] == subj_id].index[0]
        #  except IndexError:
        #  idx2replace = 0
        #  df.loc[idx2replace, :] = df_subj
        # df = df.replace(['nan', ''], [np.nan, np.nan])
        # df.to_csv(os.path.join(FILEDIR, "{}.csv".format(self.date)), index=False)

        self.close()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "test.txt",  # ?
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
    logger.debug(f"start app with {sys.argv}")
    app = QApplication(sys.argv)
    logger.debug("set widget")
    widget = QWidget
    logger.debug("start dialog")
    dlg = PostoperativeDialog()
    logger.debug("show dialog")
    dlg.show()
    logger.debug(f"app exited with {app.exec_()}")
    sys.exit(app.exec_())
