#!/usr/bin/env python3
import os, sys, re
import numpy as np
import pandas as pds
from PyQt5 import QtCore
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QFileDialog, QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QCheckBox, QMessageBox, QSpacerItem, QSizePolicy
from GUImedication import MedicationDialog
from GUI.GUIsettingsDBS import DBSsettingsDialog
from utils.helper_functions import General, Content, Clean, Output
from dependencies import FILEDIR, dtype_dict_postoperative


class PostoperativeDialog(QDialog):
    """Dialog to introduce all important information of postoperative patients."""

    def __init__(self, parent=None):
        super(PostoperativeDialog, self).__init__(parent)
        self.dialog_medication, self.dialog_DBSsettings, self.content_widgets = None, None, None  # initialised  Dialogs
        self.postoperative_date = ''
        self.date = 'postoperative'
        self.setup_ui()

    def setup_ui(self):
        self.setup_general_layout()

    def setup_general_layout(self):
        """Defines the general layout for the GUI"""
        subj_details = General.read_current_subj()  # reads information for the subject last being processed
        General.synchronize_data_with_general(self.date, subj_details.id[0],
                                              messagebox=False)  # for identical general columns in 'postoperative.csv'

        #self.create_medication_dialog()
        #self.create_DBSsettings_dialog()

        self.setWindowTitle(f'Please insert the postoperative information (PID: {int(subj_details.pid.iloc[0])})')
        self.setGeometry(200, 100, 280, 170)
        self.setMaximumWidth(2500)
        self.move(400, 200)

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # Option boxes appearing in the postoperative GUI
        # Create optionbox for dates
        self.optionbox_dates_postoperative(layout_general)

        # Create optionbox for general information
        self.optionbox_reason_for_visit_postoperative(layout_general)

        # Create optionbox for reports during postoperative visit
        self.optionbox_reports_postoperative(layout_general)

        # Create optionbox for tests performed during postoperative visits
        self.optionbox_questionnaires_postoperative(layout_general)

        # Create buttons at the bottom of the GUI
        self.create_bottom_buttons_postoperative(layout_general)

        # Connect button actions that are needed so that everything works
        self.connect_button_actions()

    # def create_medication_dialog(self):
    #    self.dialog_medication = MedicationDialog(parent=self, visit=self.date)  # creates medication dialog
    #    self.dialog_medication.hide()

    #def create_DBSsettings_dialog(self):
    #    self.dialog_DBSsettings = DBSsettingsDialog(parent=self, visit=self.date)  # creates DBSsettings dialog
    #    self.dialog_DBSsettings.hide()

    def optionbox_dates_postoperative(self, layout_general):
        """creates upper left optionbox in which important dates are added"""

        def create_line_edit_for_dates(label_text, line_edit_width=200, label_width=250):
            label = QLabel(f'{label_text}:\t\t')
            label.setFixedWidth(label_width)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText('(DD/MM/YYYY)')
            line_edit.setEnabled(False)
            line_edit.setFixedWidth(line_edit_width)
            line_edit.editingFinished.connect(self.validate_date_input)
            return label, line_edit

        def create_horizontal_layout_dates(*widgets):
            layout = QHBoxLayout()
            for widget in widgets:
                layout.addWidget(widget)
            layout.addStretch(1)
            return layout

        self.optionbox_dates_postoperative = QGroupBox('Important dates')
        self.optionbox_dates_postoperative.setMaximumWidth(600)
        self.optionbox_datesContent = QVBoxLayout(self.optionbox_dates_postoperative)
        layout_general.addWidget(self.optionbox_dates_postoperative, 0, 0)

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

        self.optionbox_dates_postoperative.setLayout(self.optionbox_datesContent)

    def validate_date_input(self):
        #GP: nutzt die staticmethod um das Format zu überprüfen (DD/MM/YYYY)
        """Validates the date input in the QLineEdit for optionbox_dates_postoperative"""
        sender = self.sender()
        date_text = sender.text()
        formatted_date = General.validate_and_format_dates(date_text)
        print(date_text)
        if date_text == '':
            pass
        elif formatted_date == 'Invalid date format':
            QMessageBox.warning(self, 'Invalid Date', 'The entered date is invalid. Please enter a date in the format DD/MM/YYYY.')
            sender.setText('')
        else:
            sender.setText(formatted_date)

    def optionbox_reason_for_visit_postoperative(self, layout_general):
        """creates upper right optionbox in which reasons for visit is added"""

        self.optionbox_visit_information = QGroupBox('Information on visit')
        self.optionbox_visit_information.setMaximumWidth(1200)
        layout_general.addWidget(self.optionbox_visit_information, 0, 1)
        self.optionbox_visit_informationContent = QVBoxLayout(self.optionbox_visit_information)

        self.subj_reason = QLabel('Reason:\t\t')
        self.lineEditreason = QComboBox()
        self.lineEditreason.setFixedWidth(400)
        self.fill_combobox()

        reason_layout = QHBoxLayout()
        reason_layout.addWidget(self.subj_reason)
        reason_layout.addWidget(self.lineEditreason)
        reason_layout.addStretch()

        self.subj_Adverse_Event = QLabel('Adverse Events:\t')
        self.lineEditAdverse_Event = QLineEdit()
        self.lineEditAdverse_Event.setFixedWidth(400)
        #self.lineEditAdverse_Event.setFixedHeight(50)
        adverse_event_layout = QHBoxLayout()
        adverse_event_layout.addWidget(self.subj_Adverse_Event)
        adverse_event_layout.addWidget(self.lineEditAdverse_Event)
        adverse_event_layout.addStretch()

        self.optionbox_visit_informationContent.addLayout(reason_layout)
        self.optionbox_visit_informationContent.addLayout(adverse_event_layout)
        self.optionbox_visit_information.setLayout(self.optionbox_visit_informationContent)

    def optionbox_reports_postoperative(self, layout_general):
        #GP: used new method to tighten up script while adding setEnabled(False)
        def create_label_and_checkbox_pair(label_text):
            checkbox = QCheckBox()
            checkbox.setEnabled(False)
            label = QLabel(label_text)
            return checkbox, label

        # Create third optionbox on the second row left
        self.optionbox3 = QGroupBox('Reports')
        self.optionbox3.setMaximumWidth(600)
        self.optionbox3Content = QVBoxLayout(self.optionbox3)
        layout_general.addWidget(self.optionbox3, 1, 0)

        self.ReportNeurCheck, self.ReportNeur = create_label_and_checkbox_pair('Report Neurology')
        self.ReportNeurosurgeryCheck, self.ReportNeurosurgery = create_label_and_checkbox_pair('Report Neurosurgery')
        self.PatProgrammerCheck, self.PatProgrammer = create_label_and_checkbox_pair('Patient Programmer in use')
        self.PostopCTCheck, self.PostopCT = create_label_and_checkbox_pair('Postoperative CT Scan')
        self.PlannedVisitCheck, self.PlannedVisit = create_label_and_checkbox_pair('Planned Visit')

        # Create horizontal layouts for each pair
        box2line1 = QHBoxLayout()
        box2line1.addWidget(self.ReportNeurCheck)
        box2line1.addWidget(self.ReportNeur)
        box2line1.addStretch()

        box2line2 = QHBoxLayout()
        box2line2.addWidget(self.ReportNeurosurgeryCheck)
        box2line2.addWidget(self.ReportNeurosurgery)
        box2line2.addStretch()

        box2line3 = QHBoxLayout()
        box2line3.addWidget(self.PatProgrammerCheck)
        box2line3.addWidget(self.PatProgrammer)
        box2line3.addStretch()

        box2line4 = QHBoxLayout()
        box2line4.addWidget(self.PostopCTCheck)
        box2line4.addWidget(self.PostopCT)
        box2line4.addStretch()

        box2line5 = QHBoxLayout()
        box2line5.addWidget(self.PlannedVisitCheck)
        box2line5.addWidget(self.PlannedVisit)
        box2line5.addStretch()

        # Add horizontal layouts to the main vertical layout
        self.optionbox3Content.addLayout(box2line1)
        self.optionbox3Content.addLayout(box2line2)
        self.optionbox3Content.addLayout(box2line3)
        self.optionbox3Content.addLayout(box2line4)
        self.optionbox3Content.addLayout(box2line5)
        self.optionbox3.setLayout(self.optionbox3Content)

    def optionbox_questionnaires_postoperative(self, layout_general):
        """optionbox containing the postopreative tests that are being applied"""

        def create_label_and_line_edit_pair(label_text, line_edit_width=50):
            label = QLabel(label_text)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setFixedWidth(130)
            line_edit = QLineEdit()
            line_edit.setEnabled(False)
            line_edit.setFixedWidth(line_edit_width)
            return label, line_edit

        def create_horizontal_layout(*widgets):
            layout = QHBoxLayout()
            for widget in widgets:
                layout.addWidget(widget)
                if widgets.index(widget) % 2 != 0 and widgets.index(widget) != 0:
                    layout.addItem(QSpacerItem(30, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
            layout.addStretch()
            return layout

        self.optionbox_tests = QGroupBox('Tests')
        self.optionbox_tests.setMaximumWidth(1200)
        self.optionbox_tests_content = QVBoxLayout(self.optionbox_tests)
        layout_general.addWidget(self.optionbox_tests)

        # First line of the optionbox
        updrs_i, self.lineEditUPDRSI = create_label_and_line_edit_pair('UPDRS I')
        updrs_iv, self.lineEditUPDRSIV = create_label_and_line_edit_pair('UPDRS IV')
        tss, self.lineEditTSS = create_label_and_line_edit_pair('TSS')
        cgic_pat, self.lineEditCGICPat = create_label_and_line_edit_pair('CGIC patient')
        cgic_clinician, self.lineEditCGICClinician = create_label_and_line_edit_pair('CGIC clinician')

        testbox_line1 = create_horizontal_layout(updrs_i, self.lineEditUPDRSI, updrs_iv, self.lineEditUPDRSIV,
                                                 tss, self.lineEditTSS, cgic_pat, self.lineEditCGICPat,
                                                 cgic_clinician, self.lineEditCGICClinician)

        # Second line of the optionbox
        updrs_on, self.lineEditUPDRSON = create_label_and_line_edit_pair('UPDRS On')
        updrs_ii, self.lineEditUPDRSII = create_label_and_line_edit_pair('UPDRS II')
        hruq, self.lineEditHRUQ = create_label_and_line_edit_pair('HRUQ')
        moca, self.lineEditMoCa = create_label_and_line_edit_pair('MoCa')
        mmst, self.lineEditMMST = create_label_and_line_edit_pair('MMST')


        # Create second line layout
        testbox_line2 = create_horizontal_layout(
            updrs_on, self.lineEditUPDRSON,
            updrs_ii, self.lineEditUPDRSII,
            hruq, self.lineEditHRUQ,
            moca, self.lineEditMoCa,
            mmst, self.lineEditMMST
        )

        # Third line of the optionbox
        bdi_ii, self.lineEditBDIII = create_label_and_line_edit_pair('BDI-II')
        nmsq, self.lineEditNMSQ = create_label_and_line_edit_pair('NMSQ')
        updrs_off, self.lineEditUPDRSOFF = create_label_and_line_edit_pair('UPDRS Off')
        hy, self.lineEditHY = create_label_and_line_edit_pair('H&Y')
        eq5d, self.lineEditEQ5D = create_label_and_line_edit_pair('EQ5D')


        # Create third line layout
        testbox_line3 = create_horizontal_layout(
            bdi_ii, self.lineEditBDIII,
            nmsq, self.lineEditNMSQ,
            updrs_off, self.lineEditUPDRSOFF,
            hy, self.lineEditHY,
            eq5d, self.lineEditEQ5D
        )

        # fourth line of the optionbox
        demtect, self.lineEditDemTect = create_label_and_line_edit_pair('DemTect')
        pdq8, self.lineEditPDQ8 = create_label_and_line_edit_pair('PDQ8')
        pdq39, self.lineEditPDQ39 = create_label_and_line_edit_pair('PDQ39')
        se, self.lineEditSE = create_label_and_line_edit_pair('S&E')
        uddrs_on, self.lineEditUDDRSOn = create_label_and_line_edit_pair('UDDRS On')


        # Create fourth line layout
        testbox_line4 = create_horizontal_layout(
            demtect, self.lineEditDemTect,
            pdq8, self.lineEditPDQ8,
            pdq39, self.lineEditPDQ39,
            se, self.lineEditSE,
            uddrs_on, self.lineEditUDDRSOn
        )

        #fifth line of optionbox
        trs_on, self.lineEditTRSOn = create_label_and_line_edit_pair('TRS On')
        uddrs_off, self.lineEditUDDRSOff = create_label_and_line_edit_pair('UDDRS Off')
        trs_off, self.lineEditTRSOff = create_label_and_line_edit_pair('TRS Off')

        # Create fifth line layout
        testbox_line5 = create_horizontal_layout(
            trs_on, self.lineEditTRSOn,
            uddrs_off, self.lineEditUDDRSOff,
            trs_off, self.lineEditTRSOff
        )

        # Add layouts to option box content
        self.optionbox_tests_content.addLayout(testbox_line1)
        self.optionbox_tests_content.addLayout(testbox_line2)
        self.optionbox_tests_content.addLayout(testbox_line3)
        self.optionbox_tests_content.addLayout(testbox_line4)
        self.optionbox_tests_content.addLayout(testbox_line5)

        self.optionbox_tests.setLayout(self.optionbox_tests_content)

    def create_bottom_buttons_postoperative(self, layout_general):
        """Creates two buttons a) to read medication and b) to save settings and exit GUI """
        self.ButtonEnterMedication = QPushButton('Open GUI \nMedication')
        self.ButtonEnterDBSsettings = QPushButton('Open GUI \nDBS settings')
        self.button_save = QPushButton('Save')
        self.button_save_return = QPushButton('Save and \nReturn')

        # Set fixed size for all buttons
        button_width = 200
        button_height = 75

        self.ButtonEnterMedication.setFixedSize(button_width, button_height)
        self.button_save.setFixedSize(button_width, button_height)
        self.ButtonEnterDBSsettings.setFixedSize(button_width, button_height)
        self.button_save_return.setFixedSize(button_width, button_height)

        hlay_bottom = QHBoxLayout()
        hlay_bottom.addStretch(5)
        hlay_bottom.addWidget(self.ButtonEnterMedication)
        hlay_bottom.addWidget(self.ButtonEnterDBSsettings)
        hlay_bottom.addWidget(self.button_save)
        hlay_bottom.addWidget(self.button_save_return)
        hlay_bottom.addStretch(1)
        layout_general.addLayout(hlay_bottom, 4, 0, 1, 3)

        self.read_content_csv()

    def connect_button_actions(self):
        """Defines the actions that are taken once a button is pressed or specific input is made"""
        self.lineEditreason.currentIndexChanged.connect(self.update_context)
        self.ButtonEnterMedication.clicked.connect(self.onClickedMedication)
        self.ButtonEnterDBSsettings.clicked.connect(self.onClickedDBSsettings)
        self.button_save.clicked.connect(self.onClickedSave)
        self.button_save_return.clicked.connect(self.onClickedSaveReturn)

    # From here on, you can find the function of the buttons, etc.
    def fill_combobox(self, new_date = None): #GP: new_date als neue Variable (s.u.)
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
        print(unique_dates)
        #GP: Set the current index to the newly added date if it exists
        #GP: stellt direkt nach Eingabe des Datums die optionbox auf das Datum ein
        #GP: direkte Eingabe möglich, ohne nochmal manuell das Datum zu ändern
        if new_date:
            self.lineEditreason.setCurrentText(new_date)

    # ====================   Defines what happens when ComboBox is modified      ====================
    def set_widget_text(self, widget, value):
        """Set widget text, handling NaN values. Generic function used in read_content_csv"""
        widget.setText(str(value)) if not pds.isna(value) else widget.setText('')

    def update_line_edits(self, line_edits, data_row):
        """Update line edits with corresponding data from the row. Generic function used in read_content_csv"""
        for line_edit, column_name in line_edits:
            self.set_widget_text(line_edit, data_row[column_name])

    def read_content_csv(self):
        """After selecting the reason for visit, data is read from the csv-file [preoperative] if available"""
        df_subj = General.import_dataframe(f"{self.date}.csv", separator_csv=',')

        # GP: postoperative.csv is always empty the first time you enter data

        if not os.path.isfile(f'{FILEDIR}/{self.date}.csv'):
            Output.msg_box(text='Something went wrong when looking for the data',
                           title=f'{self.date}.csv not found in the folder: {FILEDIR}',
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
            (self.lineEditLast_Revision, "Last_revision_postop"),
            (self.lineEditOutpatient_Contact, "Outpatient_contact_postop")
        ]

        self.update_line_edits(line_edits_upper_right, row)

        # Upper right
        self.set_widget_text(self.lineEditAdverse_Event, row["AE_postop"])

        # Middle right
        line_edits_middle_right = [
            (self.lineEditUPDRSI, "UPDRS1_postop"),
            (self.lineEditUPDRSIV, "UPDRS4_postop"),
            (self.lineEditTSS, "TSS_postop"),
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


        # CheckBoxes
        self.ReportNeurCheck.setChecked(bool(row["Report_File_NCh_postop"]))
        self.ReportNeurosurgeryCheck.setChecked(bool(row["Report_File_NR_postop"]))
        self.PatProgrammerCheck.setChecked(bool(row["Using_Programmer_postop"]))
        self.PostopCTCheck.setChecked(bool(row["CTscan_postop"]))
        self.PlannedVisitCheck.setChecked(bool(row["Planned_Visit_postop"]))


    @staticmethod
    def set_checkbox_state(state, *checkboxes):
        """this function enables checkboxes, needed to avoid data entries without first selecting reason"""
        for checkbox in checkboxes:
            checkbox.setEnabled(state)

    @staticmethod
    def set_lineedit_state(state, *line_edits):
        """this function enables LineEdits, needed to avoid data entries without first selecting reason"""
        for line_edit in line_edits:
            line_edit.setEnabled(state)

    def update_context(self):
        """updates the context according to what was selected in the ComboBox"""

        selected_item1 = self.lineEditreason.currentText()
        optionboxes = Content.find_lineedit_objects(
            [self.optionbox_tests,
             self.optionbox_dates_postoperative,
            ])
        checkboxes = Content.find_checkbox_objects(
            [self.PostopCTCheck,
             self.PlannedVisitCheck,
             self.ReportNeurCheck,
             self.ReportNeurosurgeryCheck,
             self.PatProgrammerCheck])

        if selected_item1 != 'Enter new data' and selected_item1 != 'Please select date or enter new data': # and selected_item2 != ''):
            self.set_lineedit_state(True, *optionboxes)
            self.set_checkbox_state(True, *checkboxes)
        else:
            self.set_lineedit_state(False, *optionboxes)
            self.set_checkbox_state(False, *checkboxes)

        if self.lineEditreason.currentText() == 'Please select date or enter new data':
            pass
        elif self.lineEditreason.currentText() == 'Enter new data':
            self.reason_visit = Output.open_input_dialog_postoperative(self)
            if self.reason_visit != None: #GP wenn open_input_dialog None ausgibt, wird None als date gespeichert
                data_frame = General.import_dataframe(f"{self.date}.csv", separator_csv=',')
                subj_details = General.read_current_subj()

                # GP: checking BEFORE new data is added to postoperative.csv
                match = re.search(r'^(pre|intra|post)op', self.date)
                filtered_df = data_frame[data_frame['PID_ORBIS'] == subj_details.pid[0]]

                if not filtered_df.empty:
                    list_of_dates = filtered_df['Reason_postop'].tolist()
                    if self.reason_visit in list_of_dates:
                        Output.msg_box('There is already an identical entry for this subject. Please enter a different reason',
                                       title=f'Warning, double entry for subj {subj_details.id[0]}')
                        self.fill_combobox()
                        return

                #if any(filtered_df['Reason_{}'.format(self.date)].isin([self.reason_visit])):
                #    Output.msg_box(
                #        'There is already an identical entry for this subject. Please enter a different reason',
                #        title=f'Warning, double entry for subj {subj_details.id[0]}')
                #    self.fill_combobox()
                #    return

                data_frame.loc[len(data_frame), ['ID', 'PID_ORBIS', 'Reason_{}'.format(match.group())]] = [subj_details.id[0],
                                                                                                           subj_details.pid[0],
                                                                                                           self.reason_visit]

                data_frame = data_frame.replace(['nan', ''], [np.nan, np.nan])
                data_frame = data_frame.applymap(lambda x: str(x).replace(';', ' -'))
                data_frame.to_csv(os.path.join(FILEDIR, f"{self.date}.csv"), index=False)

                self.save_data2csv()
                new_date = self.reason_visit

                self.fill_combobox(new_date)
                self.read_content_csv()
            else:
                self.lineEditreason.setCurrentText('Please select date or enter new data')
                pass
        else:
            self.reason_visit = self.lineEditreason.currentText()
            self.read_content_csv()
            #self.save_data2csv() #needed?

    # ====================   Defines actions when buttons are pressed      ====================
    @QtCore.pyqtSlot()
    def onClickedMedication(self):
        """shows the medication dialog when button is pressed; former implementation with creating GUI was replaced with
        show/hide GUI which is initiated at beginning"""
        self.dialog_medication = MedicationDialog(parent=self, visit=self.date)
        self.dialog_medication.show()

    @QtCore.pyqtSlot()
    def onClickedDBSsettings(self):
        """shows the DBSsettiongs dialog when button is pressed"""
        try:
            reason = self.reason_visit
        except AttributeError:
            QMessageBox.warning(self, 'No reason selected', 'Please select a date or create a new date before continuing.')
            return
        print(reason)
        self.dialog_DBSsettings = DBSsettingsDialog(parent=self, visit=self.date, reason = reason)  # creates medication dialog
        self.dialog_DBSsettings.show()

    @QtCore.pyqtSlot()
    def onClickedSave(self):
        #self.check_IPG_selection()
        self.save_data2csv()

    @QtCore.pyqtSlot()
    def onClickedSaveReturn(self):
        """Saves the data passed into the GUI form and returns to previous Window."""
        self.save_data2csv()
        self.close()

    def save_data2csv(self):
        current_subj = General.read_current_subj()
        subject_id = current_subj['id'][0]
        df_general = Clean.extract_subject_data(subject_id)
        match = re.search(r'^(pre|intra|post)op', self.date)
        try:
            reason_test = self.reason_visit
        except AttributeError:
            QMessageBox.warning(self, 'No Date Selected', 'Please select a date or enter new data before saving.')
            return

        df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=',')
        try:
            df_subj = df.iloc[df.index[df['Reason_postop'] == self.reason_visit][0], :].to_dict()
        except IndexError:
            df_subj = {k: '' for k in df.columns}

        df_general.reset_index(inplace=True, drop=True)
        df_subj['ID'] = General.read_current_subj().id[0]
        df_subj['PID_ORBIS'] = df_general.iloc[0, :]['PID_ORBIS']
        df_subj['Gender'] = df_general['gender'][0]
        df_subj['Diagnosis_{}'.format(match.group())] = df_general['diagnosis'][0]

        line_edits = [
            (self.lineEditAdmission_Nch, 'Admission_NCh'),
            (self.lineEditAdmission_NR, 'Admission_NR'),
            (self.lineEditDismission_Nch, 'Dismissal_NCh'),
            (self.lineEditDismission_NR, 'Dismissal_NR'),
            (self.lineEditSurgery, 'Surgery_Date'),
            (self.lineEditLast_Revision, 'Last_revision'),
            (self.lineEditOutpatient_Contact, 'Outpatient_contact'),
        ]

        # Iterate over the list and update the DataFrame
        for line_edit, column_name in line_edits:
            column_key = f'{column_name}_{match.group()}'
            df_subj[column_key] = line_edit.text()

        df_subj['AE_{}'.format(match.group())] = self.lineEditAdverse_Event.text()

        df_subj['UPDRS1_{}'.format(match.group())] = self.lineEditUPDRSI.text()
        df_subj['UPDRS4_{}'.format(match.group())] = self.lineEditUPDRSIV.text()
        df_subj['TSS_postop'] = self.lineEditTSS.text()
        df_subj['CGIC_patient_postop'] = self.lineEditCGICPat.text()
        df_subj['CGIC_clinician_caregiver_postop'] = self.lineEditCGICClinician.text()
        df_subj["UPDRS_On_postop"] = self.lineEditUPDRSON.text()
        df_subj["UPDRSII_postop"] = self.lineEditUPDRSII.text()
        df_subj["UPDRS_Off_postop"] = self.lineEditUPDRSOFF.text()
        df_subj["H&Y_postop"] = self.lineEditHY.text()
        df_subj["HRUQ_postop"] = self.lineEditHRUQ.text()
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

        checkbox_cols = [("ReportNeurCheck", "Report_File_NCh_postop"),
                         ("ReportNeurosurgeryCheck", "Report_File_NR_postop"),
                         ("PatProgrammerCheck", "Using_Programmer_postop"),
                         ("PostopCTCheck", "CTscan_postop"),
                         ("PlannedVisitCheck", "Planned_Visit_postop")]

        for checkbox, col_name in checkbox_cols:
            if getattr(self, checkbox).isChecked():
                df_subj[col_name] = 1
            else:
                df_subj[col_name] = 0
            # Incorporate the [df_subj] dataframe into the entire dataset and save as csv

        indices_to_update = df.index[df['Reason_postop'] == self.reason_visit]

        if not indices_to_update.empty:
            index_to_update = indices_to_update[0]
            df.loc[index_to_update] = df_subj
        else:
            # Handle the case when the index is not found
            print(f"Index for Reason_postop '{self.reason_visit}' not found.")

        df.to_csv(Path(f"{FILEDIR}/{self.date}.csv"), index=False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = PostoperativeDialog()
    dlg.show()
    sys.exit(app.exec_())
