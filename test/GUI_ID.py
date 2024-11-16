import sys
from PyQt5 import QtCore

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QLabel, QFileDialog, QWidget


class Dialog(QDialog):
    """Dialog."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Patients PID')
        self.setGeometry(200, 100, 280, 170)
        self.move(850, 200)

        self.layout = QVBoxLayout(self)
        self.optionbox1 = QGroupBox('PID')
        self.settings_list = QVBoxLayout(self.optionbox1)

        # ====================    Create Content for First Option box on Top left      ====================
        self.subj_PID = QLabel('PID:\t\t')
        self.lineEditFilename = QLineEdit()
        lay1 = QHBoxLayout()
        lay1.addWidget(self.subj_PID)
        lay1.addWidget(self.lineEditFilename)
        lay1.addStretch()

        self.settings_list.addLayout(lay1)

        # ====================    Create Content for Buttons at the Bottom      ====================
        layout_bottom = QHBoxLayout()
        self.button_savereturn = QPushButton('Save settings \nand return')
        self.button_savereturn.clicked.connect(self.onClickedSaveReturn)
        self.button_close = QPushButton('Save and \nclose')
        self.button_close.clicked.connect(self.close)

        layout_bottom.addStretch(1)
        layout_bottom.addWidget(self.button_savereturn)
        layout_bottom.addWidget(self.button_close)

        self.layout.addWidget(self.optionbox1)
        self.layout.addLayout(layout_bottom)

        # In the next lines, actions are defined when Buttons are pressed

    @QtCore.pyqtSlot()
    def onClickedSaveReturn(self):
        self.saveFileDialog()

    def close(self):
        self.saveFileDialog()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "test.txt", "All Files(*)",
                                                  options=options)
        print(fileName)

    # for opening
    def open_dialog_box(self):
        option = QFileDialog.Options()
        # first parameter is self; second is the Window Title, third title is Default File Name, fourth is FileType,
        # fifth is options
        file = QFileDialog.getOpenFileName(self, "Save File Window Title", "default.txt", "All Files (*)",
                                           options=option)
        print(file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QWidget
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())
