#!/usr/bin/env python3
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QWidget, QGridLayout, QLineEdit, QLabel, QCheckBox
from GUI.GUImedication import MedicationDialog
from utils.helper_functions import General, Content


class PreoperativeDialog(QDialog):
    """Dialog to introduce all important information of preoperative data ('indication check')"""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)

        self.date = 'preoperative'  # defines the date at which data are taken from/saved at
        subj_details = General.read_current_subj()
        # data_temp = General.get_data_subject(self.date, subj_details.pid[0])
        General.synchronize_data_with_general(self.date, subj_details.id[0], messagebox=False)

        # ====================    Create General Layout      ====================
        self.setWindowTitle('Please enter preoperative data (PID: {})'.format(str(int(subj_details.pid))))
        self.setGeometry(200, 100, 280, 170)
        self.move(400, 100)
        textwidth = 300
        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # ====================    Optionbox (1) upper      ====================
        self.optionbox1 = QGroupBox('Diagnosis and indication check')
        self.optionbox1Content = QVBoxLayout(self.optionbox1)
        layout_general.addWidget(self.optionbox1, 0, 0)

        self.FirstDiagnosed = QLabel('First diagnosed:\t\t')
        self.lineEditFirstDiagnosed = QLineEdit()
        self.lineEditFirstDiagnosed.setFixedWidth(textwidth)
        self.AdmNeurIndCheckLabel = QLabel('Admission (dd/mm/yyyy):\t')
        self.lineEditAdmNeurIndCheck = QLineEdit()
        self.lineEditAdmNeurIndCheck.setFixedWidth(textwidth)
        self.DismNeurIndCheck = QLabel('Dismission (dd/mm/yyyy):\t')
        self.DismNeurIndCheckLabel = QLineEdit()
        self.DismNeurIndCheckLabel.setFixedWidth(textwidth)
        self.OutpatientContact = QLabel('Outpatient contact (dd/mm/yyyy):\t\t')
        self.lineEditOutpatientContact = QLineEdit()
        self.lineEditOutpatientContact.setFixedWidth(textwidth)
        self.NChContact = QLabel('Neurosurgical contact (dd/mm/yyyy):\t')
        self.lineEditNChContact = QLineEdit()
        self.lineEditNChContact.setFixedWidth(textwidth)
        self.DBSconferenceDate = QLabel('DBS conference (dd/mm/yyyy):\t\t')
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

        # ====================    Optionbox (2) middle       ====================
        self.optionbox2 = QGroupBox('Reports and study participation:')
        self.optionbox2Content = QVBoxLayout(self.optionbox2)
        layout_general.addWidget(self.optionbox2, 1, 0)

        # TODO: Check Boxes should be aligned in the middle to match the text!
        self.VideoFile = QCheckBox()
        self.VideoFileLabel = QLabel('Report')
        self.VideoFileLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.MRIpreop = QCheckBox()
        self.MRIpreopLabel = QLabel('Decision for lead placement')
        self.MRIpreopLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.FPCITpreop = QCheckBox()
        self.FPCITpreopLabel = QLabel('Consent VERCISE DBS')
        self.FPCITpreopLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.ProtocolNeurCheck = QCheckBox()
        self.ProtocolNeurLabel = QLabel('In-/Exclusion criteria\n VERCISE-DBS')
        self.ProtocolNeurLabel.setAlignment(QtCore.Qt.AlignLeft)

        box2line1 = QHBoxLayout()
        box2line1.addWidget(self.VideoFile)
        box2line1.addWidget(self.VideoFileLabel)
        box2line1.addWidget(self.MRIpreop)
        box2line1.addWidget(self.MRIpreopLabel)
        box2line1.addWidget(self.FPCITpreop)
        box2line1.addWidget(self.FPCITpreopLabel)
        box2line1.addWidget(self.ProtocolNeurCheck)
        box2line1.addWidget(self.ProtocolNeurLabel)
        box2line1.addStretch()

        self.optionbox2Content.addLayout(box2line1)
        self.optionbox2.setLayout(self.optionbox2Content)

        # ====================    Optionbox (3) lower       ====================
        self.optionbox3 = QGroupBox('Scales and questionnaires:')
        self.optionbox3Content = QHBoxLayout(self.optionbox3)
        layout_general.addWidget(self.optionbox3, 2, 0)

        # TODO: the next part(s) should be moved to a helper function per condition to promote readability
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

        # ====================    Optionbox (2) middle       ====================
        self.optionbox4 = QGroupBox('Other:')
        self.optionbox4Content = QVBoxLayout(self.optionbox4)
        layout_general.addWidget(self.optionbox4, 3, 0)

        self.VideoFile = QCheckBox()
        self.VideoFileLabel = QLabel('Video')
        self.VideoFileLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.MRIpreop = QCheckBox()
        self.MRIpreopLabel = QLabel('MRI')
        self.MRIpreopLabel.setAlignment(QtCore.Qt.AlignLeft)
        self.FPCITpreop = QCheckBox()
        self.FPCITpreopLabel = QLabel('FP-CIT SPECT')
        self.FPCITpreopLabel.setAlignment(QtCore.Qt.AlignLeft)

        box4line1 = QHBoxLayout()
        box4line1.addWidget(self.VideoFile)
        box4line1.addWidget(self.VideoFileLabel)
        box4line1.addWidget(self.MRIpreop)
        box4line1.addWidget(self.MRIpreopLabel)
        box4line1.addWidget(self.FPCITpreop)
        box4line1.addWidget(self.FPCITpreopLabel)
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

        self.updatetext()

        # ====================   Actions when buttons are pressed      ====================
        self.ButtonEnterMedication.clicked.connect(self.onClickedMedication)
        self.button_save.clicked.connect(self.onClickedSaveReturn)

    def updatetext(self):
        """adds information extracted from database already provided"""

        # Todo: Marco, here further input is required so that every chunk of data is retrieved and may be saved later.
        #  Be careful by saving data, as everything may be deleted if you start pressing save before data is completely
        #  loaded.
        df_subj = Content.extract_saved_data(self.date)

        # Edit LineEdits with content
        self.hy.setText(str(df_subj["H&Y"][0]))
        self.updrsON.setText(str(df_subj["UPDRS On"][0]))
        self.updrsOFF.setText(str(df_subj["UPDRS Off"][0]))

        # Edit CheckBoxes with content
        if df_subj["Video"][0] != 0:
            self.VideoFile.setChecked(True)

        return

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
        """closes GUI and returns to calling (main) GUI"""
        print('Done!')
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = PreoperativeDialog()
    dlg.show()
    sys.exit(app.exec_())
