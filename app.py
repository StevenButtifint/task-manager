
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

    def set_today_progress_bar(self, value):
        today_tasks_bar = self.findChild(QProgressBar, 'bar_today_tasks')
        today_tasks_bar.setValue(value)
        return today_tasks_bar


    def delete_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.delete_layout(item.layout())
            sip.delete(layout)

    def toggle_side_menu(self):
        frame_left_menu = self.findChild(QFrame, 'frame_left_menu')
        current_width = frame_left_menu.width()
        end_value = SIDE_MENU_MAX

        if current_width == end_value:
            end_value = SIDE_MENU_MIN

        self.animation = QPropertyAnimation(frame_left_menu, b"minimumWidth")
        self.animation.setDuration(400)
        self.animation.setStartValue(current_width)
        self.animation.setEndValue(end_value)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def add_weekday_task(self):
        task_title_qle = self.findChild(QLineEdit, 'led_weekday_title')
        task_description_pte = self.findChild(QPlainTextEdit, 'pte_weekday_desc')
        rollover_slider = self.findChild(QSlider, 'sld_weekday_rollover')

        day_checkboxes_bool = []
        for day_checkbox in WEEKDAY_CHECKBOXES:
            checkbox = self.findChild(QCheckBox, day_checkbox)
            day_checkboxes_bool.append(int(checkbox.isChecked()))
            checkbox.setChecked(False)
        self.local_db.add_weekday_task(task_title_qle.text(), task_description_pte.toPlainText(), *day_checkboxes_bool, rollover_slider.value())
        self.refresh_today_tasks()

        self.clear_new_weekday_task_entry(task_title_qle, task_description_pte, rollover_slider)

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
