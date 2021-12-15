# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from gui.widgets.py_line_edit.py_line_edit import PyLineEdit
from gui.core.qt_core import *

# PY CREDITS BAR AND VERSION
# ///////////////////////////////////////////////////////////////
class PyCredits(QWidget):
    def __init__(
        self,
        bg_two,
        copyright,
        version,
        font_family,
        text_size,
        text_description_color,
        radius = 8,
        padding = 5,
        text = "",
        place_holder_text = "",
        border_size = 2,
        color = "#FFF",
        selection_color = "#FFF",
        bg_color = "#333",
        bg_color_active = "#222",
        context_color = "#00ABE8",
    ):
        """
        text = "",
        place_holder_text = "",
        radius = 8,
        border_size = 2,
        color = "#FFF",
        selection_color = "#FFF",
        bg_color = "#333",
        bg_color_active = "#222",
        context_color = "#00ABE8"
        """
        super().__init__()

        # PROPERTIES
        self._copyright = copyright
        self._version = version
        self._bg_two = bg_two
        self._font_family = font_family
        self._text_size = text_size
        self._text_description_color = text_description_color
        self._radius = radius
        self._padding = padding
        self._text = text
        self._place_holder_text = place_holder_text
        self._border_size = border_size
        self._color = color
        self._selection_color = selection_color
        self._bg_color = bg_color
        self._bg_color_active = bg_color_active
        self._context_color = context_color

        # SETUP UI
        self.setup_ui()

    def setup_ui(self):
        # ADD LAYOUT
        self.widget_layout = QHBoxLayout(self)
        self.widget_layout.setContentsMargins(0,0,0,0)

        # BG STYLE
        style_credits = f"""
        #bg_frame {{
            border-radius: {self._radius}px;
            background-color: {self._bg_two};
        }}
        .QLabel {{
            font: {self._text_size}pt "{self._font_family}";
            color: {self._text_description_color};
            padding-left: {self._padding}px;
            padding-right: {self._padding}px;
        }}
        """

        # BG FRAME
        self.bg_frame = QFrame()
        self.bg_frame.setObjectName("bg_frame")
        self.bg_frame.setStyleSheet(style_credits)


        # ADD TO LAYOUT
        self.widget_layout.addWidget(self.bg_frame)

        # ADD BG LAYOUT
        self.bg_layout = QHBoxLayout(self.bg_frame)
        self.bg_layout.setContentsMargins(0,0,0,0)

        # ADD COPYRIGHT TEXT
        self.copyright_label = QLabel(self._copyright)
        self.copyright_label.setAlignment(Qt.AlignVCenter)


        style_person_line = f'''
        QLineEdit {{
            background-color: {self._bg_color};
            border-radius: {self._radius}px;
            border: {self._border_size}px solid transparent;
            padding-left: 0px;
            padding-right: 0px;
            selection-color: {self._selection_color};
            selection-background-color: {self._context_color};
            color: {self._color};
        }}
        QLineEdit:focus {{
            border: {self._border_size}px solid {self._context_color};
            background-color: {self._bg_color_active};
        }}
        '''

        self.person_groupbox = QFrame()
        self.person_groupbox.setObjectName("person_groupbox")
        #self.person_groupbox.setMinimumWidth(80)

        self.person_layout = QHBoxLayout(self.person_groupbox)
        self.bg_layout.setContentsMargins(0,0,0,0)

        self.person = QLabel()
        self.person.setAlignment(Qt.AlignCenter)
        self.person.setMaximumWidth(80)
        self.person_layout.addWidget(self.person)

        self.person_name = PyLineEdit()
        self.person_name.setAlignment(Qt.AlignCenter)
        self.person_name.setStyleSheet(style_person_line)
        self.person_name.setReadOnly(True)
        self.person_name.setFocusPolicy(Qt.NoFocus)
        self.person_layout.addWidget(self.person_name)

        
        self.title_groupbox = QFrame()
        self.title_groupbox.setObjectName("title_groupbox")

        self.title_layout = QHBoxLayout(self.title_groupbox)

        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setMaximumWidth(80)
        self.title_layout.addWidget(self.image)

        self.image_title = QLabel("")
        self.image_title.setAlignment(Qt.AlignCenter)
        self.title_layout.addWidget(self.image_title)

        # ADD VERSION TEXT
        self.version_label = QLabel(self._version)
        self.version_label.setAlignment(Qt.AlignVCenter)

        # SEPARATOR
        self.separator = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # ADD TO LAYOUT
        self.bg_layout.addWidget(self.copyright_label)
        self.bg_layout.addSpacerItem(self.separator)
        #self.bg_layout.addWidget(self.person_name)
        self.bg_layout.addWidget(self.person_groupbox)
        self.bg_layout.addSpacerItem(self.separator)
        self.bg_layout.addWidget(self.title_groupbox)
        self.bg_layout.addSpacerItem(self.separator)
        self.bg_layout.addWidget(self.version_label)
