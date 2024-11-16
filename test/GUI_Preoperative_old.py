import sys
from PyQt5 import QtCore

from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QFileDialog, QWidget, QGridLayout, QLineEdit, QLabel, QComboBox, QPushButton

from GUI.GUImedication import MedicationDialog

textfield_width = 450


class PreoperativeDialog(QDialog):
    """Dialog to introduce all important information of preoperative patients."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.setWindowTitle('Preoperative Information')
        self.setGeometry(200, 100, 280, 170)
        self.move(550, 125)

        layout = QGridLayout(self)
        self.setLayout(layout)

        # Create one optionbox for the time being left
        self.optionbox1 = QGroupBox('General data')
        self.optionbox1Content = QVBoxLayout(self.optionbox1)
        layout.addWidget(self.optionbox1, 0, 0)

        self.subj_PID = QLabel('PID:\t\t')
        self.lineEditPID = QLineEdit()
        lay1 = QHBoxLayout()
        lay1.addWidget(self.subj_PID)
        lay1.addWidget(self.lineEditPID)
        lay1.addStretch()

        self.subj_ID = QLabel('ID:\t\t')
        self.lineEditID = QLineEdit()
        lay2 = QHBoxLayout()
        lay2.addWidget(self.subj_ID)
        lay2.addWidget(self.lineEditID)
        lay2.addStretch()

        self.subj_gender = QLabel('Gender:\t\t')
        self.lineEditGender = QComboBox()
        self.lineEditGender.addItems(['female', 'male', 'diverse'])
        self.lineEditGender.setFixedHeight(20)
        lay3 = QHBoxLayout()
        lay3.addWidget(self.subj_gender)
        lay3.addWidget(self.lineEditGender)
        lay3.addStretch()

        self.subj_diagnosis = QLabel('Diagnosis:\t')
        self.lineEditDiagnosis = QComboBox()
        self.lineEditDiagnosis.addItems(['Hypokinetic-rigid parkinson-syndrome (PD1)',
                                         'Tremordominant parkinson-syndrome(PD2)',
                                         'Mixed-type parkinson-syndrome (PD3)',
                                         'Dystonia (DT)',
                                         'Essential tremor (ET)',
                                         'Other'])

        self.lineEditDiagnosis.setFixedHeight(20)
        lay4 = QHBoxLayout()
        lay4.addWidget(self.subj_diagnosis)
        lay4.addWidget(self.lineEditDiagnosis)
        lay4.addStretch()

        self.subj_firstDiagnosed = QLabel('First Diagnosed:\t')
        self.lineEditfirstDiagnosed = QLineEdit()
        lay5 = QHBoxLayout()
        lay5.addWidget(self.subj_firstDiagnosed)
        lay5.addWidget(self.lineEditfirstDiagnosed)
        lay5.addStretch()

        self.optionbox1Content.addLayout(lay1)
        self.optionbox1Content.addLayout(lay2)
        self.optionbox1Content.addLayout(lay3)
        self.optionbox1Content.addLayout(lay4)
        self.optionbox1Content.addLayout(lay5)
        self.optionbox1.setLayout(self.optionbox1Content)

        # Create one optionbox for the time being right
        self.optionbox2 = QGroupBox('Reports')
        self.optionbox2Content = QVBoxLayout(self.optionbox2)
        layout.addWidget(self.optionbox2, 0, 1)

        self.subj_Admission = QLabel('Admission:\t')
        self.lineEditAdmission = QLineEdit()
        lay6 = QHBoxLayout()
        lay6.addWidget(self.subj_Admission)
        lay6.addWidget(self.lineEditAdmission)
        lay6.addStretch()

        self.subj_Dismissal = QLabel('Dismissal:\t\t')
        self.lineEditDismissal = QLineEdit()
        lay7 = QHBoxLayout()
        lay7.addWidget(self.subj_Dismissal)
        lay7.addWidget(self.lineEditDismissal)
        lay7.addStretch()

        self.subj_Report = QLabel('Report:\t\t')
        self.lineEditReport = QLineEdit()
        lay8 = QHBoxLayout()
        lay8.addWidget(self.subj_Report)
        lay8.addWidget(self.lineEditReport)
        lay8.addStretch()

        self.subj_ReportPreop = QLabel('Report Preop:\t')
        self.lineEditReportPreop = QLineEdit()
        lay9 = QHBoxLayout()
        lay9.addWidget(self.subj_ReportPreop)
        lay9.addWidget(self.lineEditReportPreop)
        lay9.addStretch()

        self.optionbox2Content.addLayout(lay6)
        self.optionbox2Content.addLayout(lay7)
        self.optionbox2Content.addLayout(lay8)
        self.optionbox2Content.addLayout(lay9)
        self.optionbox2.setLayout(self.optionbox2Content)

        # optionbox3

        self.optionbox3 = QGroupBox('Files/Scans')
        self.optionbox3Content = QVBoxLayout(self.optionbox3)
        layout.addWidget(self.optionbox3, 0, 2)

        self.subj_Video = QLabel('Video:\t')
        self.lineEditVideo = QLineEdit()
        lay10 = QHBoxLayout()
        lay10.addWidget(self.subj_Video)
        lay10.addWidget(self.lineEditVideo)
        lay10.addStretch()

        self.subj_VideoFile = QLabel('Video File:')
        self.lineEditVideoFile = QLineEdit()
        lay11 = QHBoxLayout()
        lay11.addWidget(self.subj_VideoFile)
        lay11.addWidget(self.lineEditVideoFile)
        lay11.addStretch()

        self.subj_MRT = QLabel('MRT:\t')
        self.lineEditMRT = QLineEdit()
        lay12 = QHBoxLayout()
        lay12.addWidget(self.subj_MRT)
        lay12.addWidget(self.lineEditMRT)
        lay12.addStretch()

        self.optionbox3Content.addLayout(lay10)
        self.optionbox3Content.addLayout(lay11)
        self.optionbox3Content.addLayout(lay12)
        self.optionbox3.setLayout(self.optionbox3Content)

        #optionbox 4
        self.optionbox4 = QGroupBox('DBS Decision')
        self.optionbox4Content = QVBoxLayout(self.optionbox4)
        layout.addWidget(self.optionbox4, 1, 0)

        self.subj_OutpatContact = QLabel('Outpat Contact:\t')
        self.lineEditOutpatContact = QLineEdit()
        lay13 = QHBoxLayout()
        lay13.addWidget(self.subj_OutpatContact)
        lay13.addWidget(self.lineEditOutpatContact)
        lay13.addStretch()

        self.subj_nch = QLabel('nch:\t\t')
        self.lineEditnch = QLineEdit()
        lay14 = QHBoxLayout()
        lay14.addWidget(self.subj_nch)
        lay14.addWidget(self.lineEditnch)
        lay14.addStretch()

        self.subj_Briefing = QLabel('Briefing:\t\t')
        self.lineEditBriefing = QLineEdit()
        lay15 = QHBoxLayout()
        lay15.addWidget(self.subj_Briefing)
        lay15.addWidget(self.lineEditBriefing)
        lay15.addStretch()

        self.subj_BriefingDoctor = QLabel('Briefing Doctor:\t')
        self.lineEditBriefingDoctor = QLineEdit()
        lay16 = QHBoxLayout()
        lay16.addWidget(self.subj_BriefingDoctor)
        lay16.addWidget(self.lineEditBriefingDoctor)
        lay16.addStretch()

        self.subj_DBSConference = QLabel('DBS Conference:\t')
        self.lineEditDBSConference = QLineEdit()
        lay17 = QHBoxLayout()
        lay17.addWidget(self.subj_DBSConference)
        lay17.addWidget(self.lineEditDBSConference)
        lay17.addStretch()

        self.subj_DecisionDBS = QLabel('Decision DBS:\t')
        self.lineEditDecisionDBS = QLineEdit()
        lay18 = QHBoxLayout()
        lay18.addWidget(self.subj_DecisionDBS)
        lay18.addWidget(self.lineEditDecisionDBS)
        lay18.addStretch()

        self.optionbox4Content.addLayout(lay13)
        self.optionbox4Content.addLayout(lay14)
        self.optionbox4Content.addLayout(lay15)
        self.optionbox4Content.addLayout(lay16)
        self.optionbox4Content.addLayout(lay17)
        self.optionbox4Content.addLayout(lay18)
        self.optionbox4.setLayout(self.optionbox4Content)

        # optionbox 6
        self.optionbox6 = QGroupBox('Tests')
        self.optionbox6Content = QVBoxLayout(self.optionbox6)
        layout.addWidget(self.optionbox6, 1, 1)

        self.subj_BDI2 = QLabel('BDI2:\t\t')
        self.lineEditBDI2 = QLineEdit()
        lay20 = QHBoxLayout()
        lay20.addWidget(self.subj_BDI2)
        lay20.addWidget(self.lineEditBDI2)
        lay20.addStretch()

        self.subj_DemTect = QLabel('DemTect:\t\t')
        self.lineEditDemTect = QLineEdit()
        lay21 = QHBoxLayout()
        lay21.addWidget(self.subj_DemTect)
        lay21.addWidget(self.lineEditDemTect)
        lay21.addStretch()

        self.subj_EQ5D = QLabel('EQ5D:\t\t')
        self.lineEditEQ5D = QLineEdit()
        lay22 = QHBoxLayout()
        lay22.addWidget(self.subj_EQ5D)
        lay22.addWidget(self.lineEditEQ5D)
        lay22.addStretch()

        self.subj_fpcit_spect = QLabel('fpcit_spect:\t')
        self.lineEditfpcit_spect = QLineEdit()
        lay23 = QHBoxLayout()
        lay23.addWidget(self.subj_fpcit_spect)
        lay23.addWidget(self.lineEditfpcit_spect)
        lay23.addStretch()

        self.subj_HRUQ = QLabel('HRUQ:\t\t')
        self.lineEditHRUQ = QLineEdit()
        lay24 = QHBoxLayout()
        lay24.addWidget(self.subj_HRUQ)
        lay24.addWidget(self.lineEditHRUQ)
        lay24.addStretch()

        self.subj_HYOn = QLabel('H&Y On:\t\t')
        self.lineEditHYOn = QLineEdit()
        lay25 = QHBoxLayout()
        lay25.addWidget(self.subj_HYOn)
        lay25.addWidget(self.lineEditHYOn)
        lay25.addStretch()

        self.subj_HYOff = QLabel('H&Y Off:\t\t')
        self.lineEditHYOff = QLineEdit()
        lay26 = QHBoxLayout()
        lay26.addWidget(self.subj_HYOff)
        lay26.addWidget(self.lineEditHYOff)
        lay26.addStretch()

        self.subj_MMST = QLabel('MMST:\t\t')
        self.lineEditMMST = QLineEdit()
        lay27 = QHBoxLayout()
        lay27.addWidget(self.subj_MMST)
        lay27.addWidget(self.lineEditMMST)
        lay27.addStretch()

        self.subj_MoCa = QLabel('MoCa:\t\t')
        self.lineEditMoCa = QLineEdit()
        lay28 = QHBoxLayout()
        lay28.addWidget(self.subj_MoCa)
        lay28.addWidget(self.lineEditMoCa)
        lay28.addStretch()

        self.subj_NMSQ = QLabel('NMSQ:\t\t')
        self.lineEditNMSQ = QLineEdit()
        lay29 = QHBoxLayout()
        lay29.addWidget(self.subj_NMSQ)
        lay29.addWidget(self.lineEditNMSQ)
        lay29.addStretch()

        self.subj_PDQ8 = QLabel('PDQ8:\t\t')
        self.lineEditPDQ8 = QLineEdit()
        lay30 = QHBoxLayout()
        lay30.addWidget(self.subj_PDQ8)
        lay30.addWidget(self.lineEditPDQ8)
        lay30.addStretch()

        self.subj_PDQ39 = QLabel('PDQ39:\t\t')
        self.lineEditPDQ39 = QLineEdit()
        lay31 = QHBoxLayout()
        lay31.addWidget(self.subj_PDQ39)
        lay31.addWidget(self.lineEditPDQ39)
        lay31.addStretch()

        self.subj_SE = QLabel('S&E:\t\t')
        self.lineEditSE = QLineEdit()
        lay32 = QHBoxLayout()
        lay32.addWidget(self.subj_SE)
        lay32.addWidget(self.lineEditSE)
        lay32.addStretch()

        self.subj_UPDRSII = QLabel('UPDRS II:\t')
        self.lineEditUPDRSII = QLineEdit()
        lay33 = QHBoxLayout()
        lay33.addWidget(self.subj_UPDRSII)
        lay33.addWidget(self.lineEditUPDRSII)
        lay33.addStretch()

        self.subj_UPDRSIIIOn = QLabel('UPDRS III On:\t')
        self.lineEditUPDRSIIIOn = QLineEdit()
        lay34 = QHBoxLayout()
        lay34.addWidget(self.subj_UPDRSIIIOn)
        lay34.addWidget(self.lineEditUPDRSIIIOn)
        lay34.addStretch()

        self.subj_UPDRSIIIOff = QLabel('UPDRS III Off:\t')
        self.lineEditUPDRSIIIOff = QLineEdit()
        lay35 = QHBoxLayout()
        lay35.addWidget(self.subj_UPDRSIIIOff)
        lay35.addWidget(self.lineEditUPDRSIIIOff)
        lay35.addStretch()


        self.optionbox6Content.addLayout(lay20)
        self.optionbox6Content.addLayout(lay21)
        self.optionbox6Content.addLayout(lay22)
        self.optionbox6Content.addLayout(lay23)
        self.optionbox6Content.addLayout(lay24)
        self.optionbox6Content.addLayout(lay25)
        self.optionbox6Content.addLayout(lay26)
        self.optionbox6Content.addLayout(lay27)
        self.optionbox6Content.addLayout(lay28)
        self.optionbox6Content.addLayout(lay29)
        self.optionbox6Content.addLayout(lay30)
        self.optionbox6Content.addLayout(lay31)
        self.optionbox6Content.addLayout(lay32)
        self.optionbox6Content.addLayout(lay33)
        self.optionbox6Content.addLayout(lay34)
        self.optionbox6Content.addLayout(lay35)
        self.optionbox6.setLayout(self.optionbox6Content)

        # optionbox 5
        self.optionbox5 = QGroupBox('LEDD')
        self.optionbox5Content = QVBoxLayout(self.optionbox5)
        layout.addWidget(self.optionbox5, 3, 0)

        self.subj_LEDD = QLabel('LEDD:\t\t')
        self.lineEditLEDD = QLineEdit()
        lay19 = QHBoxLayout()
        lay19.addWidget(self.subj_LEDD)
        lay19.addWidget(self.lineEditLEDD)
        lay19.addStretch()

        self.optionbox5Content.addLayout(lay19)
        self.optionbox5.setLayout(self.optionbox5Content)

        # optionbox 7
        self.optionbox7 = QGroupBox('Notes')
        self.optionbox7Content = QVBoxLayout(self.optionbox7)
        layout.addWidget(self.optionbox7, 3, 1)

        self.subj_Notes = QLabel('Notes:\t\t')
        self.lineEditNotes = QLineEdit()
        self.lineEditNotes.setFixedWidth(300)
        lay36 = QHBoxLayout()
        lay36.addWidget(self.subj_Notes)
        lay36.addWidget(self.lineEditNotes)
        lay36.addStretch()

        self.optionbox7Content.addLayout(lay36)
        self.optionbox7.setLayout(self.optionbox7Content)

        # buttons

        self.button_openGUI_Medication = QPushButton('Open GUI \nMedication')
        self.button_openGUI_Medication.setText("Medication")
        self.button_openGUI_Medication.setCheckable(True)

        self.button_save = QPushButton('Save')
        self.button_save.clicked.connect(self.onClickedSaveReturn)

        hlay_bottom = QHBoxLayout()
        hlay_bottom.addStretch(2)
        hlay_bottom.addWidget(self.button_openGUI_Medication)
        hlay_bottom.addWidget(self.button_save)
        hlay_bottom.addStretch(1)

        layout.addLayout(hlay_bottom, 4, 0, 1, 3)


    # In the next lines, actions are defined when Buttons are pressed
    @QtCore.pyqtSlot()

    def on_click(self):
        if self.button_openGUI_Medication.isChecked():  # selects three different options available
            dialog = MedicationDialog(parent=self)
        self.hide()
        if dialog.exec():
            pass
        self.show()

    def onClickedSaveReturn(self):
        print('Done!')
        self.hide()

        #self.saveFileDialog()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "test.txt", "All Files(*)",
                                                  options=options)
        print(fileName)

    # for opening
    def open_dialog_box(self):
        option = QFileDialog.Options()
        # first parameter is self; second is the Window Title, third title is Default File Name, fourth is FileType,
        # fifth is options
        file = QFileDialog.getOpenFileName(self, "Save File Window Title", "default.txt", "All Files (*)",
                                           options=option)
        print(file)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = PreoperativeDialog()
    dlg.show()
    sys.exit(app.exec_())
