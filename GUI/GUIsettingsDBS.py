#!/usr/bin/env python3
import sys, re
import pandas as pd
import numpy as np
from PyQt5 import QtCore
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QGroupBox, \
    QHBoxLayout, QLabel, QGridLayout, QSpacerItem, QSizePolicy, QComboBox, QStackedWidget, QLayout

import dependencies
from utils.helper_functions import General, Content
from dependencies import FILEDIR

pd.options.mode.chained_assignment = None


class DBSsettingsDialog(QWidget):
    """Dialog to introduce the medication at a specific date."""

    def __init__(self, rows, visit='postoperative', parent=None):
        super(DBSsettingsDialog, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.rows = rows
        self.date = visit  # ensures the right date is entered
        self.group_layouts_contacts = []  # this ensures that group 2 may be made visible or not
        self.group_layouts_settings = []  # this ensures that group 2 may be made visible or not

        self.adjustSize()
        self.setup_ui()

    def setup_ui(self):
        self.setup_general_layout()

    def setup_general_layout(self):
        """Defines the general layout for the GUI"""

        subj_details = General.read_current_subj() # reads information for the subject last bein processed
        self.setWindowTitle('Postoperative DBS settings (PID: {})'.format(str(int(subj_details.pid))))  # not necessary

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
            contact_name.insert(0, 'IPG')
        except KeyError:
            return obj, obj_content

        for group_number in range(1, 3):
            layout, dbs_percentage_layout = QVBoxLayout(), QHBoxLayout()
            layout.addWidget(QLabel(f"Group {group_number}"))

            anode_grid = Content.create_grid_columntitle(side_label=side.capitalize(), name_title="Anode",
                                                         num_rows=num_contacts + 1)
            cathode_grid = Content.create_grid_columntitle(side_label=side.capitalize(), name_title="Cathode",
                                                           num_rows=num_contacts + 1)

            if group_number == 1:
                FirstColumnNames = Content.create_first_column(num_rows=num_contacts + 1,
                                                               string2use=contact_name)
                dbs_percentage_layout.addLayout(FirstColumnNames)

            dbs_percentage_layout.addLayout(anode_grid)
            dbs_percentage_layout.addLayout(cathode_grid)  # adds both layouts

            if group_number == 1:
                self.set_lineedit_state(dbs_percentage_layout, enabled=True)
            layout.addLayout(dbs_percentage_layout)

            if group_number == 2:
                toggle_layout = QVBoxLayout()
                toggleButton1 = QPushButton('+', self)
                toggleButton1.setFixedSize(20, 20)  # Set a fixed size
                toggleButton2 = QPushButton('-', self)
                toggleButton2.setFixedSize(20, 20)  # Set a fixed size
                toggle_layout.addWidget(toggleButton1)
                toggle_layout.addWidget(toggleButton2)
                obj_content.addLayout(toggle_layout)
            obj_content.addLayout(layout)
            self.group_layouts_contacts.append(dbs_percentage_layout)  # needed to toggle visibility of 2nd group later

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
            settings_grid = Content.create_grid_columntitle(side_label='Group', name_title=f'Group{str(group_number)}',
                                                            num_rows=num_rows)

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
        # self.button_save_return.clicked.connect(self.onClickedSaveReturn)

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
        self.group_layouts_contacts = []  # this ensures that group 2 may be made visible or not
        self.actions_for_selected()
        self.adjustSize()

    @QtCore.pyqtSlot()
    def onClickedSaveReturn(self):
        """Saves the entered information in a csv-file according to the self.date information"""

        subj_id = General.read_current_subj().id[0]  # reads data from current_subj (saved in ./tmp)
        df = General.import_dataframe('{}.csv'.format(self.date), separator_csv=',')

        match = re.search(r'^(pre|intra|post)op', self.date)  # gets the condition, to ensure correct saving.
        df_items = {v.format('_{}'.format(match.group())).replace(' ', '_'): v.format('').replace(' ', '_')
                    for v in self.medication_names}

        try:
            idx2replace = df.index[df['ID'] == subj_id][0]  # looks for index at dataframe in which data shall be stored
            df_subj = df.iloc[idx2replace, :]
            df.iloc[idx2replace, :] = df_subj
            first_index = False
        except IndexError:
            df_subj = df
            df_subj.loc[0, 'ID'] = General.read_current_subj().id[0]
            df_subj.loc[0, 'PID_ORBIS'] = General.read_current_subj().pid[0]
            first_index = True

        for k, v in df_items.items():
            df_subj[k] = eval('self.lineEdit{}.text()'.format(v)) if v != 'Other' \
                else eval('self.lineEdit{}.toPlainText()'.format(v))
        if first_index:
            df = df.append(df_subj, ignore_index=True)
        else:
            df.iloc[idx2replace, :] = df_subj

        df = df.replace(['nan', ''], [np.nan, np.nan])
        df.to_csv(Path(f"{FILEDIR}/{self.date}.csv"), index=False)

        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = DBSsettingsDialog(rows=8)
    dlg.show()
    sys.exit(app.exec_())
