import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic, sip
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtWidgets import *

from res.constants import *
from res.database import Database

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi(UI_FILE_DIR, self)
        self.local_db = Database()

        self.lbl_notice = self.findChild(QLabel, 'lbl_notice')
        self.title = self.findChild(QLabel, 'lbl_title')
        self.page_stack = self.findChild(QStackedWidget, 'stackedWidget')
        self.today_tasks_bar = self.set_today_progress_bar(0)
        self.slider_weekday_rollover = self.findChild(QSlider, 'sld_weekday_rollover')
        self.slider_weekday_rollover.valueChanged.connect(self.change_rollover_lbl)

        self.setup()
        self.show()

    def setup(self):
        self.set_weekday_icon()
        self.setup_today_tasks()
        self.refresh_today_tasks()
        self.set_pages()
        self.setup_new_task_page()
        self.lbl_notice.setText(NOTICE_WELCOME)

    def set_today_progress_bar(self, value):
        today_tasks_bar = self.findChild(QProgressBar, 'bar_today_tasks')
        today_tasks_bar.setValue(value)
        return today_tasks_bar

    def set_pages(self):
        dashboard_page = self.findChild(QWidget, 'dashboard_page')
        manage_task_page = self.findChild(QWidget, 'manage_task_page')
        new_task_page = self.findChild(QWidget, 'new_task_page')
        progress_page = self.findChild(QWidget, 'progress_page')
        calendar_page = self.findChild(QWidget, 'calendar_page')

        btn_add_weekday = self.findChild(QPushButton, 'btn_add_weekday')
        btn_add_weekday.clicked.connect(lambda: self.add_weekday_task())
        btn_toggle = self.findChild(QPushButton, 'Btn_Toggle')
        btn_toggle.clicked.connect(lambda: self.toggle_side_menu())
        btn_exit = self.findChild(QPushButton, 'btn_exit')
        btn_exit.clicked.connect(lambda: self.close())
        self.page_stack.setCurrentWidget(dashboard_page)

        btn_dashboard_page = self.findChild(QPushButton, 'btn_dashboard_page')
        btn_manage_task_page = self.findChild(QPushButton, 'btn_manage_task_page')
        btn_new_task_page = self.findChild(QPushButton, 'btn_new_task_page')
        btn_progress_page = self.findChild(QPushButton, 'btn_progress_page')
        btn_calendar_page = self.findChild(QPushButton, 'btn_calendar_page')

        btn_dashboard_page.clicked.connect(lambda: self.change_page(dashboard_page, "Dashboard"))
        btn_manage_task_page.clicked.connect(lambda: self.change_page(manage_task_page, "Manage Tasks"))
        btn_new_task_page.clicked.connect(lambda: self.change_page(new_task_page, "New Task"))
        btn_progress_page.clicked.connect(lambda: self.show_week_progress(progress_page))
        btn_calendar_page.clicked.connect(lambda: self.change_page(calendar_page, "Calendar Events"))

    def change_page(self, page, title):
        self.page_stack.setCurrentWidget(page)
        self.title.setText(title)

    def show_week_progress(self, progress_page):
        self.change_page(progress_page, "My Progress")
        self.refresh_week_progress_bars()

    def refresh_week_progress_bars(self):
        last_week_dates = get_last_week_dates()
        for index, day_date in enumerate(last_week_dates):
            percentage = self.local_db.get_weekday_tasks_completion_percentage(day_date, index)
            bar_last_day = self.findChild(QProgressBar, 'bar_last_'+WEEKDAYS[index])
            bar_last_day.setValue(int(percentage))

    def setup_new_task_page(self):
        for day_index in range(7):
            day_checkbox = self.findChild(QCheckBox, WEEKDAY_NEW_TASK_CHECKBOXES[day_index])
            day_tile = WEEKDAY_NEW_TASK_TILES[day_index]
            day_checkbox.clicked.connect(lambda: self.update_new_weekday_checkbox_frame())
        for checkbox in WEEKDAY_CHECKBOXES:
            checkbox = self.findChild(QCheckBox, checkbox)
            checkbox.setStyleSheet(WEEKDAY_CHECKBOX_STYLESHEET)

    def change_rollover_lbl(self):
        weekday_task_rollover = self.findChild(QLabel, 'lbl_rollover')
        "Task Roll Over: 0 Day(s)"
        value = self.slider_weekday_rollover.value()
        weekday_task_rollover.setText(f'Task Roll Over: {value} Day(s)')

    def update_new_weekday_checkbox_frame(self):
        for checkbox_name in WEEKDAY_NEW_TASK_CHECKBOXES:
            checkbox = self.findChild(QCheckBox, checkbox_name)
            checkbox_frame = self.findChild(QFrame, WEEKDAY_NEW_TASK_TILES[WEEKDAY_NEW_TASK_CHECKBOXES.index(checkbox_name)])
            if checkbox.isChecked():
                checkbox_frame.setStyleSheet(NEW_WEEKDAY_TASK_TILE_CHECKED)
            else:
                checkbox_frame.setStyleSheet(NEW_WEEKDAY_TASK_TILE_UNCHECKED)

    def set_weekday_icon(self):
        day_index = get_weekday_index()
        for weekday_index in range(7):
            if weekday_index == day_index:
                self.findChild(QLabel, WEEKDAY_TITLE_LABELS[weekday_index]).setStyleSheet(
                    f'color: {DAY_BAR_ACTIVE};')
                self.findChild(QFrame, WEEKDAY_UNDER_FRAMES[weekday_index]).setStyleSheet(
                    f'background-color: {DAY_BAR_ACTIVE};')
            else:
                self.findChild(QLabel, WEEKDAY_TITLE_LABELS[weekday_index]).setStyleSheet(
                    f'color: {TASK_TEXT_COMPLETED};')
                self.findChild(QFrame, WEEKDAY_UNDER_FRAMES[weekday_index]).setStyleSheet(
                    f'background-color: {DAY_BAR_INACTIVE};')

    def setup_today_tasks(self):
        today_tasks_frame = self.findChild(QFrame, 'todayTasksFrame')
        frame_layout = QVBoxLayout(today_tasks_frame)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        self.today_tasks_container = QWidget(today_tasks_frame)
        scroll_area = QScrollArea(today_tasks_frame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.today_tasks_container)
        frame_layout.addWidget(scroll_area)

    def refresh_today_tasks(self):
        try:
            self.delete_layout(self.today_tasks_layout)
            self.today_tasks_layout = QVBoxLayout(self.today_tasks_container)

        except AttributeError:
            self.today_tasks_layout = QVBoxLayout(self.today_tasks_container)

        self.today_tasks_container.setLayout(self.today_tasks_layout)

        today_tasks = self.local_db.get_today_tasks(WEEKDAYS[get_weekday_index()])

        for task in today_tasks:
            TaskItem(task[0], task[1], task[2], self.today_tasks_layout, self.today_tasks_bar, (100 / len(today_tasks)), self.local_db, self.refresh_today_tasks)
            line = QFrame()
            line.setStyleSheet("background-color: #141617;")
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Raised)
            self.today_tasks_layout.addWidget(line)

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
