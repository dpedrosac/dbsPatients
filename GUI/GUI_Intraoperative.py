#!/usr/bin/env python3
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QGroupBox,  QSpacerItem, QSizePolicy, \
    QHBoxLayout, QWidget, QGridLayout, QLineEdit, QLabel, QListWidget, QCheckBox
from GUI.GUImedication import MedicationDialog


class IntraoperativeDialog(QDialog):
    """Dialog to introduce all important information of intraoperative patients. """

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        # ====================    Create General Layout      ====================
        self.setWindowTitle('Please insert the data from the intraoperative patient contact ...')
        self.setGeometry(200, 100, 280, 170)
        self.move(400, 100)
        self.date = 'intraoperative'  # defines the date at which data are taken from/saved at

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # ====================    Optionbox (1) left upper corner      ====================
        self.optionbox1 = QGroupBox('Admission and Dimission dates')
        self.optionbox1Content = QVBoxLayout(self.optionbox1)
        layout_general.addWidget(self.optionbox1, 0, 0)

        self.AdmNCh = QLabel('Admission Neurosurgery (dd/mm/yyyy):\t')
        self.lineEditAdmNCh = QLineEdit()
        self.AdmNeurLabel = QLabel('Admission Neurology (dd/mm/yyyy):\t')
        self.lineEditAdmNeur = QLineEdit()
        self.DismNeurLabel = QLabel('Dismission Neurology (dd/mm/yyyy):\t')
        self.lineEditDismNeur = QLineEdit()
        self.DismNCh = QLabel('Dismission Neurosurgery (dd/mm/yyyy):\t')
        self.lineEditDismNCh = QLineEdit()

        box1line1 = QHBoxLayout()
        box1line1.addWidget(self.AdmNCh)
        box1line1.addWidget(self.lineEditAdmNCh)
        box1line1.addStretch()

        box1line2 = QHBoxLayout()
        box1line2.addWidget(self.AdmNeurLabel)
        box1line2.addWidget(self.lineEditAdmNeur)
        box1line2.addStretch()

        box1line3 = QHBoxLayout()
        box1line3.addWidget(self.DismNeurLabel)
        box1line3.addWidget(self.lineEditDismNeur)
        box1line3.addStretch()

        box1line4 = QHBoxLayout()
        box1line4.addWidget(self.DismNCh)
        box1line4.addWidget(self.lineEditDismNCh)
        box1line4.addStretch()

        self.optionbox1Content.addLayout(box1line1)
        self.optionbox1Content.addLayout(box1line2)
        self.optionbox1Content.addLayout(box1line3)
        self.optionbox1Content.addLayout(box1line4)
        self.optionbox1.setLayout(self.optionbox1Content)

        # ====================    Optionbox (2) right upper corner      ====================
        self.optionbox2 = QGroupBox('Surgery')
        self.optionbox2Content = QVBoxLayout(self.optionbox2)
        layout_general.addWidget(self.optionbox2, 0, 1)

        self.SurgeryDate = QLabel('Surgery Date \n(dd/mm/yyyy):\t')
        self.lineEditSurgeryDate = QLineEdit()

        box2line1 = QHBoxLayout()
        box2line1.addWidget(self.SurgeryDate)
        box2line1.addWidget(self.lineEditSurgeryDate)
        # box2line1.addStretch()

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

        # ====================    Optionbox (3) upper middle left      ====================
        self.optionbox3 = QGroupBox('Intraoperative')
        self.optionbox3Content = QVBoxLayout(self.optionbox3)
        layout_general.addWidget(self.optionbox3, 1, 0)

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

        # ====================    Optionbox (4) upper middle right      ====================
        self.optionbox4 = QGroupBox('System Information')
        self.optionbox4Content = QVBoxLayout(self.optionbox4)
        layout_general.addWidget(self.optionbox4, 1, 1)

        self.LeadImplantedLabel = QLabel('Lead:\t\t')
        self.LeadImplantedList = QListWidget()
        self.LeadImplantedLabel.setAlignment(QtCore.Qt.AlignTop)
        self.LeadImplantedList.show()
        ls = ['Medtronic 3389', 'Medtronic 3389', 'Boston Scientific 2202-30/-45',
              'St. Jude 6146/6147/6148/6149', 'Other']
        [self.LeadImplantedList.addItem(k) for k in ls]

        box4line1 = QHBoxLayout()
        box4line1.addWidget(self.LeadImplantedLabel)
        box4line1.addWidget(self.LeadImplantedList)

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

        # ====================    Optionbox (5) lower middle left      ====================
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
        self.optionbox5Content.addLayout(self.GridCoordinatesRight)
        self.optionbox5Content.addStretch()

        # ====================    Optionbox (6) lower middle right      ====================
        self.optionbox6 = QGroupBox('Activation')
        self.optionbox6Content = QVBoxLayout(self.optionbox6)
        layout_general.addWidget(self.optionbox6, 2, 1)

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

        # ====================    Optionbox (7) lower left      ====================
        self.optionbox7 = QGroupBox('DBS settings after dismissal')
        self.optionbox7Content = QVBoxLayout(self.optionbox7)
        layout_general.addWidget(self.optionbox7, 3, 0)

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

        self.optionbox7Content.addStretch(2)
        self.optionbox7Content.addLayout(self.DBSpercentageLeft)
        self.optionbox7Content.addLayout(self.DBSpercentageRight)

        # ====================    Optionbox (8) lower right      ====================
        self.optionbox8 = QGroupBox('Amplitude, Pulse and Frequency')
        self.optionbox8Content = QVBoxLayout(self.optionbox8)
        layout_general.addWidget(self.optionbox8, 3, 1)

        self.gridDBSsettings = QGridLayout()
        self.gridDBSsettings.addWidget(QLabel('Left:\t'), 1, 0)
        self.gridDBSsettings.addWidget(QLabel('Right:\t'), 2, 0)
        self.gridDBSsettings.addWidget(QLabel('Amplitude [mA]'), 0, 1)
        self.gridDBSsettings.addWidget(QLabel('Pulse Width [µs]:'), 0, 2)
        self.gridDBSsettings.addWidget(QLabel('Frequency [Hz]'), 0, 3)

        for i in range(1, 3):
            for j in range(1, 4):
                self.gridDBSsettings.addWidget(QLineEdit(), i, j)
        self.optionbox8Content.addLayout(self.gridDBSsettings)

        self.optionbox8.setLayout(self.optionbox8Content)

        # ====================   Adds buttons at the bottom of the GUI      ====================
        self.ButtonEnterMedication = QPushButton('Open GUI \nMedication')
        self.button_save = QPushButton('Save and \nReturn')

        hlay_bottom = QHBoxLayout()
        hlay_bottom.addStretch(5)
        hlay_bottom.addWidget(self.ButtonEnterMedication)
        hlay_bottom.addWidget(self.button_save)
        hlay_bottom.addStretch(1)
        layout_general.addLayout(hlay_bottom, 4, 0, 1, 3)

        # ====================   Actions when buttons are pressed      ====================
        self.ButtonEnterMedication.clicked.connect(self.onClickedMedication)
        self.button_save.clicked.connect(self.onClickedSaveReturn)

    # ====================   Defines actions when buttons are pressed      ====================
    @QtCore.pyqtSlot()
    def onClickedMedication(self):
        """shows the medication dialog when button is pressed"""
        dialog = MedicationDialog(visit=self.date, parent=self)
        self.hide()
        if dialog.exec():
            pass
        self.show()

    def onClickedSaveReturn(self):
        """closes this GUI and returns to calling (main) GUI"""
        print('Done!')
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = IntraoperativeDialog()
    dlg.show()
    sys.exit(app.exec_())
