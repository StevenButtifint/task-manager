
import sys
import platform
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

from res.constants import *
from res.database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.local_db = Database()


    def clear_new_weekday_task_entry(self, title_entry, description_entry, rollover_slider):
        for day_checkbox in WEEKDAY_CHECKBOXES:
            checkbox = self.findChild(QCheckBox, day_checkbox)
            checkbox.setChecked(False)

        for day_tile in WEEKDAY_NEW_TASK_TILES:
            tile = self.findChild(QFrame, day_tile)
            tile.setStyleSheet(NEW_WEEKDAY_TASK_TILE_UNCHECKED)

        title_entry.clear()
        description_entry.clear()
        rollover_slider.setValue(0)
        self.change_rollover_lbl()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec_())
