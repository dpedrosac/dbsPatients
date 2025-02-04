#!/usr/bin/env python3
import sys
import numpy as np
import pandas as pds
from PyQt5 import QtCore
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QGridLayout, QLineEdit, QLabel, QCheckBox, QMessageBox
from GUImedication import MedicationDialog
from utils.helper_functions import General, Content, Clean, Output
from dependencies import FILEDIR, dtype_dict_preoperative

pds.options.mode.chained_assignment = None  # default='warn' cf.
# https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas

class PreoperativeDialog(QDialog):
    """Dialog to introduce all important information of preoperative data ('Indikationsprüfung')"""

    def __init__(self, parent=None, textwidth=300):
        """Initializer."""
        super(PreoperativeDialog, self).__init__(parent)
        self.dialog_medication, self.content_widgets = None, None
        self.date = 'preoperative'  # defines the date at which data are taken from/saved at
        self.setup_ui()
        #self.showMaximized()

    def setup_ui(self):
        self.initialize_content()
        self.setup_general_layout()

    def setup_general_layout(self):
        """Defines the general layout for the GUI"""
        subj_details = General.read_current_subj()  # reads information for the subject last being processed
        General.synchronize_data_with_general(self.date, subj_details.id[0],
                                              messagebox=False)  # for identical general columns in 'preoperative.csv'

        #self.create_medication_dialog()

        self.setWindowTitle(f'Please insert the preoperative patient data (PID: {str(subj_details.pid.iloc[0]).strip("PID_")})')
        self.setGeometry(200, 100, 280, 170)
        self.move(400, 200)

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # Option boxes appearing in the preoperative GUI
        # Create optionbox for important dates
        self.optionbox_dates_preoperative(layout_general)

        # Create optionbox for reports and study participation
        self.optionbox_reports_preoperative(layout_general)

        # Create optionbox for scales and questionnaires during or visit
        self.optionbox_questionnaires_preoperative(layout_general)

        # Create optionbox for tests performed during preoperative visits
        self.optionbox_preoperative_other(layout_general)

        # Create buttons at the bottom of the GUI
        self.create_bottom_buttons_preoperative(layout_general)

        # Connect button actions that are needed so that everything works
        self.connect_button_actions()

        # Obtain data that has been stored already in preoperative.csv
        self.updatePreoperativeData()

        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, True)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, True)

    def initialize_content(self):
        """Initializes the content that may be needed later for reading or saving data from/to csv-files"""

        self.content_widgets = {
            'First_Diagnosed_preop': 'lineEditFirstDiagnosed',
            'Admission_preop': 'lineEditAdmNeurIndCheck',
            'Dismissal_preop': 'lineEditDismNeurIndCheck',
            'Outpat_Contact_preop': 'lineEditOutpatientContact',
            'nch_preop': 'lineEditNsurgContact',
            'DBS_Conference_preop': 'lineEditDBSconference',
            'H&Y_preop': 'hy',
            'UPDRS_On_preop': 'updrsON',
            'UPDRS_Off_preop': 'updrsOFF',
            'UPDRSII_preop': 'updrsII',
            'HRUQ_preop': 'hruq',
            'MoCa_preop': 'moca',
            'MMST_preop': 'mmst',
            'BDI2_preop': 'bdi2',
            'NMSQ_preop': 'nmsq',
            'EQ5D_preop': 'eq5d',
            'DemTect_preop': 'demtect',
            'PDQ8_preop': 'pdq8',
            'PDQ39_preop': 'pdq39',
            'S&E_preop': 'se',
        }

    def optionbox_dates_preoperative(self, layout_general):
        """creates upper left optionbox in which important dates are added"""

        def create_line_edit_for_dates(label_text, line_edit_width=180, label_width=250):
            label = QLabel(f'{label_text}:')
            label.setFixedWidth(label_width)
            line_edit = QLineEdit()
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

        self.optionbox_dates_preoperative = QGroupBox('Diagnosis and indication check')
        self.optionbox_dates_preoperative_Content = QVBoxLayout(self.optionbox_dates_preoperative)
        layout_general.addWidget(self.optionbox_dates_preoperative, 0, 0)

        date_labels = [
            ('First diagnosed', 'lineEditFirstDiagnosed'),
            ('Admission Neurology', 'lineEditAdmNeurIndCheck'),
            ('Dismission Neurology', 'lineEditDismNeurIndCheck'),
            ('Outpatient contact', 'lineEditOutpatientContact'),
            ('Neurosurgical contact', 'lineEditNsurgContact'),
            ('DBS conference', 'lineEditDBSconference')
        ]

        for i in range(0, len(date_labels), 2):
            horizontal_layout = QHBoxLayout()
            for label_text, line_edit_name in date_labels[i:i + 2]:
                label, line_edit = create_line_edit_for_dates(label_text)
                setattr(self, line_edit_name, line_edit)
                horizontal_layout.addLayout(create_horizontal_layout_dates(label, line_edit))
            self.optionbox_dates_preoperative_Content.addLayout(horizontal_layout)

        self.optionbox_dates_preoperative.setLayout(self.optionbox_dates_preoperative_Content)

        # Add toggle button
        self.toggle_button = QPushButton('Change dates')
        self.toggle_button.setFixedSize(150, 50)
        self.toggle_button.clicked.connect(self.toggle_line_edit)
        self.optionbox_dates_preoperative_Content.addWidget(self.toggle_button)

    #GP: Nutzer hat die Möglichkeit die LineEdit zu aktivieren, beim Start inaktiv
    def toggle_line_edit(self):
        """Toggle the enabled state of the line edit"""
        line_edits = [
            self.lineEditFirstDiagnosed,
            self.lineEditAdmNeurIndCheck,
            self.lineEditDismNeurIndCheck,
            self.lineEditOutpatientContact,
            self.lineEditNsurgContact,
            self.lineEditDBSconference
        ]
        for line_edit in line_edits:
            line_edit.setEnabled(not line_edit.isEnabled())
            if line_edit.isEnabled():
                line_edit.setPlaceholderText("DD/MM/YYYY")
            else:
                line_edit.setPlaceholderText("")

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

    def optionbox_reports_preoperative(self, layout_general):

        self.optionbox_reports_preoperative = QGroupBox('Reports and study participation:')
        self.optionbox_reports_preoperative.setFixedHeight(120)  #GP: Set the fixed height to 90 pixels, else alignment problems
        self.optionbox_reportsContent = QVBoxLayout(self.optionbox_reports_preoperative)
        layout_general.addWidget(self.optionbox_reports_preoperative, 1, 0)

        def create_checkbox(label_text):
            checkbox = QCheckBox()
            checkbox_label = QLabel(label_text)
            checkbox_label.setAlignment(QtCore.Qt.AlignLeft)
            return checkbox, checkbox_label

        checkboxes_info = [
            ('Report_preop', 'Report'),
            ('Decision_DBS_preop', 'Decision for lead placement'),
            ('icVRCS_preop', 'Consent VERCISE-DBS'),
            ('inexVRCS_preop', 'In-/Exclusion criteria VERCISE-DBS'),
        ]

        textbox = QHBoxLayout()
        for num, (checkbox_name, label_text) in enumerate(checkboxes_info):
            checkbox, checkbox_label = create_checkbox(f'{label_text}:' if num == 0 else f'\t{label_text}:')
            setattr(self, checkbox_name, checkbox)
            setattr(self, f'{checkbox_name}_Label', checkbox_label)
            textbox.addWidget(checkbox_label)
            textbox.addWidget(checkbox)


        textbox.addStretch()
        self.optionbox_reportsContent.addLayout(textbox)
        self.optionbox_reports_preoperative.setLayout(self.optionbox_reportsContent)

    def optionbox_questionnaires_preoperative(self, layout_general):

        self.optionbox_questionnaires = QGroupBox('Scales and questionnaires:')
        self.optionbox_questionnairesContent = QHBoxLayout(self.optionbox_questionnaires)
        layout_general.addWidget(self.optionbox_questionnaires, 2, 0)

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
            for num, (k, v) in enumerate(content[i].items()):  # columns
                if num == 0:
                    label = QLabel(f'{k}:')
                else:
                    label = QLabel(f'\t{k}:')
                self.GridCoordinatesLeft.addWidget(label, i, idx_cols)
                idx_cols += 1
                self.GridCoordinatesLeft.addWidget(v, i, idx_cols)
                v.setMaximumWidth(60)
                idx_cols += 1

        self.optionbox_questionnairesContent.addLayout(self.GridCoordinatesLeft)
        self.optionbox_questionnairesContent.addStretch()

    def optionbox_preoperative_other(self, layout_general):
        self.optionbox_other = QGroupBox('Other:')
        self.optionbox_other.setFixedHeight(120) #GP: fixed alignment issues
        self.optionbox_otherContent = QVBoxLayout(self.optionbox_other)
        layout_general.addWidget(self.optionbox_other, 3, 0)

        def create_checkbox(label_text):
            checkbox = QCheckBox()
            checkbox_label = QLabel(label_text)
            checkbox_label.setAlignment(QtCore.Qt.AlignLeft)
            return checkbox, checkbox_label

        checkboxes_info = [
            ('Video_preop', 'Video'),
            ('MRI_preop', 'MRI'),
            ('fpcit_spect_preop', 'FP-CIT SPECT'),
        ]

        box4line1 = QHBoxLayout()
        for num, (checkbox_name, label_text) in enumerate(checkboxes_info):
            checkbox, checkbox_label = create_checkbox(f'{label_text}:' if num == 0 else f'\t{label_text}:')
            setattr(self, checkbox_name, checkbox)
            setattr(self, f'{checkbox_name}_Label', checkbox_label)
            box4line1.addWidget(checkbox_label)
            box4line1.addWidget(checkbox)


        box4line1.addStretch(1)
        self.optionbox_otherContent.addLayout(box4line1)
        self.optionbox_other.setLayout(self.optionbox_otherContent)

    def create_bottom_buttons_preoperative(self, layout_general):
        """Creates two buttons a) to read medication and b) to save settings and exit GUI """
        # Use more descriptive names for the buttons
        self.button_medication = QPushButton('Preoperative\nMedication')
        self.button_save = QPushButton('Save')
        self.button_save_return = QPushButton('Save and\nReturn')
        self.button_check_inputs = QPushButton('Check Inputs')

        # Set fixed size for all buttons
        button_width = 200
        button_height = 75

        # Apply fixed size using a loop for cleaner code
        for button in [self.button_medication, self.button_save, self.button_save_return, self.button_check_inputs]:
            button.setFixedSize(button_width, button_height)

        # Use QVBoxLayout for better vertical alignment
        vlay_bottom = QHBoxLayout()

        # Add buttons to the layout
        vlay_bottom.addWidget(self.button_medication)
        vlay_bottom.addWidget(self.button_save)
        vlay_bottom.addWidget(self.button_save_return)
        vlay_bottom.addWidget(self.button_check_inputs)

        # Add stretch to push buttons to the sides
        vlay_bottom.addStretch()

        # Create a horizontal layout for overall alignment
        hlay_bottom = QHBoxLayout()
        hlay_bottom.addStretch(5)
        hlay_bottom.addLayout(vlay_bottom)
        hlay_bottom.addStretch(1)

        # Add the horizontal layout to the general layout
        layout_general.addLayout(hlay_bottom, 4, 0, 1, 3)

    def updatePreoperativeData(self):
        """Displays all the information that has been stored already in the csv files"""

        df_subj = Content.extract_saved_data(self.date)
        if not df_subj["ID"]:  # this is only for when no information could be found
            print("No ID for current_subject in preoperative.csv found") #GP: zum debugging
            return

        integer_list = ["UPDRS_On_preop", "UPDRS_Off_preop",
                        "NMSQ_preop", "MoCa_preop", "DemTect_preop",
                        "MMST_preop", "PDQ8_preop", "BDI2_preop",
                        "PDQ39_preop", "UPDRSII_preop", "H&Y_preop",
                        "EQ5D_preop", "S&E_preop"]

        for column, widget in self.content_widgets.items():
            widget_object = getattr(self, widget)
            value = df_subj[column][0]
            if column in integer_list:
                widget_object.setText(str(int(value)) if str(value) not in ['nan', '0'] else '')
            else:
                widget_object.setText(str(value) if str(value) not in ['nan', '0'] else '')

        # Edit Upper CheckBoxes with content using a ternary operator

        checkboxes = ["Video_preop", "MRI_preop", "fpcit_spect_preop", "Report_preop",
                      "Decision_DBS_preop", "icVRCS_preop", "inexVRCS_preop"]

        for checkbox in checkboxes:
            if str(df_subj[checkbox][0]) == '1':
                getattr(self, checkbox).setCheckState(QtCore.Qt.Checked)
            else:
                getattr(self, checkbox).setCheckState(QtCore.Qt.Unchecked)
        # or QtCore.Qt.Checked

        return

    def connect_button_actions(self):
        """Defines the actions that are taken once a button is pressed or specific input is made"""
        self.button_medication.clicked.connect(self.onClickedMedication)
        self.button_save.clicked.connect(self.onClickedSave)
        self.button_save_return.clicked.connect(self.onClickedSaveReturn)
        self.button_check_inputs.clicked.connect(self.onClickedCheckInputs)  # Connect new button

    # ====================   Defines actions when buttons are pressed      ====================
    @QtCore.pyqtSlot()
    def onClickedCheckInputs(self):
        """Handles the Check Inputs button click event"""
        self.check_inputs()


    @QtCore.pyqtSlot()
    def onClickedMedication(self):
        """Shows medication dialog ; former implementation with creating GUI was replaced with show/hide GUI which is
        initiated at beginning at the disadvantage of not being saved until GUIpreoperative is closed"""

        subject_id = General.read_current_subj().id[0]
        df = General.import_dataframe(f'{self.date}.csv', separator_csv=',')

        if subject_id in df['ID'].values:
            self.dialog_medication = MedicationDialog(parent=self, visit=self.date)
            self.dialog_medication.exec_()
        else:
            Output.msg_box('Please save data before entering medication!', f'No entry for ID: {subject_id}')
            return

    @QtCore.pyqtSlot()
    def onClickedSave(self):
        self.save_data2csv()

    def onClickedSaveReturn(self):
        """closes GUI and returns to calling (main) GUI"""
        self.save_data2csv()
        self.close()

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
            df_subj['PID_ORBIS'] = df_general['PID_ORBIS'][0]
            df_subj['Gender'] = df_general['gender'][0]
            df_subj['Diagnosis_preop'] = df_general['diagnosis'][0]
        except KeyError:
            print("No Data in general_data for this ID found")

        # Now extract changed data from the GUI
        for column, widget in self.content_widgets.items():
            widget_object = getattr(self, widget)
            df_subj[column] = widget_object.text().strip()
            if df_subj[column] == "":
                df_subj[column] = ""

        checkboxes = ["Video_preop", "MRI_preop", "fpcit_spect_preop", "Report_preop",
                      "Decision_DBS_preop", "icVRCS_preop", "inexVRCS_preop"]

        for checkbox in checkboxes:
            df_subj[checkbox] = 1 if getattr(self, checkbox).isChecked() else 0

        preop_medication = [med.replace(' ', '_').replace('{}', '_preop') for med in General.available_PDmedication()]

        for med in preop_medication:
            if med in df_subj:
                df_subj[med] = df_subj[med] if df_subj[med] != '' else np.nan
            else:
                df_subj[med] = np.nan

        # Ensure the correct data types using dtype_dict_preoperative
        # why integer does not work with nullable values: https://pandas.pydata.org/docs/user_guide/integer_na.html
        error_keys = []
        for key, dtype in dtype_dict_preoperative.items():
            if key in df_subj:
                try:
                    if dtype == "float64":
                        df_subj[key] = float(df_subj[key]) if df_subj[key] != "" else np.nan
                    elif dtype == "int64":
                        df_subj[key] = int(df_subj[key]) if df_subj[key] != "" else pds.NA
                    elif dtype == "object":
                        df_subj[key] = str(df_subj[key]) if df_subj[key] != "" else ""
                    df_subj[key] = pds.array([df_subj[key]], dtype=dtype)[0]
                except (ValueError, TypeError):
                    print("Error", dtype, df_subj[key])
                    error_keys.append(key)
                    if dtype == "float64":
                        df_subj[key] = np.nan
                    elif dtype == "int64":
                        df_subj[key] = pds.NA
                    elif dtype == "object":
                        df_subj[key] = ""
        print("df:", df)
        print("df_subj:", df_subj)
        for error_key in error_keys:
            print(error_key, df_subj[error_key], df[error_key])

        # Incorporate the [df_subj] dataframe into the entire dataset and save as csv
        try:
            idx2replace = df.index[df['ID'] == subject_id][0]
            print("INDEX2REPLACE:\n", idx2replace)
            for key, value in df_subj.items():
                if pds.isna(value) or value in ["", "nan"]:
                    if key in dtype_dict_preoperative.keys():
                        df[key] = df[key].astype(dtype_dict_preoperative[key])
                        df.at[idx2replace, key] = value
                else:
                    if key in dtype_dict_preoperative.keys():
                        df[key] = df[key].astype(dtype_dict_preoperative[key])
                        df.at[idx2replace, key] = value
        except IndexError:
            df_subj = pds.DataFrame(df_subj, index=[df.index.shape[0]])
            df_subj = df_subj.dropna(how='all')  # Exclude all-NA entries
            df = pds.concat([df, df_subj], ignore_index=True) #GP: FutureWarning, as long as one column does not have any data

        df.to_csv(Path(f"{FILEDIR}/{self.date}.csv"), index=False)


    def check_inputs(self):
        """Checks if the input values for the questionnaires/scores are within the specified ranges"""
        neurological_tests = {
            "updrsON": (0, 199),
            "updrsOFF": (0, 199),
            "nmsq": (0, 30),
            "moca": (0, 30),
            "demtect": (0, 18),
            "mmst": (0, 30),
            "pdq8": (0, 100),
            "bdi2": (0, 63),
            "pdq39": (0, 156),
            "updrsII": (0, 52),
            "hy": (1, 5),
            "self.hy": (1,5),
            #"hruq": ("No numerical score"),
            "eq5d": (-0.59, 1.0),
            "se": (0, 100),
        }
        check_inputs_text = ""
        count = 0
        for test_name, (min_val, max_val) in neurological_tests.items():
            widget = getattr(self, test_name, None)
            if widget:
                print(widget)
                try:
                    value = float(widget.text())
                    if value < min_val or value > max_val:
                        check_inputs_text += f"Value for {test_name} is out of range: {value}\n"
                except ValueError:
                    count += 1
                    if widget.text() == "":
                        pass
                    else:
                        check_inputs_text += f"Invalid input for {test_name}: {widget.text()}\n"

        if count + 1 == len(neurological_tests.keys()):
            Output.msg_box('No inputs found', 'Check input')
        elif check_inputs_text != "":
            Output.msg_box(check_inputs_text, 'Check input')
        else:
            Output.msg_box("Correct inputs", 'Check input')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = PreoperativeDialog()
    dlg.show()
    sys.exit(app.exec_())
