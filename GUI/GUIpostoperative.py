#!/usr/bin/env python3
import os, sys, re
import numpy as np
import pandas as pds
from PyQt5 import QtCore
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QCheckBox, QMessageBox, QSpacerItem, \
    QSizePolicy, QInputDialog
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

        self.setWindowTitle(f'Please insert the postoperative information (PID: {str(subj_details.pid.iloc[0]).strip("PID_")})')
        self.setGeometry(200, 100, 280, 170)
        self.setMinimumWidth(1800)
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

        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)

    def optionbox_dates_postoperative(self, layout_general):
        """creates upper left optionbox in which important dates are added"""

        def create_line_edit_for_dates(label_text, line_edit_width=180, label_width=250):
            label = QLabel(f'{label_text}:\t\t')
            label.setFixedWidth(label_width)
            line_edit = QLineEdit()
            line_edit.setPlaceholderText('DD/MM/YYYY')
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
        self.optionbox_dates_postoperative.setMaximumWidth(500)
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
        #self.optionbox_visit_information.setMaximumWidth(1200)
        layout_general.addWidget(self.optionbox_visit_information, 0, 1)
        self.optionbox_visit_informationContent = QVBoxLayout(self.optionbox_visit_information)

        self.subj_reason = QLabel('Follow-Up-Date:\t')
        self.lineEditreason = QComboBox()
        self.lineEditreason.setFixedWidth(400)
        self.fill_combobox()

        self.button_change_delete_date = QPushButton('Change/Delete Date')  # New button
        self.button_change_delete_date.setFixedWidth(220)  # Set the width for the new button

        reason_layout = QHBoxLayout()
        reason_layout.addWidget(self.subj_reason)
        reason_layout.addWidget(self.lineEditreason)
        reason_layout.addWidget(self.button_change_delete_date)  # Add new button to layout
        self.button_change_delete_date.setEnabled(False)
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
        self.optionbox3.setMaximumWidth(500)
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
        """Optionbox containing the postoperative tests that are being applied"""

        def create_label_and_line_edit_pair(col, label_text, line_edit_width=60):
            if col == 0:
                label = QLabel(f"{label_text}:")
            else:
                label = QLabel(f"\t{label_text}:")
            label.setAlignment(QtCore.Qt.AlignRight)
            line_edit = QLineEdit()
            line_edit.setEnabled(False)
            line_edit.setFixedWidth(line_edit_width)
            return label, line_edit

        def add_widgets_to_grid_layout(layout, row, col, *widgets):
            for i, widget in enumerate(widgets):
                layout.addWidget(widget, row, col + i)

        self.optionbox_tests = QGroupBox('Tests')
        self.optionbox_tests_content = QVBoxLayout(self.optionbox_tests)
        layout_general.addWidget(self.optionbox_tests)


        grid_layout = QGridLayout()

        # Create label and line edit pairs
        questionnaires_content = {
            'UPDRS I': 'lineEditUPDRSI',
            'UPDRS IV': 'lineEditUPDRSIV',
            'TSS': 'lineEditTSS',
            'CGIC patient': 'lineEditCGICPat',
            'CGIC clinician': 'lineEditCGICClinician',
            'UPDRS On': 'lineEditUPDRSON',
            'UPDRS II': 'lineEditUPDRSII',
            'HRUQ': 'lineEditHRUQ',
            'MoCa': 'lineEditMoCa',
            'MMST': 'lineEditMMST',
            'BDI-II': 'lineEditBDIII',
            'NMSQ': 'lineEditNMSQ',
            'UPDRS Off': 'lineEditUPDRSOFF',
            'H&Y': 'lineEditHY',
            'EQ5D': 'lineEditEQ5D',
            'DemTect': 'lineEditDemTect',
            'PDQ8': 'lineEditPDQ8',
            'PDQ39': 'lineEditPDQ39',
            'S&E': 'lineEditSE',
            'UDDRS On': 'lineEditUDDRSOn',
            'TRS On': 'lineEditTRSOn',
            'UDDRS Off': 'lineEditUDDRSOff',
            'TRS Off': 'lineEditTRSOff'
        }

        # Add widgets to grid layout
        row = 0
        col = 0
        for label_text, line_edit_name in questionnaires_content.items():
            label, line_edit = create_label_and_line_edit_pair(col, label_text)
            setattr(self, line_edit_name, line_edit)
            add_widgets_to_grid_layout(grid_layout, row, col, label, line_edit)
            col += 2
            if col >= 8:  # 4 pairs per row
                col = 0
                row += 1


        # Add grid layout to option box content
        self.optionbox_tests_content.addLayout(grid_layout)
        self.optionbox_tests.setLayout(self.optionbox_tests_content)


    def create_bottom_buttons_postoperative(self, layout_general):
        """Creates two buttons a) to read medication and b) to save settings and exit GUI """
        self.ButtonEnterMedication = QPushButton('Postoperative\nMedication')
        self.ButtonEnterDBSsettings = QPushButton('Postoperative\nDBS settings')
        self.button_save = QPushButton('Save')
        self.button_save_return = QPushButton('Save and\nReturn')

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

        self.ButtonEnterMedication.setEnabled(False)
        self.ButtonEnterDBSsettings.setEnabled(False)
        self.button_save.setEnabled(False)
        self.button_save_return.setEnabled(False)

        self.read_content_csv()

    def connect_button_actions(self):
        """Defines the actions that are taken once a button is pressed or specific input is made"""
        self.lineEditreason.currentIndexChanged.connect(self.update_context)
        self.ButtonEnterMedication.clicked.connect(self.onClickedMedication)
        self.ButtonEnterDBSsettings.clicked.connect(self.onClickedDBSsettings)
        self.button_save.clicked.connect(self.onClickedSave)
        self.button_save_return.clicked.connect(self.onClickedSaveReturn)
        self.button_change_delete_date.clicked.connect(self.onClickedChangeDeleteDate)  # Connect new button

    # From here on, you can find the function of the buttons, etc.
    def fill_combobox(self, new_date = None): #GP: new_date als neue Variable (s.u.)
        """fills ComboBox for postoperative visits"""
        items_available = Content.extract_postoperative_dates()
        default_options = ['Please select date or enter new data', 'Enter new data']
        items_available = default_options if not items_available else items_available + default_options
        unique_dates = list(set(items_available))
        print(unique_dates)

        def custom_sort(item):
            if item in default_options:
                return (default_options.index(item), item)
            else:
                try:
                    return (len(default_options), datetime.strptime(item, '%d/%m/%Y'))
                except ValueError:
                    return (len(default_options), item)


        # Add items to ComboBox
        self.lineEditreason.clear()
        self.lineEditreason.addItems(sorted(unique_dates, key=custom_sort))

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
            row = pds.Series([np.nan for _ in range(len(df_subj_filtered.columns))], index=df_subj_filtered.columns)

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

        # Check if any line edits are still empty
        if any(line_edit.text() == '' for line_edit, column_name in line_edits_upper_right):
            intraoperative_dates = self.check_intraoperative_dates()
            for line_edit, column_name in line_edits_upper_right:
                if line_edit.text() == '' and column_name in intraoperative_dates:
                    self.set_widget_text(line_edit, intraoperative_dates[column_name])

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

        if selected_item1 != 'Enter new data' and selected_item1 != 'Please select date or enter new data':
            self.set_lineedit_state(True, *optionboxes)
            self.set_checkbox_state(True, *checkboxes)
            self.ButtonEnterMedication.setEnabled(True)
            self.ButtonEnterDBSsettings.setEnabled(True)
            self.button_save.setEnabled(True)
            self.button_save_return.setEnabled(True)
            self.button_change_delete_date.setEnabled(True)
            self.current_date = self.lineEditreason.currentText()
            #Needed to edit current_date:
            data_frame = General.import_dataframe(f"{self.date}.csv", separator_csv=',')
            subj_details = General.read_current_subj()
            filtered_df = data_frame[data_frame['PID_ORBIS'] == subj_details.pid[0]]
            self.list_of_dates = filtered_df['Reason_postop'].tolist()

        else:
            self.set_lineedit_state(False, *optionboxes)
            self.set_checkbox_state(False, *checkboxes)
            self.ButtonEnterMedication.setEnabled(False)
            self.ButtonEnterDBSsettings.setEnabled(False)
            self.button_save.setEnabled(False)
            self.button_save_return.setEnabled(False)
            self.button_change_delete_date.setEnabled(False)

        if self.lineEditreason.currentText() == 'Please select date or enter new data':
            pass

        elif self.lineEditreason.currentText() == 'Enter new data':
            self.reason_visit = Output.open_input_dialog_postoperative(self)
            if self.reason_visit is not None: #GP wenn open_input_dialog None ausgibt, wird None als date gespeichert
                data_frame = General.import_dataframe(f"{self.date}.csv", separator_csv=',')
                subj_details = General.read_current_subj()
                general_data = pds.read_csv(os.path.join(FILEDIR, 'general_data.csv'))
                subj_general_data = general_data[general_data['ID'] == subj_details.id[0]].iloc[0]

                match = re.search(r'^(pre|intra|post)op', self.date)
                filtered_df = data_frame[data_frame['PID_ORBIS'] == subj_details.pid[0]]

                if not filtered_df.empty:
                    list_of_dates = filtered_df['Reason_postop'].tolist()
                    if self.reason_visit in list_of_dates:
                        Output.msg_box(
                            'There is already an identical entry for this subject. Please enter a different reason',
                            title=f'Warning, double entry for subj {subj_details.id[0]}')
                        self.fill_combobox()
                        return

                new_row = {
                    'ID': subj_details.id[0],
                    'PID_ORBIS': subj_details.pid[0],
                    f'Reason_{match.group()}': self.reason_visit,
                    'Gender': subj_general_data['gender'],
                    'Diagnosis_postop': subj_general_data['diagnosis']
                }

                #Checking for existing data
                existing_data_postop = filtered_df.iloc[0] if not filtered_df.empty else {}
                new_row['Implanted_IPG'] = existing_data_postop.get('Implanted_IPG', np.nan)
                new_row['Lead_manufacturer'] = existing_data_postop.get('Lead_manufacturer', np.nan)
                new_row['implanted_leads'] = existing_data_postop.get('implanted_leads', np.nan)

                #Checking intraoperative.csv for preexisting data
                if all(pds.isna(new_row[item]) or new_row[item] in ["nan", ""] for item in ['Implanted_IPG', 'Lead_manufacturer', 'implanted_leads']):
                    try:
                        intraoperative_df = General.import_dataframe("intraoperative.csv", separator_csv=',')
                        existing_data_intraop = intraoperative_df[intraoperative_df['PID_ORBIS'] == subj_details.pid[0]]
                        new_row['Implanted_IPG'] = existing_data_intraop['Implanted_IPG'].iloc[0]
                        new_row['Lead_manufacturer'] = existing_data_intraop['Lead_manufacturer'].iloc[0]
                        new_row['implanted_leads'] = existing_data_intraop['implanted_leads'].iloc[0]
                        print(existing_data_intraop['implanted_leads'])
                    except IndexError:
                        pass

                checkboxes_postop = ["Report_File_NR_postop",
                                     "Report_File_NCh_postop",
                                     "Using_Programmer_postop",
                                     "CTscan_postop",
                                     "Planned_Visit_postop"]
                for checkbox in checkboxes_postop:
                    new_row[checkbox] = 0

                for key, dtype in dtype_dict_postoperative.items():
                    if key not in new_row:
                        if dtype == "float64":
                            new_row[key] = np.nan
                        elif dtype == "int64":
                            new_row[key] = pds.NA
                        elif dtype == "object":
                            new_row[key] = np.nan

                new_row_df = pds.DataFrame([new_row]).dropna(axis=1, how='all')
                data_frame = pds.concat([data_frame, new_row_df], ignore_index=True)
                data_frame.to_csv(os.path.join(FILEDIR, f"{self.date}.csv"), index=False)

                new_date = self.reason_visit

                self.fill_combobox(new_date)
                self.read_content_csv()

        else:
            self.reason_visit = self.lineEditreason.currentText()
            self.read_content_csv()

    # ====================   Defines actions when buttons are pressed      ====================
    @QtCore.pyqtSlot()
    def onClickedChangeDeleteDate(self):
        """Handles the action for changing or deleting the date."""
        current_date = self.current_date

        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle('Change or Delete Date')
        msg_box.setText(f'Do you want to change or delete the date: {current_date}?')
        change_button = msg_box.addButton('Change Date', QMessageBox.ActionRole)
        delete_button = msg_box.addButton('Delete Date', QMessageBox.ActionRole)
        cancel_button = msg_box.addButton(QMessageBox.Cancel)

        msg_box.exec_()

        if msg_box.clickedButton() == change_button:
            new_date, ok = QInputDialog.getText(self, 'Change Date', 'Enter new date (DD/MM/YYYY):')
            if ok and new_date:
                formatted_date = General.validate_and_format_dates(new_date)
                if formatted_date == 'Invalid date format':
                    QMessageBox.warning(self, 'Invalid Date',
                                        'The entered date is invalid. Please enter a date in the format DD/MM/YYYY.')
                else:
                    self.update_date_in_csv(current_date, formatted_date)
                    self.fill_combobox(formatted_date)
                    self.read_content_csv()
        elif msg_box.clickedButton() == delete_button:
            self.delete_date_from_csv(current_date)
            self.fill_combobox()
            self.read_content_csv()

    def update_date_in_csv(self, old_date, new_date):
        """Updates the date in the CSV file."""
        df = General.import_dataframe(f"{self.date}.csv", separator_csv=',')
        # Check if the new date already exists
        if new_date in self.list_of_dates and new_date != old_date:
            QMessageBox.warning(self, 'Duplicate Date',
                                'The entered date already exists. Please enter a different date.')
            return
        df.loc[df['Reason_postop'] == old_date, 'Reason_postop'] = new_date
        df.to_csv(Path(f"{FILEDIR}/{self.date}.csv"), index=False)

    def delete_date_from_csv(self, date_to_delete):
        """Deletes the row with the specified date from the CSV file."""
        df = General.import_dataframe(f"{self.date}.csv", separator_csv=',')
        df = df[df['Reason_postop'] != date_to_delete]
        df.to_csv(Path(f"{FILEDIR}/{self.date}.csv"), index=False)

    def check_intraoperative_dates(self):
        """Checks for available dates in intraoperative.csv for the current subject."""
        date_list = {
            "Admission_NCh_postop": "admission_Nch_intraop",
            "Admission_NR_postop": "Admission_intraop",
            "Dismissal_NCh_postop": "dismissal_NCh_intraop",
            "Dismissal_NR_postop": "Dismissal_intraop",
            "Surgery_Date_postop": "surgery_date_intraop"
        }

        subj_details = General.read_current_subj()
        intraoperative_df = General.import_dataframe("intraoperative.csv", separator_csv=',')
        filtered_df = intraoperative_df[intraoperative_df['PID_ORBIS'] == subj_details.pid[0]]

        available_dates = {}
        for postop_col, intraop_col in date_list.items():
            if intraop_col in filtered_df.columns:
                available_dates[postop_col] = filtered_df[intraop_col].values[0] if not filtered_df[
                    intraop_col].isna().all() else ''
        print(available_dates)
        return available_dates

    @QtCore.pyqtSlot()
    def onClickedMedication(self):
        """shows the medication dialog when button is pressed; former implementation with creating GUI was replaced with
        show/hide GUI which is initiated at beginning"""
        self.dialog_medication = MedicationDialog(parent=self, visit=self.date, postop_date=self.reason_visit)
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
            df_subj[col_name] = 1 if getattr(self, checkbox).isChecked() else 0

        for key, dtype in dtype_dict_postoperative.items():
            if key in df_subj:
                try:
                    if dtype == "float64":
                        df_subj[key] = str(df_subj[key]) if not (
                                pds.isna(df_subj[key]) or str(df_subj[key]) in ["", "nan"]) else np.nan
                    elif dtype == "int64":
                        df_subj[key] = str(df_subj[key]) if not (
                                pds.isna(df_subj[key]) or str(df_subj[key]) in ["", "nan"]) else pds.NA
                    elif dtype == "object":
                        df_subj[key] = str(df_subj[key]) if not (
                                    pds.isna(df_subj[key]) or str(df_subj[key]) in ["", "nan"]) else ""
                    df_subj[key] = pds.array([df_subj[key]], dtype=dtype)[0]
                except (ValueError, TypeError):
                    print("Error", dtype, df_subj[key])
                    if dtype == "float64":
                        df_subj[key] = np.nan
                    elif dtype == "int64":
                        df_subj[key] = pds.NA
                    elif dtype == "object":
                        df_subj[key] = ""

        try:
            idx2replace = df.index[df['Reason_postop'] == self.reason_visit][0]
            for key, value in df_subj.items():
                if pds.isna(value) or value in ["", "nan"]:
                    if key in dtype_dict_postoperative.keys():
                        df[key] = df[key].astype(dtype_dict_postoperative[key])
                        df.at[idx2replace, key] = value
                else:
                    if key in dtype_dict_postoperative.keys():
                        df[key] = df[key].astype(dtype_dict_postoperative[key])
                        df.at[idx2replace, key] = value
                    df.at[idx2replace, key] = value
        except IndexError:
            df_subj = pds.DataFrame(df_subj, index=[df.index.shape[0]])
            df = pds.concat([df, df_subj], ignore_index=True)

        df.to_csv(Path(f"{FILEDIR}/{self.date}.csv"), index=False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = PostoperativeDialog()
    dlg.show()
    sys.exit(app.exec_())
