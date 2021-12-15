from gui.core.qt_core import *
from gui.uis.windows.main_window.flow_layout import FlowLayout

class PyImagePage(QFrame):
    def __init__(self):
        super().__init__()
        self.flow_layout = FlowLayout()
        self.button_box = QButtonGroup()
        self.button_box.setExclusive(True)
        self.setStyleSheet("background: transparent")
        self.setFrameShape(QFrame.NoFrame)
        self.setLayout(self.flow_layout)
        self.flow_layout_boxs = []

