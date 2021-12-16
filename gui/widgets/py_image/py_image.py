from gui.core.qt_core import *
from .. py_push_button import *
from .. py_checkbox import *

class PyImage(QWidget):
    def __init__(
        self,
        filepath
    ):
        super().__init__()
        #self.setAlignment(Qt.AlignLeft)
        self.setStyleSheet("background:'transparent';border:none")
        self.setMinimumSize(200, 200)
        self.setGeometry(QRect(0,0,200,200))
        #self.setMaximumSize(200, 200)
        #self.layoutDirection('')
        self.filepath = filepath
        #self.setStyleSheet('padding:5px')
        self.image = QLabel(self)
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setFrameShape(QFrame.NoFrame)
        self.image.setGeometry(QRect(10, 10, 180, 180))
        self.image.setStyleSheet("background:transparent")

        self.set_image()
        
        self.checkbox = PyCheckbox(
            radius=5,
            width = 180,
            height = 180,
            bg_color="transparent",
            bg_color_pressed="transparent",
            bg_color_hover="transparent",  # "",
            parent=self
        )
        #width与height要与图片相同
        #self.checkbox.setGraphicsEffect(QGraphicsOpacityEffect().setOpacity(1))
        #self.checkbox.setStyleSheet("QCheckBox::indicator { width: 180px; height: 180px; }")
        #self.checkbox.setMinimumSize(200,200)
        #self.checkbox.setMaximumSize(200,200)
        index = self.filepath.rfind('\\',0,len(self.filepath))
        filename = self.filepath[index+1:]
        self.checkbox.setObjectName(filename)
        self.checkbox.setGeometry(QRect(5, 5, 190,190))
        #为边框留出空间，左上角坐标减少border，整体长宽增加2*border
        self.checkbox.setChecked(False)
        #self.checkbox.stateChanged.connect(lambda: self.btnstate(self.checkbox))
        #elf.btn.setStyleSheet("background:rgba(0, 0, 0, 1)")
        #解决间距变化的问题：https://stackoverflow.com/questions/31150330/qt-qgridlayout-different-spacing-of-header-row-needed

    def btnstate(self, btn):
        if self.checkbox.isChecked():
            print("BUTTON Checked, State={}".format(self.checkbox.objectName()))
        else:
            print("BUTTON not Checked, State={}".format(
                str(self.checkbox.checkState())))


    def set_image(self):
        '''
        
        pix_img = pix_img.convertToFormat(QImage.Format_RGB888)
        pix_img = QPixmap.fromImage(pix_img)
        pix_img = pix_img.scaled(300, 300, Qt.KeepAspectRatio)
        super().setPixmap(pix_img)
        pix_img = QPixmap(self.filepath)
        pix_img = pix_img.scaled(
            200, 200, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        super().setPixmap(pix_img)
        '''
        img = QPixmap.fromImage(self.cut_image())
        #img = img.scaled(180, 180, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        img = self.set_round_rec(img)
        self.image.setPixmap(img)
    
    def set_round_rec(self,img):
        target = QPixmap(img.size())
        target.fill(QColor("transparent"))
        painter = QPainter(target)
        painter_path = QPainterPath()
        painter.setRenderHint(QPainter.Antialiasing, True)
        #painter.setRenderHint(QPainter.HighQualityAntialiasing, True)
        painter_path.addRoundedRect(0,0,180,180,5,5)
        painter.setClipPath(painter_path)
        painter.drawPixmap(0, 0, img)
        return target

    def cut_image(self):
        image = QImageReader()
        image.setFileName(self.filepath)
        image.setAutoTransform(True)
        
        img_size = image.size()
        if img_size.width() > img_size.height():
            ratio = img_size.height()/180
        else:
            ratio = img_size.width()/180

        width = int(img_size.width()/ratio)
        height = int(img_size.height()/ratio)

        image.setScaledSize(QSize(width,height))
        image_size = min(width,height)

        rect = QRect(
            (width - image_size) / 2,
            (height - image_size) / 2,
            image_size,
            image_size,
        )
        image = QPixmap.fromImageReader(image)
        image = image.copy(rect)
        out_img = QImage(image_size, image_size, QImage.Format_ARGB32)
        out_img.fill(Qt.transparent)

        painter = QPainter(out_img)
        brush = QBrush(image)
        painter.setBrush(brush)
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, image_size, image_size)
        painter.end()
        return out_img
