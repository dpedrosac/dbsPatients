#!/usr/bin/env python3
import os, sys, re
import numpy as np
import pandas as pds
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QFileDialog, QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QCheckBox
from GUI.GUImedication import MedicationDialog
from utils.helper_functions import General, Content, Clean, Output
from dependencies import FILEDIR, SYSTEMS


class PostoperativeDialog(QDialog):
    """Dialog to introduce all important information of postoperative patients."""

    def __init__(self, parent=None):
        super(PostoperativeDialog, self).__init__(parent)
        self.dialog_medication = None
        self.postoperative_date = ''
        self.date = 'postoperative'
        self.setup_ui()

    def setup_ui(self):
        self.setup_general_layout()

    def setup_general_layout(self):
        """Defines the general layout for the GUI"""
        subj_details = General.read_current_subj() # reads information for the subject last bein processed
        General.synchronize_data_with_general(self.date, subj_details.id[0], messagebox=False)

        self.create_medication_dialog()

        self.setWindowTitle('Postoperative Information (PID: {})'.format(str(int(subj_details.pid))))  # not necessary
        self.setGeometry(200, 100, 280, 170)
        self.move(400, 200)

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # start creating the option boxes that will appear in the postoperative GUI
        # Create optionbox for dates
        self.optionbox_dates(layout_general)

        # Create optionbox for general information
        self.optionbox_reason_for_visit(layout_general)

        # Create optionbox for reports during postoperative visit
        self.create_reports_optionbox(layout_general)

        # Create optionbox for tests performed during postoperative visits
        self.optionbox_postoperative_tests(layout_general)

        # Create option boxes for DBS settings after visit
        self.dbs_settings_optionbox(layout_general)

        # Create option boxes for amplitude, pulse, and frequency
        self.amp_pulse_freq_optionbox(layout_general)

        # Create buttons at the bottom of the GUI
        self.create_bottom_buttons(layout_general)

        # Connect button actions that are needed so that everything works
        self.connect_button_actions()

    def create_medication_dialog(self):
        self.dialog_medication = MedicationDialog(parent=self, visit=self.date)  # creates medication dialog
        self.dialog_medication.hide()

    def optionbox_dates(self, layout_general):
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

        self.optionbox_dates = QGroupBox('Important Dates')
        self.optionbox_datesContent = QVBoxLayout(self.optionbox_dates)
        layout_general.addWidget(self.optionbox_dates, 0, 0)

        admission_Nch, self.lineEditAdmission_Nch = create_line_edit_for_dates('Admission Neurosurgery')
        admission_NR, self.lineEditAdmission_NR = create_line_edit_for_dates('Admission Neurology')
        dismission_Nch, self.lineEditDismission_Nch = create_line_edit_for_dates('Dismission Neurosurgery')
        dismission_NR, self.lineEditDismission_NR = create_line_edit_for_dates('Dismission Neurology')
        surgery_date, self.lineEditSurgery = create_line_edit_for_dates('Surgery date')
        last_revision, self.lineEditLast_Revision = create_line_edit_for_dates('Last Revision')
        outpatient_contact, self.lineEditOutpatient_Contact = create_line_edit_for_dates('Outpatient Contact')

        # Create lines of layout
        testbox_line1 = create_horizontal_layout_dates(admission_Nch, self.lineEditAdmission_Nch)
        testbox_line2 = create_horizontal_layout_dates(admission_NR, self.lineEditAdmission_NR)
        testbox_line3 = create_horizontal_layout_dates(dismission_Nch, self.lineEditDismission_Nch)
        testbox_line4 = create_horizontal_layout_dates(dismission_NR, self.lineEditDismission_NR)
        testbox_line5 = create_horizontal_layout_dates(surgery_date, self.lineEditSurgery)
        testbox_line6 = create_horizontal_layout_dates(last_revision, self.lineEditLast_Revision)
        testbox_line7 = create_horizontal_layout_dates(outpatient_contact, self.lineEditOutpatient_Contact)

        # Add layouts to option box content
        self.optionbox_datesContent.addLayout(testbox_line1)
        self.optionbox_datesContent.addLayout(testbox_line2)
        self.optionbox_datesContent.addLayout(testbox_line3)
        self.optionbox_datesContent.addLayout(testbox_line4)
        self.optionbox_datesContent.addLayout(testbox_line5)
        self.optionbox_datesContent.addLayout(testbox_line6)
        self.optionbox_datesContent.addLayout(testbox_line7)

        self.optionbox_dates.setLayout(self.optionbox_datesContent)

    def optionbox_reason_for_visit(self, layout_general):
        """creates upper right optionbox in which reasons for visit is added"""

        self.optionbox_visit_information = QGroupBox('Information on visit')
        layout_general.addWidget(self.optionbox_visit_information, 0, 1)
        self.optionbox_visit_informationContent = QVBoxLayout(self.optionbox_visit_information)

        self.subj_IPG = QLabel('Implanted IPG:\t')
        self.lineEditsubjIPG = QComboBox()
        [self.lineEditsubjIPG.addItem(k) for k in SYSTEMS]

        ipg_layout = QHBoxLayout()
        ipg_layout.addWidget(self.subj_IPG)
        ipg_layout.addWidget(self.lineEditsubjIPG)
        ipg_layout.addStretch()

        self.subj_reason = QLabel('Reason:\t\t')
        self.lineEditreason = QComboBox()
        self.fill_combobox()

        reason_layout = QHBoxLayout()
        reason_layout.addWidget(self.subj_reason)
        reason_layout.addWidget(self.lineEditreason)
        reason_layout.addStretch()

        self.subj_Adverse_Event = QLabel('Adverse Events:\t')
        self.lineEditAdverse_Event = QLineEdit()
        self.lineEditAdverse_Event.setFixedWidth(300)
        #self.lineEditAdverse_Event.setFixedHeight(50)
        adverse_event_layout = QHBoxLayout()
        adverse_event_layout.addWidget(self.subj_Adverse_Event)
        adverse_event_layout.addWidget(self.lineEditAdverse_Event)
        adverse_event_layout.addStretch()

        self.optionbox_visit_informationContent.addLayout(ipg_layout)
        self.optionbox_visit_informationContent.addLayout(reason_layout)
        self.optionbox_visit_informationContent.addLayout(adverse_event_layout)
        self.optionbox_visit_information.setLayout(self.optionbox_visit_informationContent)

    def create_reports_optionbox(self, layout_general):
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
        self.PlannedVisitCheck = QCheckBox()
        self.PlannedVisit = QLabel('Planned Visit')

        box2line2 = QHBoxLayout()
        box2line2.addWidget(self.PostopCTCheck)
        box2line2.addWidget(self.PostopCT)
        box2line2.addWidget(self.PlannedVisitCheck)
        box2line2.addWidget(self.PlannedVisit)
        box2line2.addStretch()

        self.optionbox3Content.addLayout(box2line1)
        self.optionbox3Content.addLayout(box2line2)
        self.optionbox3.setLayout(self.optionbox3Content)

    def optionbox_postoperative_tests(self, layout_general):
        """optionbox containing the postopreative tests that are being applied"""

        def create_label_and_line_edit_pair(label_text, line_edit_width=50):
            label = QLabel(label_text)
            line_edit = QLineEdit()
            line_edit.setEnabled(False)
            line_edit.setFixedWidth(line_edit_width)
            return label, line_edit

        def create_horizontal_layout(*widgets):
            layout = QHBoxLayout()
            for widget in widgets:
                layout.addWidget(widget)
            layout.addStretch()
            return layout

        self.optionbox_tests = QGroupBox('Tests')
        self.optionbox_tests_content = QVBoxLayout(self.optionbox_tests)
        layout_general.addWidget(self.optionbox_tests, 1, 1)

        # First line of the optionbox
        updrs_i, self.lineEditUPDRSI = create_label_and_line_edit_pair('UPDRS I')
        updrs_iv, self.lineEditUPDRSIV = create_label_and_line_edit_pair('UPDRS IV')
        tss, self.lineEditTSS = create_label_and_line_edit_pair('TSS')
        cgic_pat, self.lineEditCGICPat = create_label_and_line_edit_pair('CGIC patient')
        cgic_clinician, self.lineEditCGICClinician = create_label_and_line_edit_pair('CGIC clinician and caregiver')

        testbox_line1 = create_horizontal_layout(updrs_i, self.lineEditUPDRSI, updrs_iv, self.lineEditUPDRSIV,
                                                 tss, self.lineEditTSS, cgic_pat, self.lineEditCGICPat,
                                                 cgic_clinician, self.lineEditCGICClinician)

        # Second line of the optionbox
        updrs_on, self.lineEditUPDRSON = create_label_and_line_edit_pair('UPDRS On')
        updrs_ii, self.lineEditUPDRSII = create_label_and_line_edit_pair('UPDRS II')
        hruq, self.lineEditHRUQ = create_label_and_line_edit_pair('HRUQ')
        moca, self.lineEditMoCa = create_label_and_line_edit_pair('MoCa')
        mmst, self.lineEditMMST = create_label_and_line_edit_pair('MMST')
        bdi_ii, self.lineEditBDIII = create_label_and_line_edit_pair('BDI-II')
        nmsq, self.lineEditNMSQ = create_label_and_line_edit_pair('NMSQ')

        # Create second line layout
        testbox_line2 = create_horizontal_layout(
            updrs_on, self.lineEditUPDRSON,
            updrs_ii, self.lineEditUPDRSII,
            hruq, self.lineEditHRUQ,
            moca, self.lineEditMoCa,
            mmst, self.lineEditMMST,
            bdi_ii, self.lineEditBDIII,
            nmsq, self.lineEditNMSQ
        )

        # Third line of the optionbox
        updrs_off, self.lineEditUPDRSOFF = create_label_and_line_edit_pair('UPDRS Off')
        hy, self.lineEditHY = create_label_and_line_edit_pair('H&Y')
        eq5d, self.lineEditEQ5D = create_label_and_line_edit_pair('EQ5D')
        demtect, self.lineEditDemTect = create_label_and_line_edit_pair('DemTect')
        pdq8, self.lineEditPDQ8 = create_label_and_line_edit_pair('PDQ8')
        pdq39, self.lineEditPDQ39 = create_label_and_line_edit_pair('PDQ39')
        se, self.lineEditSE = create_label_and_line_edit_pair('S&E')

        # Create third line layout
        testbox_line3 = create_horizontal_layout(
            updrs_off, self.lineEditUPDRSOFF,
            hy, self.lineEditHY,
            eq5d, self.lineEditEQ5D,
            demtect, self.lineEditDemTect,
            pdq8, self.lineEditPDQ8,
            pdq39, self.lineEditPDQ39,
            se, self.lineEditSE
        )

        # fourth line of the optionbox
        uddrs_on, self.lineEditUDDRSOn = create_label_and_line_edit_pair('UDDRS On')
        trs_on, self.lineEditTRSOn = create_label_and_line_edit_pair('TRS On')
        uddrs_off, self.lineEditUDDRSOff = create_label_and_line_edit_pair('UDDRS Off')
        trs_off, self.lineEditTRSOff = create_label_and_line_edit_pair('TRS Off')

        # Create fourth line layout
        testbox_line4 = create_horizontal_layout(
            uddrs_on, self.lineEditUDDRSOn,
            trs_on, self.lineEditTRSOn,
            uddrs_off, self.lineEditUDDRSOff,
            trs_off, self.lineEditTRSOff
        )

        # Add layouts to option box content
        self.optionbox_tests_content.addLayout(testbox_line1)
        self.optionbox_tests_content.addLayout(testbox_line2)
        self.optionbox_tests_content.addLayout(testbox_line3)
        self.optionbox_tests_content.addLayout(testbox_line4)

        self.optionbox_tests.setLayout(self.optionbox_tests_content)

    def dbs_settings_optionbox(self, layout_general, num_contacts=8):
        """Creates an option box with a grid according to the number of contacts available"""
        self.optionbox_dbs_contacts = QGroupBox('DBS settings after dismissal')
        self.optionbox_dbs_contactsContent = QVBoxLayout(self.optionbox_dbs_contacts)
        layout_general.addWidget(self.optionbox_dbs_contacts, 3, 0)

        self.titleRowContacts = Content.create_title(num_contacts, string2use=[1,2,3,4,5,6,7,8])
        self.DBSpercentageLeft1 = Content.create_contents_grid_with_rows(side_label='Left', side_no=1,
                                                                         num_columns=num_contacts)
        self.DBSpercentageRight1 = Content.create_contents_grid_with_rows(side_label='Right', side_no=1,
                                                                          num_columns=num_contacts)
        self.DBSpercentageLeft2 = Content.create_contents_grid_with_rows(side_label='Left', side_no=2,
                                                                         num_columns=num_contacts)
        self.DBSpercentageRight2 = Content.create_contents_grid_with_rows(side_label='Right', side_no=2,
                                                                          num_columns=num_contacts)

        toggleButton = QPushButton('+', self)
        toggleButton.setFixedSize(20, 20)  # Set a fixed size
        toggleButton.clicked.connect(self.toggle_content_visibilityPercentage)
        self.set_initial_content_statePercentage()

        self.optionbox_dbs_contactsContent.addStretch(2)
        self.optionbox_dbs_contactsContent.addLayout(self.titleRowContacts)
        self.optionbox_dbs_contactsContent.addLayout(self.DBSpercentageLeft1)
        self.optionbox_dbs_contactsContent.addLayout(self.DBSpercentageRight1)
        self.optionbox_dbs_contactsContent.addWidget(toggleButton)
        self.optionbox_dbs_contactsContent.addLayout(self.DBSpercentageLeft2)
        self.optionbox_dbs_contactsContent.addLayout(self.DBSpercentageRight2)

    def set_initial_content_statePercentage(self):
        [item.widget().setEnabled(False) for widget in [self.DBSpercentageLeft2, self.DBSpercentageRight2]
         for i in range(widget.count()) if (item := widget.itemAt(i)) is not None and item.widget() is not None]

    def toggle_content_visibilityPercentage(self):
        [item.widget().setEnabled(not item.widget().isEnabled())
         for widget in [self.DBSpercentageLeft2, self.DBSpercentageRight2]
         for i in range(widget.count()) if (item := widget.itemAt(i)) is not None and item.widget() is not None]

    def amp_pulse_freq_optionbox(self, layout_general, num_columns=3):
        """Optionbox for the DBS settings """
        self.optionbox_dbs_settings = QGroupBox('Amplitude, Pulse, and Frequency')
        self.optionbox_dbs_settingsContent = QVBoxLayout(self.optionbox_dbs_settings)
        layout_general.addWidget(self.optionbox_dbs_settings, 3, 1)

        self.titleRowSettings = Content.create_title(num_columns, string2use=['Amplitude [mA]',
                                                                              'Pulse width [µs]',
                                                                              'Frequency [Hz]'])
        self.DBSsettingsLeft1 = Content.create_contents_grid_with_rows(side_label='Left', side_no=1,
                                                                       num_columns=num_columns)
        self.DBSsettingsRight1 = Content.create_contents_grid_with_rows(side_label='Right', side_no=1,
                                                                        num_columns=num_columns)
        self.DBSsettingsLeft2 = Content.create_contents_grid_with_rows(side_label='Left', side_no=2,
                                                                       num_columns=num_columns)
        self.DBSsettingsRight2 = Content.create_contents_grid_with_rows(side_label='Right', side_no=2,
                                                                        num_columns=num_columns)

        toggleButton = QPushButton('+', self)
        toggleButton.setFixedSize(20, 20)  # Set a fixed size
        toggleButton.clicked.connect(self.toggle_content_visibilitySettings)
        self.set_initial_content_stateSettings()

        self.optionbox_dbs_settingsContent.addStretch(2)
        self.optionbox_dbs_settingsContent.addLayout(self.titleRowSettings)
        self.optionbox_dbs_settingsContent.addLayout(self.DBSsettingsLeft1)
        self.optionbox_dbs_settingsContent.addLayout(self.DBSsettingsRight1)
        self.optionbox_dbs_settingsContent.addWidget(toggleButton)
        self.optionbox_dbs_settingsContent.addLayout(self.DBSsettingsLeft2)
        self.optionbox_dbs_settingsContent.addLayout(self.DBSsettingsRight2)

    def set_initial_content_stateSettings(self):
        [item.widget().setEnabled(False) for widget in [self.DBSsettingsLeft2, self.DBSsettingsRight2]
         for i in range(widget.count()) if (item := widget.itemAt(i)) is not None and item.widget() is not None]

    def toggle_content_visibilitySettings(self):
        [item.widget().setEnabled(not item.widget().isEnabled())
         for widget in [self.DBSsettingsLeft2, self.DBSsettingsRight2]
         for i in range(widget.count()) if (item := widget.itemAt(i)) is not None and item.widget() is not None]

    def create_bottom_buttons(self, layout_general):
        """Creates two buttons a) to read medication and b) to save settings and exit GUI """
        self.ButtonEnterMedication = QPushButton('Open GUI \nMedication')
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
        hlay_bottom.addWidget(self.button_buffer)
        hlay_bottom.addWidget(self.button_save)
        hlay_bottom.addStretch(1)
        layout_general.addLayout(hlay_bottom, 4, 0, 1, 3)

        self.read_content_csv()

    def connect_button_actions(self):
        """Defines the actions that are taken once a button is pressed or specific input is made"""
        self.lineEditreason.currentIndexChanged.connect(self.update_context)
        self.lineEditsubjIPG.currentIndexChanged.connect(self.update_IPG)
        self.ButtonEnterMedication.clicked.connect(self.on_clickedMedication)
        self.button_buffer.clicked.connect(self.onClickedSave)
        self.button_save.clicked.connect(self.onClickedSaveReturn)

    # From here on, you can find the function of the buttons, etc.
    def fill_combobox(self):
        """fills ComboBox for postoperative visits"""
        items_available = Content.extract_postoperative_dates()
        default_options = ['Please select date or enter new data', 'Enter new data']
        items_available = default_options if not items_available else items_available + default_options
        unique_dates = list(set(items_available))

        def custom_sort(item):
            if item in default_options:
                return (default_options.index(item), item)
            else:
                return (len(default_options), item)

        # Add items to ComboBox
        self.lineEditreason.clear()
        self.lineEditreason.addItems(sorted(unique_dates, key=custom_sort))
        # self.update_context() # Not sure if that is needed but so far it drops no error, so keep it!

    # ====================   Defines what happens when ComboBox is modified      ====================
    def set_widget_text(self, widget, value):
        """Set widget text, handling NaN values. Generic function used in read_content_csv"""
        widget.setText(str(value)) if not pds.isna(value) else widget.setText('')

    def update_line_edits(self, line_edits, data_row):
        """Update line edits with corresponding data from the row. Generic function used in read_content_csv"""
        for line_edit, column_name in line_edits:
            self.set_widget_text(line_edit, data_row[column_name])

    def update_dbs_settings(self, layout, data_row, side):
        """Update DBS settings widgets with data from the row."""
        # Assuming you want to update three columns with different names
        column_names = [f'Ampl{side}_postop', f'PW{side}_postop', f'Freq{side}_postop']

        for i, column_name in enumerate(column_names, start=1):
            widget = layout.itemAtPosition(0, i).widget()
            self.set_widget_text(widget, data_row[column_name])

    def read_content_csv(self):
        """After selecting the reason for visit, data is read from the csv-file [preoperative] if available"""
        print('updating content for the selected visit date...')
        df_subj = General.import_dataframe(f"{self.date}.csv", separator_csv=',')

        if df_subj.empty:
            Output.msg_box(text='Something went wrong when looking for the data',
                           title=f'{self.date}.csv not found in the folder: {FILEDIR}/data/',
                           flag='File not found')
            return

        df_subj = df_subj[df_subj['PID_ORBIS'] == General.read_current_subj().pid[0]]
        df_subj_filtered = df_subj[df_subj['Reason_postop'] == self.lineEditreason.currentText()]

        if self.lineEditreason.currentText() == 'Please select date or enter new data':
            return  # Script stops, as intended to only provide opportunity to add new data or modify existing entries

        try:
            row = df_subj_filtered.iloc[0]
        except IndexError:
            row = pds.Series(['nan' for _ in range(len(df_subj_filtered.columns))], index=df_subj_filtered.columns)

        line_edits_upper_right = [
            (self.lineEditAdmission_Nch, "Admission_NCh_postop"),
            (self.lineEditAdmission_NR, "Admission_NR_postop"),
            (self.lineEditDismission_Nch, "Dismissal_NCh_postop"),
            (self.lineEditDismission_NR, "Dismissal_NR_postop"),
            (self.lineEditSurgery, "Surgery_Date_postop"),
        ]

        self.update_line_edits(line_edits_upper_right, row)

        # Upper right
        self.set_widget_text(self.lineEditAdverse_Event, row["AE_postop"])

        # Middle right
        line_edits_middle_right = [
            (self.lineEditUPDRSI, "UPDRS1_postop"),
            (self.lineEditUPDRSIV, "UPDRS4_postop"),
            (self.lineEditCGICPat, "CGIC_patient_postop"),
            (self.lineEditCGICClinician, "CGIC_clinician_caregiver_postop"),
            (self.lineEditUPDRSON, "UPDRS_On_postop"),
            (self.lineEditUPDRSOFF, "UPDRS_Off_postop"),
            (self.lineEditUPDRSII, "UPDRSII_postop"),
            (self.lineEditHRUQ, "HRUQ_postop"),
            (self.lineEditMoCa, "MoCa_postop"),
            (self.lineEditMMST, "MMST_postop"),
            (self.lineEditBDIII, "BDI2_postop"),
            (self.lineEditNMSQ, "NMSQ_postop"),
            (self.lineEditHY, "H&Y_postop"),
            (self.lineEditEQ5D, "EQ5D_postop"),
            (self.lineEditDemTect, "DemTect_postop"),
            (self.lineEditPDQ8, "PDQ8_postop"),
            (self.lineEditPDQ39, "PDQ39_postop"),
            (self.lineEditSE, "S&E_postop"),
            (self.lineEditUDDRSOn, "UDDRSon_postop"),
            (self.lineEditTRSOn, "TRSon_postop"),
            (self.lineEditUDDRSOff, "UDDRSoff_postop"),
            (self.lineEditTRSOff, "TRSoff_postop")
        ]

        self.update_line_edits(line_edits_middle_right, row)

        # DBS settings (bottom left and right)
        self.update_dbs_settings(self.DBSsettingsLeft1, row, side='L')
        self.update_dbs_settings(self.DBSsettingsRight1, row, side='R')

        # TODO: percentage of DBS missing

        # CheckBoxes
        self.ReportNeurCheck.setChecked(bool(row["Report_File_NCh_postop"]))
        self.ReportNeurosurgeryCheck.setChecked(bool(row["Report_File_NR_postop"]))
        self.PatProgrammerCheck.setChecked(bool(row["Using_Programmer_postop"]))
        self.PostopCTCheck.setChecked(bool(row["CTscan_postop"]))

    def read_content_csv_old(self):
        """DO NOT DELETE UNTIL THE PERCENTAGE OF CURRENT IS TRANSFERRED! After selecting the reason for visit, data is read from the csv-file [preoperative] if available"""
        print('updating content for the selected visit date...')
        df_subj = General.import_dataframe(f"{self.date}.csv", separator_csv=',')
        if df_subj.empty:
            Output.msg_box(text='Something went wrong when looking for the data',
                           title=f'{self.date}.csv not found in the folder: {FILEDIR}/data/',
                           flag='File not found')
            return

        df_subj = df_subj[df_subj['PID_ORBIS'] == General.read_current_subj().pid[0]]
        df_subj_filtered = df_subj[df_subj['Reason_postop'] == self.lineEditreason.currentText()]
        if df_subj.empty:
            Output.msg_box(text=f'Subject: {General.read_current_subj().pid[0]} not found, please double check!',
                           title=f'{self.date} not found in {FILEDIR}/data/postoperative.csv',
                           flag='File not found')
            return

        if self.lineEditreason.currentText() == 'Please select date or enter new data':
            # Script stops, as it is intended to only provide the opportunity to add new data or modify existing one
            return

        else:
            try:
                row = df_subj_filtered.iloc[0]
            except IndexError:
                df_subj_filtered = df_subj_filtered.apply(lambda x: 'nan')
                row = df_subj_filtered

            line_edits = [
                (self.lineEditAdmission_Nch, "Admission_NCh_postop"),
                (self.lineEditAdmission_NR, "Admission_NR_postop"),
                (self.lineEditDismission_Nch, "Dismissal_NCh_postop"),
                (self.lineEditDismission_NR, "Dismissal_NR_postop"),
                (self.lineEditSurgery, "Surgery_Date_postop"),
            ]

            for line_edit, column_name in line_edits: # iterate over list and update every QLineEdit

                value = str(df_subj_filtered[column_name].iloc[0])
                line_edit.setText(value) if value != 'nan' else line_edit.setText('')

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
            self.lineEditCGICPat.setText(str(row["CGIC_patient_postop"])) \
                if str(row["CGIC_patient_postop"]) != 'nan' else self.lineEditCGICPat.setText('')
            self.lineEditCGICClinician.setText(str(row["CGIC_clinician_caregiver_postop"])) \
                if str(row["CGIC_clinician_caregiver_postop"]) != 'nan' else self.lineEditCGICClinician.setText('')
            self.lineEditUPDRSON.setText(str(row["UPDRS_On_postop"])) \
                if str(row["UPDRS_On_postop"]) != 'nan' else self.lineEditUPDRSON.setText('')
            self.lineEditUPDRSOFF.setText(str(row["UPDRS_Off_postop"])) \
                if str(row["UPDRS_Off_postop"]) != 'nan' else self.lineEditUPDRSOFF.setText('')
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
            self.lineEditUDDRSOn.setText(str(row["UDDRSon_postop"])) \
                if str(row["UDDRSon_postop"]) != 'nan' else self.lineEditUDDRSOn.setText('')
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

            # bottom, DBS percentage left and right
            DBSleft = self.DBSpercentageLeft1.itemAtPosition(0, 1).widget()
            DBSleft.setText(str(row["Perc1_postop"]))
            DBSleft = self.DBSpercentageLeft1.itemAtPosition(0, 2).widget()
            DBSleft.setText(str(row["Perc2_postop"]))
            DBSleft = self.DBSpercentageLeft1.itemAtPosition(0, 3).widget()
            DBSleft.setText(str(row["Perc3_postop"]))
            DBSleft = self.DBSpercentageLeft1.itemAtPosition(0, 4).widget()
            DBSleft.setText(str(row["Perc4_postop"]))
            DBSleft = self.DBSpercentageLeft1.itemAtPosition(0, 5).widget()
            DBSleft.setText(str(row["Perc5_postop"]))
            DBSleft = self.DBSpercentageLeft1.itemAtPosition(0, 6).widget()
            DBSleft.setText(str(row["Perc6_postop"]))
            DBSleft = self.DBSpercentageLeft1.itemAtPosition(0, 7).widget()
            DBSleft.setText(str(row["Perc7_postop"]))
            DBSleft = self.DBSpercentageLeft1.itemAtPosition(0, 8).widget()
            DBSleft.setText(str(row["Perc8_postop"]))

            # DBS right

            DBSright = self.DBSpercentageRight1.itemAtPosition(0, 1).widget()
            DBSright.setText(str(row["Perc9_postop"]))
            DBSright = self.DBSpercentageRight1.itemAtPosition(0, 2).widget()
            DBSright.setText(str(row["Perc10_postop"]))
            DBSright = self.DBSpercentageRight1.itemAtPosition(0, 3).widget()
            DBSright.setText(str(row["Perc11_postop"]))
            DBSright = self.DBSpercentageRight1.itemAtPosition(0, 4).widget()
            DBSright.setText(str(row["Perc12_postop"]))
            DBSright = self.DBSpercentageRight1.itemAtPosition(0, 5).widget()
            DBSright.setText(str(row["Perc13_postop"]))
            DBSright = self.DBSpercentageRight1.itemAtPosition(0, 6).widget()
            DBSright.setText(str(row["Perc14_postop"]))
            DBSright = self.DBSpercentageRight1.itemAtPosition(0, 7).widget()
            DBSright.setText(str(row["Perc15_postop"]))
            DBSright = self.DBSpercentageRight1.itemAtPosition(0, 8).widget()
            DBSright.setText(str(row["Perc16_postop"]))

            # Bottom right
            # setting left

            # Get a reference to the Amplitude widget for the left side
            amplitudeLeftWidget = self.DBSsettingsLeft1.itemAtPosition(0, 1).widget()
            amplitudeLeftWidget.setText(str(row["AmplL_postop"]))

            pulseWidthLeftWidget = self.DBSsettingsLeft1.itemAtPosition(0, 2).widget()
            pulseWidthLeftWidget.setText(str(row["PWL_postop"]))

            frequencyLeftWidget = self.DBSsettingsLeft1.itemAtPosition(0, 3).widget()
            frequencyLeftWidget.setText(str(row["FreqL_postop"]))

            amplitudeRightWidget = self.DBSsettingsRight1.itemAtPosition(0, 1).widget()
            amplitudeRightWidget.setText(str(row["AmplR_postop"]))

            pulseWidthRightWidget = self.DBSsettingsRight1.itemAtPosition(0, 2).widget()
            pulseWidthRightWidget.setText(str(row["PWR_postop"]))

            frequencyRightWidget = self.DBSsettingsRight1.itemAtPosition(0, 3).widget()
            frequencyRightWidget.setText(str(row["FreqR_postop"]))

    def set_lineedit_state(self, state, *line_edits):
        """this function enables LineEdits, needed to avoid data entries without first selecting reason"""
        for line_edit in line_edits:
            line_edit.setEnabled(state)

    def update_context(self):
        """updates the context according to what was selected in the ComboBox"""

        selected_item1 = self.lineEditreason.currentText()
        selected_item2 = self.lineEditsubjIPG.currentText()
        optionboxes = Content.get_lineedits_in_optionbox(
            [self.optionbox_tests,
             self.optionbox_dates,
             self.optionbox_dbs_contacts,
             self.optionbox_dbs_settings])

        if ((selected_item1 != 'Enter new data' and selected_item1 != 'Please select date or enter new data') and
                selected_item2 != ''):
            self.set_lineedit_state(True, *optionboxes)
        else:
            self.set_lineedit_state(False, *optionboxes)

        if self.lineEditreason.currentText() == 'Please select date or enter new data':
            pass
        elif self.lineEditreason.currentText() == 'Enter new data':
            self.reason_visit = Output.open_input_dialog_postoperative(self)
            data_frame = General.import_dataframe(f"{self.date}.csv", separator_csv=',')
            subj_details = General.read_current_subj()

            match = re.search(r'^(pre|intra|post)op', self.date)
            data_frame.loc[len(data_frame), ['ID', 'PID_ORBIS', 'Reason_{}'.format(match.group())]] = [subj_details.id[0],
                                                                                                       subj_details.pid[0],
                                                                                                       self.reason_visit]
            data_frame = data_frame.replace(['nan', ''], [np.nan, np.nan])
            data_frame = data_frame.applymap(lambda x: str(x).replace(';', ' -'))
            data_frame.to_csv(os.path.join(FILEDIR, f"{self.date}.csv"), index=False)

            self.fill_combobox()
            self.read_content_csv()
        else:
            self.reason_visit = self.lineEditreason.currentText()
            self.read_content_csv()
            self.save_data2csv()

    def update_IPG(self):
        """Used so that no data is entered until some information is provided"""

        selected_item1 = self.lineEditreason.currentText()
        selected_item2 = self.lineEditsubjIPG.currentText()

        optionboxes = Content.get_lineedits_in_optionbox(
            [self.optionbox_tests,
             self.optionbox_dates,
             self.optionbox_dbs_contacts,
             self.optionbox_dbs_settings])

        # Enable/disable LineEdits if no data was yet entered
        if ((selected_item1 != 'Enter new data' and selected_item1 != 'Please select date or enter new data') and
                selected_item2 != ''):
            self.set_lineedit_state(True, *optionboxes)
        else:
            self.set_lineedit_state(False, *optionboxes)

    @QtCore.pyqtSlot()
    def on_clickedMedication(self):
        """shows the medication dialog when button is pressed; former implementation with creating GUI was replaced with
        show/hide GUI which is initiated at beginning"""
        self.dialog_medication.show()

    @QtCore.pyqtSlot()
    def onClickedSave(self):
        self.save_data2csv()

    @QtCore.pyqtSlot()
    def onClickedSaveReturn(self):
        """
        Saves the data passed into the GUI form and returns to previous Window.

        Args:
            pds: dataframe to safe??

        Returns: None

        """
        self.save_data2csv()
        self.close()

    def save_data2csv(self):
        current_subj = General.read_current_subj()
        subject_id = current_subj['id'][0]
        df_general = Clean.extract_subject_data(subject_id)
        match = re.search(r'^(pre|intra|post)op', self.date)

        df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=',')
        try:
            df_subj = df.iloc[df.index[df['Reason_postop'] == self.reason_visit][0], :].to_dict()
        except IndexError:
            df_subj = pds.Series(['nan' for _ in range(len(df.columns))], index=df.columns)

        df_general.reset_index(inplace=True, drop=True)
        df_subj['ID'] = General.read_current_subj().id[0]
        df_subj['PID_ORBIS'] = df_general.iloc[0, :]['PID_ORBIS']
        df_subj['Gender'] = df_general['Gender'][0]
        df_subj['Diagnosis_{}'.format(match.group())] = df_general['diagnosis'][0]

        # Extract text for the upper left optionbox
        line_edits = [
            (self.lineEditAdmission_Nch, 'Admission_NCh'),
            (self.lineEditAdmission_NR, 'Admission_NR'),
            (self.lineEditDismission_Nch, 'Dismissal_NCh'),
            (self.lineEditDismission_NR, 'Dismissal_NR'),
            (self.lineEditSurgery, 'Surgery_Date'),
            (self.lineEditLast_Revision, 'Last_revision'),
            (self.lineEditOutpatient_Contact, 'Outpatient_Contact'),
        ]

        # Iterate over the list and update the DataFrame
        for line_edit, column_name in line_edits:
            column_key = f'{column_name}_{match.group()}'
            df_subj[column_key] = line_edit.text()

        # upper right
        df_subj['AE_{}'.format(match.group())] = self.lineEditAdverse_Event.text()

        # middle right
        df_subj['UPDRS1_{}'.format(match.group())] = self.lineEditUPDRSI.text()
        df_subj['UPDRS4_{}'.format(match.group())] = self.lineEditUPDRSIV.text()
        df_subj['TSS_postop'] = self.lineEditTSS.text()
        df_subj['CGIC_patient_postop'] = self.lineEditCGICPat.text()
        df_subj['CGIC_clinician_caregiver_postop'] = self.lineEditCGICClinician.text()
        df_subj["UPDRSon_postop"] = self.lineEditUPDRSON.text()
        df_subj["UPDRSII_postop"] = self.lineEditUPDRSII.text()
        df_subj["UPDRSoff_postop"] = self.lineEditUPDRSOFF.text()
        df_subj["H&Y_postop"] = self.lineEditHY.text()
        df_subj["HRUQ_post"] = self.lineEditHRUQ.text()
        df_subj["MoCa_postop"] = self.lineEditMoCa.text()
        df_subj["MMST_postop"] = self.lineEditMMST.text()
        df_subj["BDI2_postop"] = self.lineEditBDIII.text()
        df_subj["NMSQ_postop"] = self.lineEditNMSQ.text()
        df_subj["EQ5D_postop"] = self.lineEditEQ5D.text()
        df_subj["DemTect_postop"] = self.lineEditDemTect.text()
        df_subj["PDQ8_postop"] = self.lineEditPDQ8.text()
        df_subj["PDQ39_postop"] = self.lineEditPDQ39.text()
        df_subj["S&E_postop"] = self.lineEditSE.text()
        df_subj["UDDRSon_postop"] = self.lineEditUDDRSOn.text()
        df_subj["TRSon_postop"] = self.lineEditTRSOn.text()
        df_subj["UDDRSoff_postop"] = self.lineEditUDDRSOff.text()
        df_subj["TRSoff_postop"] = self.lineEditTRSOff.text()

        # middle left
        checkbox_cols = [("ReportNeurCheck", "Report_File_NCh_postop"),
                         ("ReportNeurosurgeryCheck", "Report_File_NR_postop"),
                         ("PatProgrammerCheck", "Using_Programmer_postop"), ("PostopCTCheck", "CTscan_postop")]

        for checkbox, col_name in checkbox_cols:
            if getattr(self, checkbox).isChecked():
                df_subj[col_name] = 1
            else:
                df_subj[col_name] = 0
            # Incorporate the [df_subj] dataframe into the entire dataset and save as csv

        indices_to_update = df.index[df['Reason_postop'] == self.reason_visit]

        # Check if any indices match the condition
        if not indices_to_update.empty:
            # Take the first index from the Int64Index object
            index_to_update = indices_to_update[0]
            df.loc[index_to_update] = df_subj
        else:
            # Handle the case when the index is not found
            print(f"Index for Reason_postop '{self.reason_visit}' not found.")

        df.to_csv(os.path.join(FILEDIR, "postoperative.csv"), index=False)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "test.txt",
                                                  "All Files(*)", options=options)
        print(fileName)

    # for opening
    def open_dialog_box(self):
        option = QFileDialog.Options()
        file = QFileDialog.getOpenFileName(self, "Save File Window Title", "default.txt",
                                           "All Files (*)", options=option)
        print(file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = PostoperativeDialog()
    dlg.show()
    sys.exit(app.exec_())
