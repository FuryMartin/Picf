# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_pagesQXgmIk.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from gui.core.qt_core import *

class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(860, 600)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setStyleSheet(u"font-size: 14pt")
        self.horizontalLayout = QHBoxLayout(self.page_1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)



        self.horizontalLayout.addStretch()
        #############################################

        self.func_1 = QWidget()
        self.func_1.setObjectName(u"func_1")
        self.func_1.setStyleSheet(u"background: transparent;")
        self.func_1_layout = QVBoxLayout(self.func_1)
        self.func_1_layout.setObjectName("func_1_layout")

        self.func_1_lable = QLabel()
        self.func_1_lable.setObjectName(u"func_1_lable")
        self.func_1_lable.setStyleSheet(u"background: transparent;")
        self.func_1_lable.setText("识别分类")
        self.func_1_lable.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 20pt;color:white")
        self.func_1_lable.setAlignment(Qt.AlignCenter)


        self.func_1_frame_1 = QFrame()
        self.func_1_frame_1.setObjectName(u"func_1_frame_1")
        self.func_1_frame_1.setStyleSheet(u"background: transparent;")
        self.func_1_frame_1_layout = QHBoxLayout(self.func_1_frame_1)


        self.func_1_frame_2 = QFrame()
        self.func_1_frame_2.setObjectName(u"func_1_frame_2")
        self.func_1_frame_2.setStyleSheet(u"background: transparent;")
        self.func_1_frame_2_layout = QHBoxLayout(self.func_1_frame_2)

        self.func_1_layout.addStretch()
        self.func_1_layout.addWidget(self.func_1_lable)
        self.func_1_layout.addWidget(self.func_1_frame_1)
        self.func_1_layout.addWidget(self.func_1_frame_2)
        self.func_1_layout.addStretch()

        self.func_1_layout.setSpacing(50)
        self.horizontalLayout.addWidget(self.func_1)
        ##################################################################
        self.func_2 = QWidget()
        self.func_2.setObjectName(u"func_2")
        self.func_2.setStyleSheet(u"background: transparent;")
        self.func_2_layout = QVBoxLayout(self.func_2)
        self.func_2_layout.setObjectName("func_2_layout")

        self.func_2_lable = QLabel()
        self.func_2_lable.setObjectName(u"func_2_lable")
        self.func_2_lable.setStyleSheet(u"background: transparent;")
        self.func_2_lable.setText("人脸搜索")
        self.func_2_lable.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 20pt;color:white")
        self.func_2_lable.setAlignment(Qt.AlignCenter)


        self.func_2_frame_1 = QFrame()
        self.func_2_frame_1.setObjectName(u"func_2_frame_1")
        self.func_2_frame_1.setStyleSheet(u"background: transparent;")
        self.func_2_frame_1_layout = QHBoxLayout(self.func_2_frame_1)


        self.func_2_frame_2 = QFrame()
        self.func_2_frame_2.setObjectName(u"func_2_frame_2")
        self.func_2_frame_2.setStyleSheet(u"background: transparent;")
        self.func_2_frame_2_layout = QHBoxLayout(self.func_2_frame_2)

        self.func_2_layout.addStretch()
        self.func_2_layout.addWidget(self.func_2_lable)
        self.func_2_layout.addWidget(self.func_2_frame_1)
        self.func_2_layout.addWidget(self.func_2_frame_2)
        self.func_2_layout.addStretch()

        self.func_2_layout.setSpacing(50)
        self.horizontalLayout.addWidget(self.func_2)
        ######################################################################

        self.func_3 = QWidget()
        self.func_3.setObjectName(u"func_3")
        self.func_3.setStyleSheet(u"background: transparent;")
        self.func_3_layout = QVBoxLayout(self.func_3)
        self.func_3_layout.setObjectName("func_3_layout")

        self.func_3_lable = QLabel()
        self.func_3_lable.setObjectName(u"func_3_lable")
        self.func_3_lable.setStyleSheet(u"background: transparent;")
        self.func_3_lable.setText("相似筛查")
        self.func_3_lable.setStyleSheet(u"font-family:Microsoft Yahei;font-size: 20pt;color:white")
        self.func_3_lable.setAlignment(Qt.AlignCenter)


        self.func_3_frame_1 = QFrame()
        self.func_3_frame_1.setObjectName(u"func_3_frame_1")
        self.func_3_frame_1.setStyleSheet(u"background: transparent;")
        self.func_3_frame_1_layout = QHBoxLayout(self.func_3_frame_1)


        self.func_3_frame_2 = QFrame()
        self.func_3_frame_2.setObjectName(u"func_3_frame_2")
        self.func_3_frame_2.setStyleSheet(u"background: transparent;")
        self.func_3_frame_2_layout = QHBoxLayout(self.func_3_frame_2)

        self.func_3_layout.addStretch()
        self.func_3_layout.addWidget(self.func_3_lable)
        self.func_3_layout.addWidget(self.func_3_frame_1)
        self.func_3_layout.addWidget(self.func_3_frame_2)
        self.func_3_layout.addStretch()


        self.func_3_layout.setSpacing(50)
        self.horizontalLayout.addWidget(self.func_3)
        #################################################################

        self.horizontalLayout.addStretch()

        self.pages.addWidget(self.page_1)

        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2_layout = QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.pages.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setStyleSheet(u"QFrame {\n"
"	font-size: 16pt;\n"
"}")
        self.page_3_layout = QVBoxLayout(self.page_3)
        self.page_3_layout.setObjectName(u"page_3_layout")
        self.scrollArea_1= QScrollArea(self.page_3)
        self.scrollArea_1.setObjectName(u"scrollArea")
        self.scrollArea_1.setStyleSheet(u"background: transparent;")
        self.scrollArea_1.setFrameShape(QFrame.NoFrame)
        self.scrollArea_1.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea_1.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 100, 30))
        self.scrollAreaWidgetContents.setStyleSheet(u"background: transparent;")
        self.gridLayout_2 = QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.scrollArea_1.setWidget(self.scrollAreaWidgetContents)

        self.page_3_layout.addWidget(self.scrollArea_1)

        self.pages.addWidget(self.page_3)
        ############################################################################
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.page_4.setStyleSheet(u"QFrame {\n"
"	font-size: 16pt;\n"
"}")
        self.page_4_layout = QVBoxLayout(self.page_4)
        self.page_4_layout.setObjectName(u"page_4_layout")
        self.scrollArea_2 = QScrollArea(self.page_4)
        self.scrollArea_2.setObjectName(u"scrollArea_2")
        self.scrollArea_2.setStyleSheet(u"background: transparent;")
        self.scrollArea_2.setFrameShape(QFrame.NoFrame)
        self.scrollArea_2.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea_2.setWidgetResizable(True)

        self.page_4_layout.addWidget(self.scrollArea_2)

        self.pages.addWidget(self.page_4)
        #############################################################################
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.page_5.setStyleSheet(u"QFrame {\n"
"	font-size: 16pt;\n"
"}")
        self.page_5_layout = QVBoxLayout(self.page_5)
        self.page_5_layout.setObjectName(u"page_5_layout")
        self.scrollArea_3 = QScrollArea(self.page_5)
        self.scrollArea_3.setObjectName(u"scrollArea_3")
        self.scrollArea_3.setStyleSheet(u"background: transparent;")
        self.scrollArea_3.setFrameShape(QFrame.NoFrame)
        self.scrollArea_3.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea_3.setWidgetResizable(True)

        self.page_5_layout.addWidget(self.scrollArea_3)

        self.pages.addWidget(self.page_5)
        #############################################################################

        self.main_pages_layout.addWidget(self.pages)

        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
    # retranslateUi

