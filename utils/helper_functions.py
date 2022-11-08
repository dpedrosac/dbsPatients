#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rstr
import csv
import os
import shutil

import pandas as pds
from dependencies import ROOTDIR, FILEDIR
from PyQt5.QtWidgets import QMessageBox, QFileDialog


class General:
    def __init__(self, _debug=False):
        pass

    @staticmethod
    def generate_code(size_array):
        """generates a code consisting of a random combination of letters, numbers and special characters; ';' and ','
        are omitted to avoid confusion in 'csv-files' """
        re_expression = '[a-zA-Z0-9_!#%$§]{}'.format('{%s}' % str(size_array))

        return rstr.xeger(re_expression)

    @staticmethod
    def import_dataframe(filename, separator_csv=';'):
        """returns pandas dataframe from csv ()"""

        filename_total = os.path.join(FILEDIR, filename)
        if not os.path.isfile(filename_total):
            print('\t Filename: {} not found. Please double-check!'.format(filename_total))

        df = pds.read_csv(filename_total, sep=separator_csv)

        return df

    @staticmethod
    def write_csv_temp(df, idx, default_filename='current_subj.csv'):
        """this function is intended to write a file in which the metadata of the subject being processed is saved"""

        header = ['pid', 'id', 'idx']
        data = [int(df["PID_ORBIS"][idx[0]]), str(df["ID"][idx[0]]), idx[0]]

        with open(os.path.join(ROOTDIR, 'temp', default_filename), 'w', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow(data)

    @staticmethod
    def read_current_subj(default_filename='current_subj.csv'):
        """reads data from temporary information"""

        try:
            subj_details = pds.read_csv(os.path.join(ROOTDIR, 'temp', default_filename))  # Read currently used subj.
        except FileNotFoundError:
            print('Data not found! Please make sure that a file named "current_subj.csv" exists in the "temp" folder')
            subj_details = []

        return subj_details

    @staticmethod
    def get_data_subject(flag, pid2lookfor):
        """gets data from available dataframes for a single subject or creates empty file if not present"""

        file2read = os.path.join('{}.csv'.format(flag))
        try:
            data_all = General.import_dataframe(file2read, separator_csv=',')
            pid2lookfor = str(pid2lookfor).lstrip('0')  # string that is searched for in metadata file
            idxPID = data_all.index[data_all['PID'] == int(pid2lookfor)].to_list()
            data_subj = data_all.iloc[idxPID]
        except FileNotFoundError:
            print('No file names {} found, creating new file from template in {}/.install '.format(file2read, ROOTDIR))
            file2write = os.path.join(ROOTDIR, '.install', '{}_template.csv'.format(flag))
            shutil.copyfile(file2read, file2write)
            data_subj = []

        return data_subj

    @staticmethod
    def synchronize_data_with_general(flag, id2lookfor, MessageBox=True):
        """adds gender and ID to where no entries were made in the csv-files"""

        file_general = General.import_dataframe('general_data.csv', separator_csv=',')
        idx1 = file_general.index[file_general['ID'] == id2lookfor].to_list()

        file2change = General.import_dataframe('{}.csv'.format(flag), separator_csv=',')
        indices2change = file2change.index[file2change['ID'] == id2lookfor].to_list()
        for k in indices2change:
            file2change['Gender'].loc[int(k)] = int(file_general['Gender'].iloc[idx1])
            file2change['PID'].loc[int(k)] = int(file_general['PID_ORBIS'].iloc[idx1])

        if MessageBox:
            Output.msg_box(text='There were changes in the file \n\t{} \nfor subj\n\t{}.\n Please '
                                'confirm to continue'.format('{}.csv'.format(flag),
                                                             int(file_general['PID_ORBIS'].iloc[idx1])),
                           title='Changed data in {}.csv'.format(flag), flag='Warning')
        file2change.to_csv(os.path.join(FILEDIR, '{}.csv'.format(flag)), index=False)

        return


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


class Clean:
    def __init__(self, _debug=False):
        pass

    @staticmethod
    def fill_missing_demographics(flag):
        """very unique function without much versatility intended to fill missing data from general_data.csv to
        pre-/intra-/postoperative.csv in the ./data folder"""

        file_general = General.import_dataframe('general_data.csv', separator_csv=',')

        for index, row in file_general.iterrows():
            General.synchronize_data_with_general(flag, row['ID'], MessageBox=False)
