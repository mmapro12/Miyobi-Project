from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from designs.main_design import Ui_MainWindow
import sys
import miyobi


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui_design = Ui_MainWindow()
        self.ui_design.setupUi(self)

        self.CreateConnects()
    
    def CreateConnects(self):
        self.ui_design.start_button.clicked.connect(self.startProgram)
    
    def startProgram(self):
        cam, q_but  = self.getStartSettings()
        miyobi.main()
    
    def getStartSettings(self):
        camera = self.ui_design.camera_select.currentIndex()
        q_button = self.ui_design.out_button.text()

        return camera, q_button


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
