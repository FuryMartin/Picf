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
import sys

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from gui.core.qt_core import *

# LOAD UI MAIN
# ///////////////////////////////////////////////////////////////
from . ui_main import *

from . flow_layout import *

from utils.display_by_person import *

import os
import json

# FUNCTIONS
class MainFunctions():
    def __init__(self):
        super().__init__()
        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

    # SET MAIN WINDOW PAGES
    # ///////////////////////////////////////////////////////////////
    def set_page(self, page):
        self.ui.load_pages.pages.setCurrentWidget(page)

    # SET LEFT COLUMN PAGES
    # ///////////////////////////////////////////////////////////////
    def set_left_column_menu(
        self,
        menu,
        title,
        icon_path
    ):
        self.ui.left_column.menus.menus.setCurrentWidget(menu)
        self.ui.left_column.title_label.setText(title)
        self.ui.left_column.title_label.setAlignment(Qt.AlignCenter)
        self.ui.left_column.icon.set_icon(icon_path)

    # RETURN IF LEFT COLUMN IS VISIBLE
    # ///////////////////////////////////////////////////////////////
    def left_column_is_visible(self):
        width = self.ui.left_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    # RETURN IF RIGHT COLUMN IS VISIBLE
    # ///////////////////////////////////////////////////////////////
    def right_column_is_visible(self):
        width = self.ui.right_column_frame.width()
        if width == 0:
            return False
        else:
            return True

    # SET RIGHT COLUMN PAGES
    # ///////////////////////////////////////////////////////////////
    def set_right_column_menu(self, menu):
        self.ui.right_column.menus.setCurrentWidget(menu)

    # GET TITLE BUTTON BY OBJECT NAME
    # ///////////////////////////////////////////////////////////////
    def get_title_bar_btn(self, object_name):
        return self.ui.title_bar_frame.findChild(QPushButton, object_name)

    # GET TITLE BUTTON BY OBJECT NAME
    # ///////////////////////////////////////////////////////////////
    def get_left_menu_btn(self, object_name):
        return self.ui.left_menu.findChild(QPushButton, object_name)
    
    # LEDT AND RIGHT COLUMNS / SHOW / HIDE
    # ///////////////////////////////////////////////////////////////
    def toggle_left_column(self):
        # GET ACTUAL CLUMNS SIZE
        width = self.ui.left_column_frame.width()
        right_column_width = self.ui.right_column_frame.width()

        MainFunctions.start_box_animation(self, width, right_column_width, "left")

    def toggle_right_column(self):
        # GET ACTUAL CLUMNS SIZE
        left_column_width = self.ui.left_column_frame.width()
        width = self.ui.right_column_frame.width()

        MainFunctions.start_box_animation(self, left_column_width, width, "right")

    def start_box_animation(self, left_box_width, right_box_width, direction):
        right_width = 0
        left_width = 0
        time_animation = self.ui.settings["time_animation"]
        minimum_left = self.ui.settings["left_column_size"]["minimum"]
        maximum_left = self.ui.settings["left_column_size"]["maximum"]
        minimum_right = self.ui.settings["right_column_size"]["minimum"]
        maximum_right = self.ui.settings["right_column_size"]["maximum"]

        # Check Left Values        
        if left_box_width == minimum_left and direction == "left":
            left_width = maximum_left
        else:
            left_width = minimum_left

        # Check Right values        
        if right_box_width == minimum_right and direction == "right":
            right_width = maximum_right
        else:
            right_width = minimum_right       

        # ANIMATION LEFT BOX        
        self.left_box = QPropertyAnimation(self.ui.left_column_frame, b"minimumWidth")
        self.left_box.setDuration(time_animation)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        # ANIMATION RIGHT BOX        
        self.right_box = QPropertyAnimation(self.ui.right_column_frame, b"minimumWidth")
        self.right_box.setDuration(time_animation)
        self.right_box.setStartValue(right_box_width)
        self.right_box.setEndValue(right_width)
        self.right_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.stop()
        self.group.addAnimation(self.left_box)
        self.group.addAnimation(self.right_box)
        self.group.start()

    def load_persons(self):
        self.persons = get_persons_more(get_persons('output.json'))
        self.temp_widget = QWidget()
        self.person_group = QButtonGroup()
        self.btn_boxes_layout = QVBoxLayout(self.temp_widget)
        for name, paths in self.persons.items():
            #print(paths)
            #print("PK")
            btn = PyPushButton(
                text=name,
                radius = 5,
                color = self.themes["app_color"]["white"],
                bg_color =  self.themes["app_color"]["dark_one"],
                bg_color_hover = self.themes['app_color']['orange'],
                bg_color_pressed = self.themes['app_color']['orange']
            )
            btn.setMinimumHeight(25)
            btn.setMaximumHeight(25)
            self.btn_boxes_layout.addWidget(btn)
            btn.paths = paths
            btn.clicked.connect(lambda: MainFunctions.load_images_by_person(self))
            btn.DoubleClickSig.connect(lambda: MainFunctions.exec_edit_group_name(self))
            btn.setObjectName("Person")
            btn.setCheckable(True)
            self.person_group.addButton(btn)
        self.btn_boxes_layout.addStretch()
        self.btn_boxes_layout.setSpacing(10)
        try:
            if self.ui.left_column.menus.verticalLayout.count() > 0:
                self.ui.left_column.menus.verticalLayout.itemAt(0).widget().setParent(None)
                self.ui.left_column.menus.verticalLayout.removeWidget(self.ui.left_column.menus.verticalLayout.itemAt(0).widget())
                self.ui.left_column.menus.verticalLayout.update()
        except AttributeError:
            pass

        self.ui.left_column.menus.verticalLayout.addWidget(self.temp_widget)
        self.image_dic = {}

    def load_images_by_person(self):
        self.ui.credits.copyright_label.setText("正在加载图片，请稍后")
        self.ui.credits.person.setText("")
        self.ui.credits.person_name.setText("")
        self.ui.credits.person_name.setFocusPolicy(Qt.WheelFocus)
        self.ui.credits.person_name.setReadOnly(False)
        self.ui.credits.image.setText("")
        self.ui.credits.image_title.setText("")
        self.ui.credits.update()
        QApplication.processEvents()
        #print(btn.text())
        #print(btn.paths)
        btn = self.person_group.checkedButton()
        MainFunctions.load_image_page(self,name=btn.text(), paths=btn.paths)
        MainFunctions.update_image_count(self, len(btn.paths))
        self.ui.credits.person_name.setText(btn.text())
        QApplication.processEvents()
        #MainFunctions.load_images(self, btn.paths)

    def load_image_page(self, name, paths):
        try:
            self.ui.load_pages.gridLayout_2.itemAt(0).widget().setParent(None)
            self.ui.load_pages.gridLayout_2.removeWidget(self.ui.load_pages.gridLayout_2.itemAt(0).widget())
        except AttributeError:
            pass
        image_page = PyImagePage()
        if name not in self.image_dic:
            self.image_dic[name] = image_page
            MainFunctions.load_images(self, paths, image_page)
            QApplication.processEvents()
        #self.image_dic[name].setParent(self.ui.load_pages.gridLayout_2)
        self.ui.load_pages.gridLayout_2.addWidget(self.image_dic[name])
        #self.ui.load_pages.scrollArea_1.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def load_images(self, paths, image_page):
        for count, path in enumerate(paths):
            path = os.path.normpath(os.path.join(self.settings['image_path'], path))
            image_box = PyImage(path)
            #image_page.button_box.setAutoExclusive(False)
            image_box.checkbox.stateChanged.connect(lambda: MainFunctions.get_checked_button(self, image_page))
            image_page.flow_layout_boxs.append(image_box)
            image_page.flow_layout.addWidget(image_box)
            image_page.button_box.addButton(image_box.checkbox)
            image_page.flow_layout.update()
            self.ui.load_pages.gridLayout_2.update()
            QApplication.processEvents()
        #print(image_page.flow_layout_boxs)


    def update_image_count(self, count):
        self.ui.credits.copyright_label.setText("总数量：{}".format(str(count)))
        self.ui.credits.person.setText("人物名：")
        self.ui.credits.person_name.setText("")
        self.ui.credits.person_name.setFocusPolicy(Qt.WheelFocus)
        self.ui.credits.person_name.setReadOnly(False)
        self.ui.credits.image.setText("图片名：")
        self.ui.credits.image_title.setText("")
        self.ui.credits.update()

    def load_main_credit_bar(self):
        self.ui.credits.copyright_label.setText(self.settings["copyright"])
        self.ui.credits.person.setText("")
        self.ui.credits.person_name.setText("")
        self.ui.credits.person_name.setFocusPolicy(Qt.NoFocus)
        self.ui.credits.person_name.setReadOnly(True)
        self.ui.credits.image.setText("")
        self.ui.credits.image_title.setText("")
        self.ui.credits.update()

    def get_checked_button(self,image_page):
        btn = image_page.button_box.checkedButton()
        print("{} Checked".format(btn.objectName())) 
        self.ui.credits.image_title.setText(btn.objectName())
            
    def get_flow_layout(self):
        return self.flow_layout

    def select_single_image(self):
        m = QFileDialog.getOpenFileName(None,"选取文件","./","图片 (*.png *.jpg *.jpeg *.tiff *.bmp);;")
        self.selected_image = m[0]
        self.ui.credits.copyright_label.setText("选择图片：{}".format(self.selected_image))
        return m[0]

    def select_image_directory(self):
        directory = QFileDialog.getExistingDirectory(None, "C:/")
        with open('resources/settings.json', 'r+',encoding='utf-8') as f:
            if directory == '':
                print("No folder selected")
                return None
            self.settings = json.load(f)
            self.settings['image_path'] = directory
            f.seek(0)
            f.truncate()
            f.write(json.dumps(self.settings,indent=4,ensure_ascii=False))
        #print("Get Image Folder:{}".format(directory))
        self.ui.credits.copyright_label.setText("选择文件夹：{}".format(directory))
        #self.settings["image_path"] = directory
        return directory
    
    def load_search_result(self):
        if not self.has_searched:
            self.ui.credits.copyright_label.setText("还未选择图片")
            self.ui.credits.person.setText("")
            self.ui.credits.person_name.setText("")
            self.ui.credits.person_name.setFocusPolicy(Qt.NoFocus)
            self.ui.credits.person_name.setReadOnly(True)
            self.ui.credits.image.setText("")
            self.ui.credits.image_title.setText("")
            return None
        else:
            name, paths = tuple(self.person_search_result.items())[0]
            self.ui.credits.copyright_label.setText("总数量：{}".format(len(paths)))
            self.ui.credits.person.setText("人物名：")
            self.ui.credits.person_name.setText(name)
            self.ui.credits.person_name.setFocusPolicy(Qt.NoFocus)
            self.ui.credits.person_name.setReadOnly(True)
            self.ui.credits.image.setText("图片名：")
            self.ui.credits.image_title.setText("")
        
        if not self.search_changed:
            return None

        self.search_changed = False
        try:
            self.scrollArea_2_WidgetContents.setParent(None)
            self.ui.load_pages.scrollArea_2.removeWidget(self.scrollArea_2_WidgetContents)
        except AttributeError:
            pass

        self.scrollArea_2_WidgetContents = QWidget()
        self.scrollArea_2_WidgetContents.setObjectName(u"scrollArea_2_WidgetContents")
        self.scrollArea_2_WidgetContents.setGeometry(QRect(0, 0, 100, 30))
        self.scrollArea_2_WidgetContents.setStyleSheet(u"background: transparent;")
        self.scrollArea_2_layout = QVBoxLayout(self.scrollArea_2_WidgetContents)
        self.scrollArea_2_layout.setSpacing(0)
        self.scrollArea_2_layout.setObjectName(u"verticalLayout")
        self.scrollArea_2_layout.setContentsMargins(0, 0, 0, 0)
        self.ui.load_pages.scrollArea_2.setWidget(self.scrollArea_2_WidgetContents)
        #self.scrollArea_2_layout.addStretch(50)

        self.ui.credits.copyright_label.setText("正在加载图片")
        self.ui.credits.person.setText("")
        self.ui.credits.person_name.setText("")
        self.ui.credits.person_name.setFocusPolicy(Qt.NoFocus)
        self.ui.credits.person_name.setReadOnly(True)
        self.ui.credits.image.setText("")
        self.ui.credits.image_title.setText("")
        QApplication.processEvents()

        try:
            self.target_image_box = QWidget()
            self.target_image_box_layout = QHBoxLayout(self.target_image_box)
            self.target_image_box_layout.setAlignment(Qt.AlignCenter)
            self.target_image = PyImage(self.selected_image)
            self.target_image_box_layout.addWidget(self.target_image)
            self.target_image.checkbox.setCheckable(False)  


            self.search_target_lable = QLabel()
            self.search_target_lable.setObjectName(u"search_target_lable")
            self.search_target_lable.setStyleSheet(u"background: transparent;")
            self.search_target_lable.setText("所选照片")
            self.search_target_lable.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt")
            self.search_target_lable.setAlignment(Qt.AlignCenter)
            self.scrollArea_2_layout.addWidget(self.search_target_lable)

            self.scrollArea_2_layout.addWidget(self.target_image_box)
        except AttributeError:

            #print("还未选择图片")
            return None

        self.search_result_lable = QLabel()
        self.search_result_lable.setObjectName(u"search_result_lable")
        self.search_result_lable.setStyleSheet(u"background: transparent;")
        self.search_result_lable.setText("搜索结果")
        self.search_result_lable.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 14pt")
        self.search_result_lable.setAlignment(Qt.AlignCenter)
        self.scrollArea_2_layout.addWidget(self.search_result_lable)
        self.scrollArea_2_layout.update()
        self.scrollArea_2_WidgetContents.update()
        self.ui.load_pages.scrollArea_2.update()


        #print(self.person_search_result)
        image_page = PyImagePage()
        for name, paths in self.person_search_result.items():
            for path in paths:
                path = os.path.normpath(os.path.join(self.settings['image_path'], path))
                image_box = PyImage(path)
                image_box.checkbox.stateChanged.connect(lambda: MainFunctions.get_checked_button(self, image_page))
                image_page.flow_layout_boxs.append(image_box)
                image_page.flow_layout.addWidget(image_box)
                image_page.button_box.addButton(image_box.checkbox)
                image_page.flow_layout.update()
                self.scrollArea_2_layout.update()
                #QApplication.processEvents()
            self.ui.credits.copyright_label.setText("总数量：{}".format(len(paths)))
            self.ui.credits.person.setText("人物名：")
            self.ui.credits.person_name.setText(name)
            self.ui.credits.person_name.setFocusPolicy(Qt.NoFocus)
            self.ui.credits.person_name.setReadOnly(True)
            self.ui.credits.image.setText("图片名：")
            self.ui.credits.image_title.setText("")

        self.scrollArea_2_layout.addWidget(image_page)
        self.scrollArea_2_layout.addStretch()
        self.scrollArea_2_layout.setSpacing(20)

    def load_duplicate_result(self):
        ########################################################################
        # ADD Confirm Button
        ########################################################################
        if not self.found_duplicate_image:
            self.ui.credits.copyright_label.setText("还未进行相似性筛查")
            self.ui.credits.person.setText("")
            self.ui.credits.person_name.setText("")
            self.ui.credits.person_name.setFocusPolicy(Qt.NoFocus)
            self.ui.credits.person_name.setReadOnly(True)
            self.ui.credits.image.setText("")
            self.ui.credits.image_title.setText("")
            return None
        else:            
            self.ui.credits.copyright_label.setText("正在加载图片")
            self.ui.credits.person.setText("")
            self.ui.credits.person_name.setText("")
            self.ui.credits.person_name.setFocusPolicy(Qt.NoFocus)
            self.ui.credits.person_name.setReadOnly(True)
            self.ui.credits.image.setText("")
            self.ui.credits.image_title.setText("")
            QApplication.processEvents()

            if len(self.image_pages) != 0:
                self.ui.credits.copyright_label.setText("选择要删除的图片并点击确定")
                return None

        """"""
        try:
            self.ui.load_pages.page_5_layout.itemAt(1).widget().setParent(None)
            self.ui.load_pages.page_5_layout.removeWidget(self.ui.load_pages.page_5_layout.itemAt(1).widget())
        except AttributeError:
            pass
        
        self.commit_delete_button = PyPushButton(
            text = '确定',
            radius = 8,
            color = self.themes['app_color']['white'],
            bg_color = self.themes['app_color']['dark_one'],
            bg_color_hover = self.themes['app_color']['orange'],
            bg_color_pressed = self.themes['app_color']['orange']
        )
        self.commit_delete_button.setMinimumHeight(40)
        self.ui.load_pages.page_5_layout.addWidget(self.commit_delete_button)
        self.commit_delete_button.clicked.connect(lambda: MainFunctions.get_reserved_images(self))

        #########################################################################
        # ADD Pics
        #########################################################################
        self.scrollArea_3_WidgetContents = QWidget()
        self.scrollArea_3_WidgetContents.setObjectName(u"scrollArea_3_WidgetContents")
        self.scrollArea_3_WidgetContents.setGeometry(QRect(0, 0, 100, 30))
        self.scrollArea_3_WidgetContents.setStyleSheet(u"background: transparent;")
        self.ui.load_pages.scrollArea_3.setWidget(self.scrollArea_3_WidgetContents)
        self.scrollArea_3_layout = QVBoxLayout(self.scrollArea_3_WidgetContents)
        self.scrollArea_3_layout.setSpacing(0)
        self.scrollArea_3_layout.setObjectName(u"verticalLayout")
        self.scrollArea_3_layout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_3_layout.setSpacing(20)

        try:
            for paths in self.person_duplicate_result:
                image_page = PyImagePage()
                image_page.button_box.setExclusive(False)
                self.scrollArea_3_layout.addWidget(image_page)
                for path in paths:
                    path = os.path.normpath(os.path.join(self.settings['image_path'], path))
                    image_box = PyImage(path)
                    image_page.flow_layout_boxs.append(image_box)
                    image_page.flow_layout.addWidget(image_box)
                    image_page.button_box.addButton(image_box.checkbox)
                    image_page.flow_layout.update()
                    self.scrollArea_3_layout.update()
                self.image_pages.append(image_page)
            QApplication.processEvents()
            """
            for image in self.person_duplicate_result:
                print(image)
            """
        except AttributeError:
            print("还未进行相似筛查")
            return None
        self.ui.credits.copyright_label.setText("选择要删除的图片并点击确定")


    def get_reserved_images(self):
        #print(self.image_pages)
        checked_buttons = []
        unchecked_buttons = []
        image_page_to_delete = []
        for image_page in self.image_pages:
            buttons = image_page.button_box.buttons()
            checked_widgets = []
            for index, button in enumerate(buttons):
                if button.isChecked():
                    #print(index)
                    checked_buttons.append(button.objectName())
                    checked_widgets.append(image_page.flow_layout.itemAt(index).widget())
                    # 从image_page.button_box中移除button
                    image_page.button_box.removeButton(button)
            # 从image_page中移除checked_widget
            for checked_widget in checked_widgets:
                checked_widget.setParent(None)
                image_page.flow_layout.removeWidget(checked_widget)
                image_page.flow_layout.update()
                QApplication.processEvents()
            # 如果image_page中的图片为零，从scrollArea_3_layout中移除image_page
            if image_page.flow_layout.count() == 0:
                image_page.setParent(None)
                self.scrollArea_3_layout.removeWidget(image_page)
                image_page_to_delete.append(image_page)
                QApplication.processEvents()
        for image_page in image_page_to_delete:
            self.image_pages.remove(image_page)
        print(checked_buttons)
        self.persons = delete_multi_pic(self.settings['image_path'],checked_buttons, get_persons('output.json'))
        write_json(self.persons)
        MainFunctions.load_persons(self)


    def exec_edit_single_group_name(self, person_name_editer):
        new_name = person_name_editer.text()
        btn = self.person_group.checkedButton()
        origin_name = btn.text()

        checked_image = self.image_dic[origin_name].button_box.checkedButton()
        path = checked_image.objectName()

        origin_buttons = self.image_dic[origin_name].button_box.buttons()
        index = origin_buttons.index(checked_image)

        origin_widget = self.image_dic[origin_name].flow_layout.itemAt(index).widget()

        self.image_dic[origin_name].button_box.removeButton(checked_image)
        self.image_dic[origin_name].flow_layout.removeWidget(origin_widget)
        self.image_dic[origin_name].flow_layout.update()
        checked_image.setParent(None)
        origin_image_page = self.image_dic[origin_name]
        """
        new_name_existed = False
        if new_name in self.image_dic:
            new_name_existed = True
            self.image_dic[new_name].button_box.addButton(checked_image)
            self.image_dic[new_name].flow_layout.addWidget(origin_widget)
            self.image_dic[new_name].flow_layout.update()
            new_image_page = self.image_dic[new_name]
        """

        self.persons = edit_single_group_name(new_name, path, get_persons('output.json'))
        write_json(self.persons)
        MainFunctions.load_persons(self)
        

        self.image_dic[origin_name] = origin_image_page
        """
        if new_name_existed:
            self.image_dic[new_name] = new_image_page
        """
        #MainFunctions.update_image_count(self, len(self.persons[origin_name]))
        #MainFunctions.load_image_page(self,name = origin_name, paths=self.persons[origin_name])
        buttons = self.person_group.buttons()
        for button in buttons:
            if button.text() == origin_name:
                #print(button.text())
                button.setChecked(True)
                self.ui.credits.person_name.setText(button.text())
                break
        QApplication.processEvents()

    def exec_edit_group_name(self):
        btn = self.person_group.checkedButton()
        input_dialog = QInputDialog(self)
        new_name, ok = input_dialog.getText(self, "更改名称", "New Name:")
        if ok:
            self.persons = edit_group_name(new_name, btn.text(), get_persons('output.json'))
            write_json(self.persons)
            MainFunctions.load_persons(self)
            if new_name != "错误分类":
                MainFunctions.update_image_count(self, len(self.persons[new_name]))
                MainFunctions.load_image_page(self,name = new_name, paths=self.persons[new_name])
            QApplication.processEvents()
            #print(btn.text())