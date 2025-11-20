from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QVBoxLayout #QHBoxLayout

#App Settings
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("My first App")
main_window.resize(300,200)

#Create all Object/Widgets below here


main_window.show()
app.exec_()