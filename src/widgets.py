from PyQt6.QtWidgets import *
from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtCore import QSize, Qt, QThread, QTimer


class BaseMixin:
    def __init__(self, master, width=None, height=None, tag='', cursor=False, **kwargs):
        super().__init__(master, **kwargs)

        if width is not None and height is not None:
            self.setFixedSize(width, height)
        if tag:
            self.setObjectName(tag)
        if cursor:
            self.setCursor(Qt.CursorShape.PointingHandCursor)


class ImageMixin:
    @staticmethod
    def get_path(path, is_full=False):
        return path if is_full else f'assets/images/{path}'


class Widget(BaseMixin, QWidget): pass


class StackedWidget(BaseMixin, QStackedWidget): pass


class Frame(BaseMixin, QFrame): pass


class ScrollArea(BaseMixin, QScrollArea): pass


class ComboBox(BaseMixin, QComboBox): pass


class CheckBox(BaseMixin, QCheckBox): pass


class ProgressBar(BaseMixin, QProgressBar): pass


class LineEdit(BaseMixin, QLineEdit): pass


class TextEdit(BaseMixin, QTextEdit): pass


class Label(BaseMixin, ImageMixin, QLabel):
    def set_image(self, path, all_path=False, size=None):
        image = QImage(self.get_path(path, all_path))
        if size:
            image = image.scaled(QSize(*size),
                                 transformMode=Qt.TransformationMode.SmoothTransformation)

        if QThread.currentThread() == self.thread():
            self.setPixmap(QPixmap.fromImage(image))
        else:
            QTimer.singleShot(0, lambda img=image: self.setPixmap(QPixmap.fromImage(img)))


class Button(BaseMixin, ImageMixin, QPushButton):
    def __init__(self, master, width, height, text='', **kwargs):
        super().__init__(master, width, height, text=text, **kwargs)

    def set_function(self, func):
        try:
            self.clicked.disconnect()
        except TypeError:
            pass

        self.clicked.connect(func)

    def set_icon(self, path, size=None, all_path=False):
        self.setIcon(QIcon(self.get_path(path, all_path)))
        if size:
            self.setIconSize(QSize(*size))


class Message(QMessageBox):
    def __init__(self, icon_type, title, text, info=''):
        super().__init__()

        icons = {
            'info': QMessageBox.Icon.Information,
            'warn': QMessageBox.Icon.Warning,
            'crit': QMessageBox.Icon.Critical
        }

        self.setIcon(icons.get(icon_type, QMessageBox.Icon.Information))
        self.setWindowTitle(title)
        self.setText(text)
        self.setInformativeText(info)
        self.exec()
