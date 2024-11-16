# Hallo David
# Danke für die vielen Kommentare. Das ist wirklich sehr hilfreich.


import sys  # handles exit status of the application
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget

# create instance

app = QApplication(sys.argv)

# create instance of apllications GUI

window = QWidget()
window.setWindowTitle('DBS_Patients_Preoperative')  # define title
window.setGeometry(100, 100, 280, 80)  # define window size (x, y, width, height)
window.move(60, 15)
helloMsg = QLabel('<h1>Patient!</h1>', parent=window)  # uses HTML Test
helloMsg.move(60, 15)  # place the Hello Message to these coordinates

# show your applications GUI
window.show()  # adds new event to the applications event queue

# run apllication event loop
sys.exit(app.exec_())
