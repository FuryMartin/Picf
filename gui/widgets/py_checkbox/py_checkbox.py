from gui.core.qt_core import *

style = '''
QCheckBox::indicator {{
    width: {_width};
    height: {_height};
    border: none;
	border-radius: {_radius};
	background-color: {_bg_color};
}}
QCheckBox::indicator:checked {{
    background-color: {_bg_color_pressed};
    border-style:solid;
    border-radius: {_radius};
    border-width:5px;
    border-color: #E6ff8c00;
}}
QCheckBox::indicator:unchecked:hover {{
    background-color: {_bg_color_hover};
}}
'''

class PyCheckbox(QCheckBox):
    def __init__(
        self,
        width,
        height,
        radius,
        bg_color,
        bg_color_pressed,
        bg_color_hover,
        parent=None,
    ):
        super().__init__()

        # SET PARAMETRES
        if parent != None:
            self.setParent(parent)
        #self.setCursor(Qt.PointingHandCursor)

        # SET STYLESHEET
        custom_style = style.format(
            _width = width,
            _height = height,
            _radius=radius,
            _bg_color=bg_color,
            _bg_color_pressed = bg_color_pressed,
            _bg_color_hover=bg_color_hover
        )
        self.setStyleSheet(custom_style)
