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

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
import time


from . functions_main_window import *
from utils.face_functions import get_duplicate_pics, search_person_pics, sorter_main
from utils.embedder import differ_paths, get_image_paths
import utils.embedder as EMBEDDER

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from gui.core.qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT THEME COLORS
# ///////////////////////////////////////////////////////////////
from gui.core.json_themes import Themes

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *

# MAIN FUNCTIONS 
# ///////////////////////////////////////////////////////////////
from . functions_main_window import *

from . flow_layout import *


# PY WINDOW
# ///////////////////////////////////////////////////////////////
class SetupMainWindow:
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # ADD LEFT MENUS
    # ///////////////////////////////////////////////////////////////
    add_left_menus = [
        {
            "btn_icon" : "icon_home.svg",
            "btn_id" : "btn_home",
            "btn_text" : "Home",
            "btn_tooltip" : "Home page",
            "show_top" : True,
            "is_active" : True
        },
        {
            "btn_icon": "icon_folder_open.svg",
            "btn_id": "btn_page_pics",
            "btn_text": "open pics",
            "btn_tooltip": "open pics",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_search.svg",
            "btn_id": "btn_page_search",
            "btn_text": "open page search",
            "btn_tooltip": "open page search",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_signal.svg",
            "btn_id": "btn_page_duplicate",
            "btn_text": "open page duplicate",
            "btn_tooltip": "open page duplicate",
            "show_top": True,
            "is_active": False
        },
        {
            "btn_icon": "icon_settings.svg",
            "btn_id": "btn_settings",
            "btn_text": "open Settings",
            "btn_tooltip": "open Settings",
            "show_top": False,
            "is_active": False
        }

    ]

     # ADD TITLE BAR MENUS
    # ///////////////////////////////////////////////////////////////
    add_title_bar_menus = []

    # SETUP CUSTOM BTNs OF CUSTOM WIDGETS
    # Get sender() function when btn is clicked
    # ///////////////////////////////////////////////////////////////
    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()
        elif self.ui.left_column.menus.verticalLayout.sender() != None:
            return self.ui.left_column.menus.verticalLayout.sender()

    # SETUP MAIN WINDOW WITH CUSTOM PARAMETERS
    # ///////////////////////////////////////////////////////////////
    def setup_gui(self):
        # APP TITLE
        # ///////////////////////////////////////////////////////////////
        self.setWindowTitle(self.settings["app_name"])
        
        # REMOVE TITLE BAR
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

        # ADD GRIPS
        # ///////////////////////////////////////////////////////////////
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)

        # LEFT MENUS / GET SIGNALS WHEN LEFT MENU BTN IS CLICKED / RELEASED
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)

        # SET SIGNALS
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)

        # TITLE BAR / ADD EXTRA BUTTONS
        # ///////////////////////////////////////////////////////////////
        # ADD MENUS
        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)

        # SET SIGNALS
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)

        # ADD Title
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Welcome to PyOneDark")

        # LEFT COLUMN SET SIGNALS
        # ///////////////////////////////////////////////////////////////
        self.ui.left_column.clicked.connect(self.btn_clicked)
        self.ui.left_column.released.connect(self.btn_released)

        # SET INITIAL PAGE / SET LEFT AND RIGHT COLUMN MENUS
        # ///////////////////////////////////////////////////////////////
        MainFunctions.set_page(self, self.ui.load_pages.page_1)
        MainFunctions.set_left_column_menu(
            self,
            menu = self.ui.left_column.menus.menu_1,
            title = "Settings Left Column",
            icon_path = Functions.set_svg_icon("icon_settings.svg")
        )
        MainFunctions.set_right_column_menu(self, self.ui.right_column.menu_1)

        # ///////////////////////////////////////////////////////////////
        # EXAMPLE CUSTOM WIDGETS
        # Here are added the custom widgets to pages and columns that
        # were created using Qt Designer.
        # This is just an example and should be deleted when creating
        # your application.
        #
        # OBJECTS FOR LOAD PAGES, LEFT AND RIGHT COLUMNS
        # You can access objects inside Qt Designer projects using
        # the objects below:
        #
        # <OBJECTS>
        # LEFT COLUMN: self.ui.left_column.menus
        # RIGHT COLUMN: self.ui.right_column
        # LOAD PAGES: self.ui.load_pages
        # </OBJECTS>
        # ///////////////////////////////////////////////////////////////

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # LOAD THEME COLOR
        # ///////////////////////////////////////////////////////////////
        themes = Themes()
        self.themes = themes.items
        self.ui.load_pages.page_1.setStyleSheet

        self.ui.credits.person_name.returnPressed.connect(lambda: MainFunctions.exec_edit_single_group_name(self, self.ui.credits.person_name))
        #################################################################
        # 选择文件夹
        self.func_btn_11 = PyPushButton(
            text = '选择文件夹',
            radius = 8,
            color = self.themes['app_color']['white'],
            bg_color = self.themes['app_color']['dark_one'],
            bg_color_hover = self.themes['app_color']['dark_three'],
            bg_color_pressed = self.themes['app_color']['orange']
        )
        self.func_btn_11.setMaximumWidth(200)
        self.func_btn_11.setMinimumWidth(200)
        self.func_btn_11.setMinimumHeight(40)

        self.func_btn_11.clicked.connect(lambda: MainFunctions.select_image_directory(self))
        
        #################################################################
        # 识别分类
        self.func_btn_12 = PyPushButton(
            text = '开始识别',
            radius = 8,
            color = self.themes['app_color']['white'],
            bg_color = self.themes['app_color']['dark_one'],
            bg_color_hover = self.themes['app_color']['dark_three'],
            bg_color_pressed = self.themes['app_color']['orange']
        )
        self.func_btn_12.setMaximumWidth(200)
        self.func_btn_12.setMinimumWidth(200)
        self.func_btn_12.setMinimumHeight(40)

        def detect_finished():
            self.timer.stop()
            self.ui.credits.copyright_label.setText("完成识别，耗时 {} 秒".format(self.timer_count))
            QMessageBox.information(self, "", "完成识别")
        def print_time():
            try:
                processed_image = EMBEDDER.global_counter.value
            except AttributeError:
                processed_image = 0
            self.timer_count = int(time.time() - self.t0)
            if processed_image == 0:
                self.ui.credits.copyright_label.setText("正在加载模型，已开始 {} 秒".format(self.timer_count))
                #print("正在加载模型，已开始 {} 秒".format(self.timer_count))
            elif processed_image == self.total_image:
                self.ui.credits.copyright_label.setText("识别完成，正在分类，已开始 {} 秒".format(self.timer_count))
            else:
                self.ui.credits.copyright_label.setText("正在识别中，{}/{}，已开始 {} 秒".format(processed_image, self.total_image, self.timer_count))
                #print("正在识别中，{}/{}，已识别 {} 秒".format(processed_image, self.total_image, self.timer_count))

        def create_detect_worker():
            self.t0 = time.time()
            self.timer_count = 0
            self.timer = QTimer()
            self.timer.timeout.connect(lambda: print_time())
            self.timer.start(100)

            image_paths = get_image_paths(self.settings['image_path'])
            image_paths = differ_paths(image_paths, self.settings['image_path'])
            self.total_image = len(image_paths)
            if self.total_image== 0:
                self.ui.credits.copyright_label.setText("共有 0 张新增图片，识别取消")
                return None

            #print("Found {} images..".format(self.total_image))

            self.worker_detect = Worker('Detect', image_paths)
            self.worker_detect.start()
            self.worker_detect.finished.connect(detect_finished)

        self.worker_detect = Worker('Detect')
        self.func_btn_12.clicked.connect(lambda: create_detect_worker())
        #################################################################
        # 人脸搜索
        self.func_btn_21 = PyPushButton(
            text = '选择图片',
            radius = 8,
            color = self.themes['app_color']['white'],
            bg_color = self.themes['app_color']['dark_one'],
            bg_color_hover = self.themes['app_color']['dark_three'],
            bg_color_pressed = self.themes['app_color']['orange']
        )
        self.func_btn_21.setMaximumWidth(200)
        self.func_btn_21.setMinimumWidth(200)
        self.func_btn_21.setMinimumHeight(40)
        self.func_btn_21.clicked.connect(lambda: MainFunctions.select_single_image(self))

        self.func_btn_22 = PyPushButton(
            text = '开始查找',
            radius = 8,
            color = self.themes['app_color']['white'],
            bg_color = self.themes['app_color']['dark_one'],
            bg_color_hover = self.themes['app_color']['dark_three'],
            bg_color_pressed = self.themes['app_color']['orange']
        )
        self.func_btn_22.setMaximumWidth(200)
        self.func_btn_22.setMinimumWidth(200)
        self.func_btn_22.setMinimumHeight(40)

        def get_person_search_result(path):
            self.person_search_result = path
            self.ui.credits.copyright_label.setText("搜索完成")
            QMessageBox.information(self, "", "搜索完成")
        def create_search_worker(path):
            self.search_changed = True
            self.has_searched = True
            self.ui.credits.copyright_label.setText("正在进行人脸搜索，请稍等")
            self.worker_search = Worker('Search', path)
            self.worker_search.start()
            self.worker_search.finished.connect(get_person_search_result)
        def call_create_search_worker():
            try:
                create_search_worker(self.selected_image)
            except AttributeError:
                QMessageBox.information(self, "", "还未选择照片，请先选择照片后再开始搜索")
        self.search_changed = False
        self.has_searched = False
        self.func_btn_22.clicked.connect(lambda: call_create_search_worker())
        
        ###################################################################

        self.func_btn_31 = PyPushButton(
            text = '开始筛查',
            radius = 8,
            color = self.themes['app_color']['white'],
            bg_color = self.themes['app_color']['dark_one'],
            bg_color_hover = self.themes['app_color']['dark_three'],
            bg_color_pressed = self.themes['app_color']['orange']
        )
        self.func_btn_31.setMaximumWidth(200)
        self.func_btn_31.setMinimumWidth(200)
        self.func_btn_31.setMinimumHeight(40)

        self.func_btn_32 = QFrame()
        self.func_btn_32.setStyleSheet(u"background: transparent;")
        self.func_btn_32.setMaximumWidth(200)
        self.func_btn_32.setMinimumWidth(200)
        self.func_btn_32.setMinimumHeight(40)
        def get_person_duplicate_result(path):
            self.person_duplicate_result = path
            self.image_pages = []
            self.ui.credits.copyright_label.setText("完成筛查")
            QMessageBox.information(self, "", "完成筛查")
        def create_duplicate_worker(path):
            self.found_duplicate_image = True
            self.ui.credits.copyright_label.setText("正在进行相似图片筛查，请稍等")
            self.worker_duplicate = Worker('Duplicate', path)
            self.worker_duplicate.start()
            self.worker_duplicate.finished.connect(get_person_duplicate_result)
        self.func_btn_31.clicked.connect(lambda: create_duplicate_worker(self.settings['image_path']))
        self.found_duplicate_image = False
        ###################################################################

        self.ui.load_pages.func_1_frame_1_layout.addWidget(self.func_btn_11,Qt.AlignCenter,Qt.AlignCenter)
        self.ui.load_pages.func_1_frame_2_layout.addWidget(self.func_btn_12,Qt.AlignCenter,Qt.AlignCenter)
        self.ui.load_pages.func_2_frame_1_layout.addWidget(self.func_btn_21,Qt.AlignCenter,Qt.AlignCenter)
        self.ui.load_pages.func_2_frame_2_layout.addWidget(self.func_btn_22,Qt.AlignCenter,Qt.AlignCenter)
        self.ui.load_pages.func_3_frame_1_layout.addWidget(self.func_btn_31,Qt.AlignCenter,Qt.AlignCenter)
        self.ui.load_pages.func_3_frame_2_layout.addWidget(self.func_btn_32,Qt.AlignCenter,Qt.AlignCenter)



        # ADD Widgets
        # ///////////////////////////////////////////////////////////////
        #SetupMainWindow.load_image(self)
        #MainFunctions.load_images(self)
        #MainFunctions.load_persons(self)

        # LEFT COLUMN
        # ///////////////////////////////////////////////////////////////

        # ///////////////////////////////////////////////////////////////
        # END - EXAMPLE CUSTOM WIDGETS
        # ///////////////////////////////////////////////////////////////

    # RESIZE GRIPS AND CHANGE POSITION
    # Resize or change position when window is resized
    # ///////////////////////////////////////////////////////////////
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)
    
    def get_flow_layout(self):
        return self.flow_layout

    def get_frame(self):
        return self.frame

    def remove_pic(self):
        temp_widget = SetupMainWindow.get_flow_layout(self).itemAt(0).widget()
        #从flow_layout中删除第0张图片
        SetupMainWindow.get_flow_layout(self).removeWidget(temp_widget)
        SetupMainWindow.get_flow_layout(self).update()

class Worker(QThread):
    finished = Signal(dict)
    def __init__(self, mode, path = ''):
        super().__init__()
        self.mode = mode 
        if path != '':
            self.path = path

    def run(self):
        if self.mode == "Detect":
            sorter_main(self.path)
            self.finished.emit({})
        elif self.mode == "Search":
            result = search_person_pics(self.path)
            self.finished.emit(result)
        elif self.mode == "Duplicate":
            result = get_duplicate_pics(self.path)
            self.finished.emit(result)
            #print(result)
        pass


