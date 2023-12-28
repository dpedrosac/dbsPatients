import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QStackedWidget, QLabel, QLineEdit

class MyGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Right-side options
        right_options = QComboBox(self)
        right_options.addItem("Please select an option")
        right_options.addItem("Option 1")
        right_options.addItem("Option 2")
        right_options.currentIndexChanged.connect(self.updateDisplay)

        # Stacked widget for left and right sections
        self.stacked_widget = QStackedWidget()

        # Left-side section
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Label 1"))
        left_layout.addWidget(QLineEdit())
        left_layout.addWidget(QLabel("Label 2"))
        left_layout.addWidget(QLineEdit())
        left_widget.setLayout(left_layout)

        # Add both sections to the stacked widget
        self.stacked_widget.addWidget(QWidget())  # Placeholder for "Please select an option"
        self.stacked_widget.addWidget(left_widget)

        # Add stacked widget and right-side options to the main layout
        layout.addWidget(right_options)
        layout.addWidget(self.stacked_widget)

        self.setLayout(layout)

        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('Dynamic GUI Example')
        self.show()

    def updateDisplay(self, index):
        # Show the corresponding section in the stacked widget
        self.stacked_widget.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyGUI()
    sys.exit(app.exec_())
