#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import re
import rstr
import csv
import os
import shutil
import pandas as pds
import numpy as np
from pathlib import Path
from dependencies import ROOTDIR, FILEDIR, LEADS, dtype_dict_intraoperative, dtype_dict_preoperative, dtype_dict_postoperative
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QVBoxLayout, QGroupBox, QInputDialog, \
    QHBoxLayout, QFileDialog, QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QCheckBox, QMessageBox, QDialogButtonBox
from PyQt5 import QtCore


class General:
    def __init__(self, _debug=False):
        pass

    @staticmethod
    def create_pseudonym(size_array: int) -> str:
        """generates pseudonym -- ';' and ',' are omitted to avoid confusion in 'csv-files' """
        re_expression = f'[a-zA-Z0-9_!#%$§]{{{size_array}}}'
        return rstr.xeger(re_expression)

    @staticmethod
    def available_PDmedication():
        """TODO: should be reoplaced as defined in dependnciesList w/ available medication against PD;
        parenthesis intended to introduce pre|intra|postoperative"""

        medication = ['Levodopa Carbidopa{}', # delete carbidopa
                      'Levodopa Carbidopa CR{}', #delete carbidopa
                      #'Levodopa ER',
                      #'Duodopa',
                      'Entacapone{}',
                      'Tolcapone{}',
                      'Opicapone{}',
                      'Selegiline oral{}',
                      'Selegiline sublingual{}',
                      'Rasagiline{}',
                      'Safinamide{}',
                      'Apomorphine{}',
                      'Piribedil{}',
                      'Pramipexole{}',
                      'Ropinirole{}',
                      'Rotigotine{}',
                      'Amantadine{}',
                      ]
        return medication

    @staticmethod
    def import_dataframe(filename: str, separator_csv: str = ',', missing_values: str = '') -> pds.DataFrame:
        """returns pandas dataframe from csv"""
        #TODO: use dtype to make data consistent
        filename_total = os.path.join(FILEDIR, filename)

        if not os.path.isfile(filename_total):
            print(f'\t Filename: {filename_total} not found. Please double-check!')
        df = pds.read_csv(filename_total, sep=separator_csv, on_bad_lines='skip', na_values=missing_values)

        if df.shape[1] == 1:
            df = pds.read_csv(filename_total, sep=';', on_bad_lines='skip', na_values=missing_values)
        return df

    @staticmethod
    def write_csv_temp(df, idx, default_filename='current_subj.csv'):
        """this function is intended to write a file in which the metadata of the subject being processed is saved"""

        header = ['pid', 'id', 'idx']
        data = [str(df["PID_ORBIS"][idx[0]]), str(df["ID"][idx[0]]), idx[0]] #GP: PID should not be integer

        with open(os.path.join(ROOTDIR, 'temp', default_filename), 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow(data)

    @staticmethod
    def read_current_subj(default_filename='current_subj.csv'):
        """Reads data from temporary information"""

        file_path = Path(ROOTDIR) / 'temp' / default_filename
        if file_path.exists():
            subj_details = pds.read_csv(file_path)
        else:
            subj_details = pds.DataFrame()

        return subj_details

    @staticmethod
    def get_data_subject_old(flag, pid2lookfor):
        """gets data from available dataframes for a single subject or creates empty file if not present"""

        file_to_read = os.path.join(f'{flag}.csv')
        try:
            data_all = General.import_dataframe(file_to_read, separator_csv=',')
            if data_all.shape[1] == 1:  # avoids problems with comma-separated vs. semicolon-separated csv-files
                data_all = General.import_dataframe(file_to_read, separator_csv=';')
            #pid2lookfor = str(pid2lookfor).lstrip('0')  # string that is searched for in metadata file, GP: PIDs could have leading zeros
            idxPID = data_all.index[data_all['PID_ORBIS'] == int(pid2lookfor)].to_list() #GP: PIDs should not be treated as integers (leading zero)
            data_subj = data_all.iloc[idxPID]
        except FileNotFoundError:  # creates empty file from template (/.install) in case of first use
            print('No file names {} found, creating new file from template in {}/.install '.format(file_to_read, ROOTDIR))
            file2copy = os.path.join(ROOTDIR, '.install', '{}_template.csv'.format(flag))
            shutil.copyfile(file2copy, os.path.join(FILEDIR, file_to_read))
            data_subj = []

        return data_subj

    @staticmethod
    def get_data_subject(flag, pid2lookfor):
        """gets data from available dataframes for a single subject or creates empty file if not present"""

        file_to_read = os.path.join(f'{flag}.csv')
        try:
            data_all = General.import_dataframe(file_to_read, separator_csv=',')
            if data_all.shape[1] == 1:  # avoids problems with comma-separated vs. semicolon-separated csv-files
                data_all = General.import_dataframe(file_to_read, separator_csv=';')
            # pid2lookfor = str(pid2lookfor).lstrip('0')  # string that is searched for in metadata file, GP: PIDs could have leading zeros
            idxPID = data_all.index[data_all['PID_ORBIS'] == pid2lookfor].to_list()  # GP: PIDs should not be treated as integers (leading zero)
            data_subj = data_all.iloc[idxPID]
        except FileNotFoundError:  # creates empty file from template (/.install) in case of first use
            print(
                'No file names {} found, creating new file from template in {}/.install '.format(file_to_read, ROOTDIR))
            file2copy = os.path.join(ROOTDIR, '.install', '{}_template.csv'.format(flag))
            shutil.copyfile(file2copy, os.path.join(FILEDIR, file_to_read))
            data_subj = []

        return data_subj

    @staticmethod
    def synchronize_data_with_general(flag, id2lookfor, messagebox=True, DEBUG=False):
        """adds gender and ID to where no entries were made in the csv-files"""
        print("flag, id2lookfor:", flag, id2lookfor)
        if flag == 'preoperative':
            dtype_dict = dtype_dict_preoperative
        elif flag == 'postoperative':
            dtype_dict = dtype_dict_postoperative
        elif flag == 'intraoperative':
            dtype_dict = dtype_dict_intraoperative

        df_general = General.import_dataframe('general_data.csv', separator_csv=',')
        if df_general.shape[1] == 1:  # avoids problems with comma-separated vs. semicolon-separated csv-files
            df_general = General.import_dataframe('general_data.csv', separator_csv=';')

        idx1 = df_general.index[df_general['ID'] == id2lookfor].to_list()

        file2change = General.import_dataframe(f'{flag}.csv', separator_csv=',')
        if file2change.shape[1] == 1:  # avoids problems with comma-separated vs. semicolon-separated csv-files
            file2change = General.import_dataframe(f'{flag}.csv', separator_csv=';')


        indices2change = file2change.index[file2change['ID'] == id2lookfor].to_list()
        for k in indices2change:
            # Ensure the PID_ORBIS column is of string dtype
            file2change['PID_ORBIS'] = file2change['PID_ORBIS'].astype(str)
            # Assign the value
            file2change.loc[int(k), 'PID_ORBIS'] = df_general.loc[idx1[0], 'PID_ORBIS']

        if messagebox:
            Output.msg_box(text='There were changes in the file \n\t{} \nfor subj\n\t{}.\n Please '
                                'confirm to continue'.format(f'{flag}.csv',
                                                             int(df_general['PID_ORBIS'].iloc[idx1])),
                           title='Changed data in {}.csv'.format(flag), flag='Warning')
        file2change.to_csv(os.path.join(FILEDIR, f'{flag}.csv'), index=False)

        return

    @staticmethod
    def validate_and_format_dates(date):
        """
        Validates and formats a date string to the format DD/MM/YYYY.

        Parameters:
        - date (str): Date string to validate and format.

        Returns:
        - str: Formatted date string or 'Invalid date format'.
        """
        date_pattern = re.compile(r'^\d{2}/\d{2}/\d{4}$')

        if not date_pattern.match(date):
            try:
                # Attempt to reformat the date
                parsed_date = pds.to_datetime(date, dayfirst=True)
                year = parsed_date.year
                if year > 2025: #handle future years after being parsed
                    year -= 100
                formatted_date = parsed_date.replace(year=year).strftime('%d/%m/%Y')
                return formatted_date
            except ValueError:
                return 'Invalid date format'
        else:
            return date

    #GP: fixing problem with pandas not keeping a consistent DataType
    @staticmethod
    def ensure_float_dtype(df, columns):
        """Ensures that the specified columns in the DataFrame are of string dtype."""
        for column in columns:
            if column in df.columns:
                try: df[column] = df[column].astype(float)
                except AttributeError:
                    print("AttributeError ensuring float dtype")
                    df[column] = np.nan
        return df

    @staticmethod
    def ensure_int_dtype(df, columns):
        """Ensures that the specified columns in the DataFrame are of integer dtype."""
        for column in columns:
            if column in df.columns:
                try:
                    df[column] = df[column].astype(int)
                except AttributeError:
                    print("AttributeError ensuring int dtype")
                    df[column] = np.nan
        return df


class Content:
    def __init__(self, _debug=False):
        pass

    @staticmethod
    def details_of_IPG(detail_to_extract='Manufacturer'):
        """Here a list of all available details of DBS systems is created see [dependencies.py] for details """

        detail = set()  # Using a set to store unique manufacturers

        for lead, details in LEADS.items():
            x = details.get(detail_to_extract)
            if detail_to_extract:
                detail.add(x)

        return list(detail)

    @staticmethod
    def list_of_IPG(manufacturer_to_extract=None):
        """Creates a list of available IPG models according to the list provided in [dependencies.py]"""

        if not manufacturer_to_extract:
            models = list(LEADS.keys())
        else:
            models = [key for key, details in LEADS.items() if
                      details.get('Manufacturer') == manufacturer_to_extract]

        return models

    @staticmethod
    def extract_postoperative_dates(condition='postoperative'):
        """ Extracts a list with all available postoperative dates for a subject"""

        subject_pid = General.read_current_subj().pid[0]
        data_frame = General.import_dataframe('{}.csv'.format(condition), separator_csv=',')

        data_frame = data_frame.loc[data_frame['PID_ORBIS'] == subject_pid]
        list_of_dates = data_frame['Reason_postop'].tolist()

        # Check if NaN is present in the list_of_dates
        if any(pds.isna(date) for date in list_of_dates): # Replace NaN with an empty string
            list_of_dates = ['' if pds.isna(date) else date for date in list_of_dates]

        return list_of_dates

    @staticmethod
    def extract_saved_data(condition, followup_timing=''):
        """ defines a list of columns for the csv files in the data folder; if id not found,
        dictionary remains empty"""

        subj_id = General.read_current_subj().id[0]  # reads data from curent_subj (saved in ./tmp)
        df = General.import_dataframe('{}.csv'.format(condition), separator_csv=',')
        if df.shape[1] == 1:
            df = General.import_dataframe('{}.csv'.format(condition), separator_csv=';')

        if df.shape[0] == 0:
            ID_to_add = {'PID_ORBIS': General.read_current_subj().pid[0],
                         'ID': General.read_current_subj().id[0]}  # Fill in the actual value for PID_ORBIS
            new_row_df = pds.DataFrame(ID_to_add, index=[0])
            df = df._append(new_row_df, ignore_index=True)

        # Only filter the data if the condition is "postoperative" and a follow-up interval is provided
        if followup_timing != '':
            df_subj = df[(df['Reason_postop'] == followup_timing) & (df['ID'] == subj_id)]
        else:
            df_subj = df.iloc[df.index[df['ID'] == subj_id].tolist()].to_dict('list')

        return df_subj

    @staticmethod
    def create_first_column(num_rows, string2use: list):
        """Creates first column in a grid, which indicates what content at each column"""
        titleRow_layout = QGridLayout()

        if num_rows == 3:
            for j in range(num_rows + 1):
                    label = QLabel('') if j == 0 else QLabel(str(string2use[j-1]))
                    label.setAlignment(QtCore.Qt.AlignCenter)
                    label.setFixedHeight(35)
                    titleRow_layout.addWidget(label, j, 0)
            return titleRow_layout

        else:
            for j in range(num_rows + 1):
                if j == 0:
                    label = QLabel('')
                    label.setAlignment(QtCore.Qt.AlignCenter)
                    label.setFixedHeight(35)
                    titleRow_layout.addWidget(label, j, 0)
                elif j ==1:
                    label = QLabel(str(string2use[j - 1]))
                    #QLabel(str(string2use[j - 1]))
                    label.setAlignment(QtCore.Qt.AlignCenter)
                    label.setFixedSize(50, 35)
                    titleRow_layout.addWidget(label, j, 0)
                else:
                    label = QLabel(str(string2use[j - 1]))
                    label.setAlignment(QtCore.Qt.AlignCenter)
                    label.setFixedSize(50, 35)
                    hbox = QHBoxLayout()
                    hbox.addWidget(label)
                    hbox.addStretch()
                    titleRow_layout.addLayout(hbox, j, 0)
            return titleRow_layout


    @staticmethod
    def find_lineedit_objects(optionboxes):
        """Finding all QLineEdit elements to be enabled/disabled until reason for visit is entered"""
        line_edits = []

        for optionbox in optionboxes:
            line_edits_in_optionbox = optionbox.findChildren(QLineEdit)
            line_edits.extend(line_edits_in_optionbox)

        return line_edits

    @staticmethod
    def find_checkbox_objects(widget_list):
        """Finds and returns a list of QCheckBox objects from the provided widget list."""
        checkbox_objects = []
        for widget in widget_list:
            if isinstance(widget, QGroupBox):
                for child in widget.findChildren(QCheckBox):
                    checkbox_objects.append(child)
            elif isinstance(widget, QCheckBox):
                checkbox_objects.append(widget)
        return checkbox_objects

    @staticmethod
    def object_visibility(obj, action):
        """ Modifies the visibility of an object; here it makes sure selection occurs sequentially"""

        for i in range(obj.count()):
            item = obj.itemAt(i)

            if isinstance(item.widget(), QLabel) or isinstance(item.widget(), QComboBox):
                if action == 'show':
                    item.widget().show()
                elif action == 'hide':
                    item.widget().hide()


class Output:
    def __init__(self, _debug=False):
        pass

    @staticmethod
    def msg_box(text='Unknown text', title='unknown title', flag='Information'):
        """helper intended to provide some sort of message box with a text and a title"""
        msgBox = QMessageBox()
        if flag == 'Information':
            msgBox.setIcon(QMessageBox.Information)
        elif flag == 'Warning':
            msgBox.setIcon(QMessageBox.Warning)
        else:
            msgBox.setIcon(QMessageBox.Critical)

        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec()

    def open_input_dialog_postoperative(self):
        """
        Open a message box asking for user input to determine the date after surgery.
        """
        while True:
            # Prompt the user for a date or event description
            result, ok = QInputDialog.getText(
                self, 'Input Dialog', 'Please enter the date after surgery or the event:'
            )
            if not ok:  # User canceled the dialog
                return None #if None is retuned, None is added to list

            # Validate and format the entered date
            formatted_date = General.validate_and_format_dates(result)
            if formatted_date == 'Invalid date format':
                # Show a warning message if the date format is invalid
                QMessageBox.warning(
                    self, 'Invalid Date',
                    'The entered date is invalid. Please enter a date in the format DD/MM/YYYY.'
                )
            else:
                # If the date is valid, print and return it
                print(f'Validated and formatted date: {formatted_date}')
                return formatted_date

    @staticmethod
    def delete_msg_box(pid_subject):
        # Create a custom dialog for user confirmation
        dialog = QDialog()
        dialog.setWindowTitle('Delete Data')
        dialog_layout = QVBoxLayout(dialog)

        label = QLabel(f'All data for PID {pid_subject} will be lost.\nTo proceed, type "Yes" below:')
        dialog_layout.addWidget(label)

        line_edit = QLineEdit()
        line_edit.setFixedSize(200, 50)
        dialog_layout.addWidget(line_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        dialog_layout.addWidget(button_box)

        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        if dialog.exec() == QDialog.Accepted and line_edit.text().lower() == 'yes':
            return True
        else:
            return False

class Clean:
    def __init__(self, _debug=False):
        pass

    @staticmethod
    def extract_subject_data(subject_id):
        """
        Extract data for a subject from a CSV file.

        Parameters:
        - subject_id (str): The ID of the subject.

        Returns:
        - df (pd.DataFrame): Extracted dataframe with the data.
        """
        # missing_values = ['n/a', 'na', '--'] # has been used in previous versions
        df = General.import_dataframe(os.path.join(FILEDIR, 'general_data.csv'))
        df = df.loc[df['ID'] == subject_id]
        return df

    @staticmethod
    def delete_subject_data(subject_id, path=FILEDIR):
        """Deletes rows with the specified subject_id from all CSV files in the data folder."""
        csv_files = ['preoperative.csv', 'intraoperative.csv', 'postoperative.csv', 'general_data.csv']

        for file in csv_files:
            file_path = os.path.join(path, file)
            df = pds.read_csv(file_path)
            df = df[df['ID'] != subject_id]  # Delete rows with the specified subject_id
            df.to_csv(file_path, index=False)  # Save the updated DataFrame back to the CSV file


        file_path = os.path.join(path, 'general_data.csv')
        df = pds.read_csv(file_path)
        # Update curr_no according to the new index
        df['curr_no'] = df.index
        # Save the updated DataFrame back to the CSV file
        df.to_csv(file_path, index=False)
