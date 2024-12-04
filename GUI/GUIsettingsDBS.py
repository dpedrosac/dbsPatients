#!/usr/bin/env python3
import sys, re
import pandas as pd
import numpy as np
from PyQt5 import QtCore
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QPushButton, QLineEdit, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QLabel, QGridLayout, QComboBox, QLayout, QDialog, QMessageBox

import dependencies
from utils.helper_functions import General, Content, Clean
from dependencies import FILEDIR

pd.options.mode.chained_assignment = None


class DBSsettingsDialog(QDialog):
    """Dialog to introduce the DBS-Settings at a specific date."""

    def __init__(self, visit='postoperative', reason = "DD/MM/YYY",  parent=None):
        super(DBSsettingsDialog, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.date = visit  # ensures the right date is entered
        self.group_layouts_contacts = []  # this ensures that group 2 may be made visible or not
        self.group_layouts_settings = []  # this ensures that group 2 may be made visible or not
        self.group_anode = []
        self.group_cathode = []
        self.group_settings = []
        self.reason = reason
        #self.implanted_IPG = implanted_IPG

        self.adjustSize()
        self.setup_ui()
        self.update_inputs_with_existing_data()

    def setup_ui(self):
        self.setup_general_layout()

    def setup_general_layout(self):
        """Defines the general layout for the GUI"""

        subj_details = General.read_current_subj() # reads information for the subject last being processed
        self.setWindowTitle(f'Postoperative DBS settings (PID: {int(subj_details.pid.iloc[0])}) on date: {self.reason}')

        layout_general = QGridLayout(self)
        self.setLayout(layout_general)

        # start creating option boxes that will appear in the GUI for entering DBS settings
        # Create option box for entering the selected contacts
        self.settings_left, self.settings_leftContent = self.settings_DBSleads_general(layout_general, side='left')
        self.settings_right, self.settings_rightContent = self.settings_DBSleads_general(layout_general, side='right')

        # Create option box for entering details of system (if not present already)
        self.system_information(layout_general)

        # Create option box for entering selected amplitude and frequency
        self.DBSparameters_left = self.DBS_parameters(layout_general, side='left')
        self.DBSparameters_right = self.DBS_parameters(layout_general, side='right')

        # Create option box with further possibilities
        self.action_buttons_bottom(layout_general)

        self.show()

    @staticmethod
    def settings_DBSleads_general(layout_general, side):
        """Generic function to create the option box to be filled later with content"""

        contacts = QGroupBox(f'Selected contacts - {side.capitalize()} target')
        contacts.setMaximumHeight(900)  #GP: Set the maximum width and height, helps with alignment while stetching the window vertically
        contactsContent = QHBoxLayout(contacts)

        idx = 0 if side == 'left' else 1
        layout_general.addWidget(contacts, 0, idx)

        return contacts, contactsContent

    def DBSsettings_specific(self, side, obj, obj_content):
        """Generic function to fill the created optionbox with specific content according to the [LEADS] information"""
        from dependencies import LEADS

        idx = 0 if side == 'left' else 1
        try:
            num_contacts = int(LEADS[self.lineEditLeads.currentText()]['Contacts_per_side'])
            contact_name = LEADS[self.lineEditLeads.currentText()]['Contacts_name'][idx]
            contact_name.insert(0, 'IPG') if not contact_name[0] == 'IPG' else contact_name  # necessary for some reason, GP: makes list look like this: [['IPG', names1],[IPG, names2]]
            print(contact_name)
            #GP: IPG hat eigene Eingabeflächen!!!

        except KeyError:
            print("Keyerror DBSsettings_specific")
            return obj, obj_content

        for group_number in range(1, 3): #GP: erstellt 2 Gruppen
            layout, dbs_percentage_layout = QVBoxLayout(), QHBoxLayout()
            group_label = QLabel(f"Group {group_number}")
            #group_label.setFixedSize(100, 100)  # Set the desired width and height
            layout.addWidget(group_label)
            #GP: imported former staticmethod to GUI -> access to lineedit objectnames
            anode_grid, anode_content = self.create_grid_columntitle(name_title="Anode", num_rows=num_contacts, group_num = f'G{group_number}', side = idx, contact_names = contact_name)
            cathode_grid, cathode_content = self.create_grid_columntitle(name_title="Cathode",num_rows=num_contacts, group_num = f'G{group_number}', side = idx, contact_names = contact_name)
            #GP: y-achsenbeschriftung
            if group_number == 1:
                FirstColumnNames = Content.create_first_column(num_rows=num_contacts + 1,
                                                               string2use=contact_name)
                dbs_percentage_layout.addLayout(FirstColumnNames)

            dbs_percentage_layout.addLayout(anode_grid)
            dbs_percentage_layout.addLayout(cathode_grid)  # adds both layouts

            if group_number == 1:
                self.set_lineedit_state(dbs_percentage_layout, enabled=True)
            layout.addLayout(dbs_percentage_layout)
            #GP: mittige Buttons
            if group_number == 2:
                toggle_layout = QVBoxLayout()
                toggleButton1 = QPushButton('+', self)
                toggleButton1.setFixedSize(30, 30)  # Set a fixed size
                toggleButton2 = QPushButton('-', self)
                toggleButton2.setFixedSize(30, 30)  # Set a fixed size
                toggle_layout.addWidget(toggleButton1)
                toggle_layout.addWidget(toggleButton2)
                obj_content.addLayout(toggle_layout)
            obj_content.addLayout(layout)
            self.group_layouts_contacts.append(dbs_percentage_layout)  # needed to toggle visibility of 2nd group later
            self.group_anode.append(anode_content)  # needed to extract values for saving
            self.group_cathode.append(cathode_content)  # needed to extract values for saving

        # Define what to do when button is pressed
        toggleButton1.clicked.connect(self.enable_SecondGroup)
        toggleButton2.clicked.connect(self.disable_SecondGroup)

        obj_content.addStretch(2)
        obj.hide()

        return obj, obj_content

    def system_information(self, layout_general):
        """Creates a series of combiboxes intended to obtain information about the implanted system"""
        self.optionbox_IPGchoice = QGroupBox(f'Information about the implanted system')
        self.optionbox_IPGchoiceContent = QVBoxLayout(self.optionbox_IPGchoice)
        layout_general.addWidget(self.optionbox_IPGchoice, 0, 3)

        #GP: necessary if IPG is imported from GUIpostoperative?
        manufacturer_layout = QHBoxLayout()
        self.LabelIPG = QLabel('IPG model?')
        self.lineEditIPG = QComboBox()
        items = ['Please select an IPG']
        systems = dependencies.SYSTEMS
        items.extend(systems)
        [self.lineEditIPG.addItem(k) for k in items]

        manufacturer_layout.addWidget(self.LabelIPG)
        manufacturer_layout.addWidget(self.lineEditIPG)
        manufacturer_layout.addStretch()

        #self.lineEditIPG.setCurrentText(self.implanted_IPG)
        #self.lineEditIPG.setEnabled(False)

        ipg_layout = QHBoxLayout()
        self.LeadManufacturer = QLabel('Lead manufacturer?')
        self.lineEditLeadManufacturer = QComboBox()
        items = ['Please select a manufacturer']
        manufacturers = Content.details_of_IPG()
        items.extend(manufacturers)
        [self.lineEditLeadManufacturer.addItem(k) for k in items]

        ipg_layout.addWidget(self.LeadManufacturer)
        ipg_layout.addWidget(self.lineEditLeadManufacturer)
        ipg_layout.addStretch()

        self.leads_layout = self.lead_manufacturer()
        self.hideLeadsLayoutIfNeeded()

        self.optionbox_IPGchoiceContent.addLayout(manufacturer_layout)
        self.optionbox_IPGchoiceContent.addLayout(ipg_layout)
        self.optionbox_IPGchoiceContent.addLayout(self.leads_layout)
        self.optionbox_IPGchoiceContent.addStretch(4)
        self.optionbox_IPGchoice.setLayout(self.optionbox_IPGchoiceContent)

        # Connect signals to slots
        self.lineEditLeadManufacturer.currentIndexChanged.connect(self.changed_index_comboboxIPG)
        self.lineEditIPG.currentIndexChanged.connect(self.changed_index_comboboxSystem)

    def lead_manufacturer(self):
        """Creates ComboBox that might be hidden or shown depending upon the input in ComboBoxes above"""

        leads_layout = QHBoxLayout()
        self.LabelLeads = QLabel('Implanted Leads?')
        self.lineEditLeads = QComboBox()
        self.lineEditLeads.addItem('')

        leads_layout.addWidget(self.LabelLeads)
        leads_layout.addWidget(self.lineEditLeads)
        leads_layout.addStretch()

        self.lineEditLeads.currentIndexChanged.connect(self.changed_index_comboboxLeads)

        return leads_layout

    def hideLeadsLayoutIfNeeded(self):
        """the leads combobox should only be called if there is some content in the system Combobox above"""
        if self.lineEditLeadManufacturer.currentText() == 'Please select a manufacturer':
            Content.object_visibility(self.leads_layout, action='hide')

    def DBS_parameters(self, layout_general, side, num_rows=3):
        """Optionbox for the DBS settings amplitude, pulse width and frequency """

        idx = 0 if side == 'left' else 1
        self.optionbox_dbs_settings = QGroupBox(f'DBS parameters - {side.capitalize()} target')
        self.optionbox_dbs_settingsContent = QHBoxLayout(self.optionbox_dbs_settings)
        layout_general.addWidget(self.optionbox_dbs_settings, 1, idx)

        for group_number in range(1, 3):
            group_layout = QVBoxLayout()
            settings_grid, settings_content = self.create_grid_bottom(
                lineedit_title=f'Group {str(group_number)}',
                num_rows=num_rows,
                contact_names=['test', 'Amp', 'Freq', 'PW'],
                side=idx
            )

            dbs_settings_layout = QHBoxLayout()
            if group_number == 1:
                FirstColumnNames = Content.create_first_column(num_rows=num_rows,
                                                               string2use=['Amplitude', 'Frequency', 'Pulse width'])
                dbs_settings_layout.addLayout(FirstColumnNames)

            dbs_settings_layout.addLayout(settings_grid)
            if group_number == 1:
                self.set_lineedit_state(dbs_settings_layout, enabled=True)

            group_layout.addLayout(dbs_settings_layout)
            self.group_layouts_settings.append(dbs_settings_layout)
            self.group_settings.append(settings_content)
            self.optionbox_dbs_settingsContent.addLayout(group_layout)

        return self.optionbox_dbs_settings

    def action_buttons_bottom(self, layout_general):
        """Create the action buttons at the bottom of the GUI"""

        self.optionbox_actionbutton = QGroupBox('')
        self.optionbox_actionbuttonContent = QVBoxLayout(self.optionbox_actionbutton)
        layout_general.addWidget(self.optionbox_actionbutton, 1, 3)

        layout_actionbuttons = QHBoxLayout()
        self.button_save_return = QPushButton('Save and Return')
        layout_actionbuttons.addWidget(self.button_save_return)

        self.optionbox_actionbuttonContent.addLayout(layout_actionbuttons)

        # Connect signals to slots
        self.button_save_return.clicked.connect(self.onClickedSaveReturn)

    def adapt_combobox(self, obj, action):
        """Update items in QComboBox; different actions are available, see below"""

        for i in range(obj.count()):
            item = obj.itemAt(i)

            if isinstance(item.widget(), QComboBox):
                combo_box = item.widget()

                if action == 'change_items':
                    combo_box.clear()
                    items = ['Please select the implanted leads']
                    items.extend(
                        Content.list_of_IPG(manufacturer_to_extract=self.lineEditLeadManufacturer.currentText()))
                    combo_box.addItems(items)
                    return
                elif action == 'return_contents':
                    return combo_box.currentText()

    def actions_for_selected(self):
        """Define actions to be taken when ComboBoxes are changed."""

        lead_selection = self.adapt_combobox(self.leads_layout, action='return_contents')
        manufacturer_selected = self.lineEditLeadManufacturer.currentText() != 'Please select a manufacturer'
        leads_selected = lead_selection != 'Please select the implanted leads'
        ipg_selected = self.lineEditIPG.currentText() != 'Please select an IPG'

        if manufacturer_selected and leads_selected and ipg_selected:
            self.settings_left, self.settings_leftContent = self.DBSsettings_specific(
                side='left', obj=self.settings_left, obj_content=self.settings_leftContent
            )
            self.settings_right, self.settings_rightContent = self.DBSsettings_specific(
                side='right', obj=self.settings_right, obj_content=self.settings_rightContent
            )

            self.settings_left.show()
            self.settings_right.show()
            Content.object_visibility(self.leads_layout, action='show')
        else:
            self.settings_left.hide()
            self.settings_right.hide()
            Content.object_visibility(self.leads_layout, action='hide')

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.itemAt(0)
                layout.removeItem(item)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clear_layout(item.layout())

    def set_lineedit_state(self, layout, enabled=False):
        for i in range(layout.count()):
            item = layout.itemAt(i)

            if item is not None:
                widget = item.widget()

                if isinstance(widget, QLineEdit):
                    widget.setEnabled(enabled)

                elif isinstance(widget, QLayout):
                    self.set_lineedit_state(widget, enabled)  # Recursively handle nested layouts

                elif widget is None:
                    # If the item is not a widget, it might be a layout or spacer.
                    # Check if it's a layout and handle it recursively.
                    if isinstance(item, QLayout):
                        self.set_lineedit_state(item, enabled)

    def create_grid_columntitle(self, name_title, num_rows: int, group_num, side, contact_names):
        """creates a grid with a title and a number of rows to be defined and returns two objects"""
        #GP: gives each lineedit a specific name corresponding to the ones in postoperative.csv
        content = []
        dbs_percentage_layout = QGridLayout()

        if side == 0:
            side = "L"
        else:
            side = "R"
        if name_title == "Anode":
            polarity = "ano"
        else:
            polarity = "ktd"

        # number_sidegroup_pol
        for i in range(1):  # Only one column
            dbs_percentage_layout.addWidget(QLabel(f'{name_title}:\t'), i, 0)
            for j in range(num_rows + 1):
                self.line_edit = QLineEdit()
                self.line_edit.setObjectName(f'{contact_names[j]}_{side}{group_num}_{polarity}') #GP: WHITESPACE as first char needed if template.csv not stripped!!!!!!!!!
                # print(self.line_edit.objectName())
                print(getattr(self.line_edit, 'objectName')())

                self.line_edit.setEnabled(False)
                self.line_edit.setFixedHeight(35)  # GP: ansonsten gibt es ein alignment-problem

                content.append(self.line_edit)
                dbs_percentage_layout.addWidget(self.line_edit, j + 1, i)

        return dbs_percentage_layout, content

    def create_grid_bottom(self, lineedit_title, num_rows: int, contact_names, side):
        """creates a grid with a title and a number of rows to be defined and returns two objects"""
        content = []
        dbs_percentage_layout = QGridLayout()
        if side == 0:
            side = "L"
        else:
            side = "R"
        if "1" in lineedit_title:
            group = "G1"
        elif "2" in lineedit_title:
            group = "G2"
        # contact_name_side_name_title
        for i in range(1):  # Only one column
            dbs_percentage_layout.addWidget(QLabel(f'{lineedit_title}:\t'), i, 0)
            for j in range(num_rows):
                self.line_edit = QLineEdit()
                self.line_edit.setObjectName(
                    f'{contact_names[j + 1]}_{side}{group}')
                # print(self.line_edit.objectName())
                print(getattr(self.line_edit, 'objectName')())

                self.line_edit.setEnabled(False)
                self.line_edit.setFixedHeight(35)  # GP: ansonsten gibt es ein alignment-problem

                content.append(self.line_edit)
                dbs_percentage_layout.addWidget(self.line_edit, j + 1, i)

        return dbs_percentage_layout, content

    @QtCore.pyqtSlot()
    def disable_SecondGroup(self):
        self.set_lineedit_state(self.group_layouts_contacts[1], enabled=False)
        self.set_lineedit_state(self.group_layouts_contacts[3], enabled=False)
        self.set_lineedit_state(self.group_layouts_settings[1], enabled=False)
        self.set_lineedit_state(self.group_layouts_settings[3], enabled=False)

    @QtCore.pyqtSlot()
    def enable_SecondGroup(self):
        self.set_lineedit_state(self.group_layouts_contacts[1], enabled=True)
        self.set_lineedit_state(self.group_layouts_contacts[3], enabled=True)
        self.set_lineedit_state(self.group_layouts_settings[1], enabled=True)
        self.set_lineedit_state(self.group_layouts_settings[3], enabled=True)

    @QtCore.pyqtSlot()
    def changed_index_comboboxIPG(self):
        self.adapt_combobox(self.leads_layout, action='change_items')
        Content.object_visibility(self.leads_layout, action='show')
        self.adjustSize()

    @QtCore.pyqtSlot()
    def changed_index_comboboxSystem(self):
        self.clear_layout(self.settings_leftContent)
        self.clear_layout(self.settings_rightContent)
        self.actions_for_selected()
        self.adjustSize()

    @QtCore.pyqtSlot()
    def changed_index_comboboxLeads(self):
        self.clear_layout(self.settings_leftContent)
        self.clear_layout(self.settings_rightContent)
        self.group_anode = []
        self.group_cathode = []
        self.group_layouts_contacts = []  # this ensures that group 2 may be made visible or not
        self.actions_for_selected()
        self.adjustSize()

    @QtCore.pyqtSlot()
    def onClickedSaveReturn(self):
        """Saves the entered information in a csv-file according to the self.date information"""
        missing_info = []
        if "Please" in self.lineEditIPG.currentText():
            missing_info.append("IPG")
        if "Please" in self.lineEditLeadManufacturer.currentText():
            missing_info.append("Lead Manufacturer")
        if "Please" in self.lineEditLeads.currentText():
            missing_info.append("Leads")

        if missing_info:
            QMessageBox.warning(self, 'Missing Information',
                                f"Please select the following information: {', '.join(missing_info)}")
        else:
            self.save_data2csv()
        #self.close()

    def update_inputs_with_existing_data(self):
        print("updating...")
        current_subj = General.read_current_subj()
        subject_id = current_subj['id'][0]
        df_general = Clean.extract_subject_data(subject_id)
        match = re.search(r'^(pre|intra|post)op', self.date)

        df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=',')
        if self.date == 'postoperative':
            try:
                df_subj = df.iloc[df.index[df['Reason_postop'] == self.reason][0], :].to_dict() #GP: new problems with DBSsettings for intraoperative
                print(df_subj.get('Lead_manufacturer'))
                print(df_subj.get('implanted_leads'))
                if pd.isna(df_subj.get('Implanted_IPG')):
                    print("No data for Implanted_IPG")
                    return
                elif pd.isna(df_subj.get('Lead_manufacturer')) and pd.isna(df_subj.get('implanted_leads')):
                    print("No data for Lead_manufacturer and implanted_leads")
                    return # No action needed if Lead_manufacturer or implanted_leads are empty
                else: # Update the inputs with existing data
                    print(df_subj.items())
                    #first change comboboxes to update layout:
                    self.lineEditIPG.setCurrentText(df_subj.get('Implanted_IPG'))
                    self.changed_index_comboboxIPG()

                    self.lineEditLeadManufacturer.setCurrentText(df_subj.get('Lead_manufacturer'))
                    self.changed_index_comboboxSystem()

                    self.lineEditLeads.setCurrentText(df_subj.get('implanted_leads'))
                    self.changed_index_comboboxLeads

                    #fill the rest, +/- is missing


                    for key, value in df_subj.items():
                        widget = self.findChild((QLineEdit, QComboBox), key)
                        if widget:
                            if isinstance(widget, QLineEdit):
                                widget.setText(value if value == str else str(value))
                            elif isinstance(widget, QComboBox):
                                pass
            except IndexError:
                print("IndexError")
                return  # No existing data for this reason
        elif self.date == 'intraoperative':
            try:
                df_subj = df.iloc[df.index[df['ID'] == subject_id][0],
                          :].to_dict()  # GP: new problems with DBSsettings for intraoperative
                if pd.isna(df_subj.get('Implanted_IPG')):
                    print("No data for Implanted_IPG")
                    return
                elif pd.isna(df_subj.get('Lead_manufacturer')) and pd.isna(df_subj.get('implanted_leads')):
                    print("No data for Lead_manufacturer and implanted_leads")
                    return  # No action needed if Lead_manufacturer or implanted_leads are empty
                else:  # Update the inputs with existing data
                    print(df_subj.items())
                    # first change comboboxes to update layout:
                    self.lineEditIPG.setCurrentText(df_subj.get('Implanted_IPG'))
                    self.changed_index_comboboxIPG()

                    self.lineEditLeadManufacturer.setCurrentText(df_subj.get('Lead_manufacturer'))
                    self.changed_index_comboboxSystem()

                    self.lineEditLeads.setCurrentText(df_subj.get('implanted_leads'))
                    self.changed_index_comboboxLeads

                    # fill the rest, +/- is missing

                    for key, value in df_subj.items():
                        widget = self.findChild((QLineEdit, QComboBox), key)
                        if widget:
                            if isinstance(widget, QLineEdit):
                                widget.setText(value if value == str else str(value))
                            elif isinstance(widget, QComboBox):
                                pass
            except IndexError:
                print(f"IndexError, no entry for {subject_id} found in {self.date}.csv")
                return  # No existing data for this reason



    def save_data2csv(self):
        #GP: copied from GUI-postoperative, not working yet
        """Saves the entered information in a csv-file according to the self.date information"""
        current_subj = General.read_current_subj()
        subject_id = current_subj['id'][0]
        df_general = Clean.extract_subject_data(subject_id)
        match = re.search(r'^(pre|intra|post)op', self.date)

        df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=',')
        if self.date == 'postoperative':
            try:
                df_subj = df.iloc[df.index[df['Reason_postop'] == self.reason][0], :].to_dict()
            except IndexError:
                df_subj = pd.Series(['nan' for _ in range(len(df.columns))], index=df.columns)

        elif self.date == 'intraoperative':
            try:
                df_subj = df.iloc[df.index[df['ID'] == subject_id][0], :].to_dict()
            except IndexError:
                df_subj = pd.Series(['nan' for _ in range(len(df.columns))], index=df.columns)


        df_general.reset_index(inplace=True, drop=True)
        df_subj['ID'] = General.read_current_subj().id[0]
        df_subj['PID_ORBIS'] = df_general.iloc[0, :]['PID_ORBIS']
        df_subj['Gender'] = df_general['gender'][0]
        #df_subj['Diagnosis_{}'.format(match.group())] = df_general['diagnosis'][0]

        # Save lead Implanted_IPG, Lead_manufacturer and implanted_leads
        df_subj['Implanted_IPG'] = self.lineEditIPG.currentText()
        df_subj['Lead_manufacturer'] = self.lineEditLeadManufacturer.currentText()
        df_subj['implanted_leads'] = self.lineEditLeads.currentText()

        # DBS-Leads Data
        data = {}
        # Collect data from group_anode and group_cathode
        for group in self.group_anode + self.group_cathode:
            for line_edit in group:
                object_name = line_edit.objectName()
                text = line_edit.text()
                data[object_name] = text

        # Collect data from group_settings
        for group in self.group_settings:
            for line_edit in group:
                object_name = line_edit.objectName()
                text = line_edit.text()
                data[object_name] = text

        print(data)

        # Update the DataFrame with the collected data
        for key, value in data.items():
            df_subj[key] = value
            if df_subj[key]:
                print("key", key, "value", value)

        if self.date == 'postoperative':
            indices_to_update = df.index[df['Reason_postop'] == self.reason]
        elif self.date == 'intraoperative':
            indices_to_update = df.index[df['ID'] == subject_id]

        # Check if any indices match the condition
        if not indices_to_update.empty:
            # Take the first index from the Int64Index object
            index_to_update = indices_to_update[0]
            df.loc[index_to_update] = df_subj
        else:
            # Handle the case when the index is not found
            print(f"Index for Reason_postop '{self.reason}' not found.")

        df.to_csv(Path(f"{FILEDIR}/{self.date}.csv"), index=False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = DBSsettingsDialog()
    dlg.show()
    sys.exit(app.exec_())
