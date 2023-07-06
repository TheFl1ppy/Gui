from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QDesktopWidget, QHeaderView
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor
import pyodbc
import sys


class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()

        screen = QDesktopWidget().screenGeometry()
        width = screen.width()
        height = screen.height()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnBottomHint | Qt.WindowDoesNotAcceptFocus)
        self.setAttribute(Qt.WA_MacAlwaysShowToolWindow, True)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(int(width / 2.5), int(height / 5))
        self.setStyleSheet("background-color: transparent;")
        self.setWindowOpacity(0.9)
        self.setEnabled(False)

        # Создаем вертикальный макет и добавляем его в окно
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.table_widget = QTableWidget(self)
        self.table_widget.setWindowOpacity(0.8)
        self.table_widget.setEnabled(False)
        self.table_widget.setStyleSheet("""
            font: bold italic;
            color: gray;
            font-size: maximum;
        """)

        number = "Номер"
        city = "Город"
        building = "Учреждение"
        device = "Прибор"
        havePC = "Наличие ПК"
        lastdate = "Дата сдачи"
        startdate = "Дата начала"
        respons = "Ответственный"

        # Устанавливаем заголовки столбцов
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels([number, city, building, device, havePC, lastdate, startdate, respons])
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout.addWidget(self.table_widget)

        screen_geometry = QApplication.desktop().screenGeometry()
        self.resize(int(screen_geometry.width() / 2.5), int(screen_geometry.height() / 5))
        self.move(screen_geometry.width() - self.width(), 0)

        self.conn_str = "DRIVER={SQL Server};SERVER=SERVER;DATABASE=DeadLineBase;UID=DeadLine;PWD=123"
        self.initial_check = False

        self.update_table()

    def update_table(self):
            self.table_widget.clearContents()

            conn = pyodbc.connect(self.conn_str)
            cursor = conn.cursor()
            query = "SELECT * FROM DeadLineTable WHERE Крайняя_дата > GETDATE() ORDER BY Крайняя_дата"

            cursor.execute(query)
            rows = cursor.fetchall()

            self.table_widget.setRowCount(len(rows))

            for index, line in enumerate(rows):
                for col, value in enumerate(line):
                    item = QTableWidgetItem(str(value))
                    if index == 0 and line[col] == line[0]:
                        item.setForeground(QColor('red'))
                    else:
                        item.setForeground(QColor('gray'))
                    self.table_widget.setItem(index, col, item)

            self.blink_first_row()

            header = self.table_widget.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

    def blink_first_row(self):
        row = 0
        color = QColor('red')

        for col in range(self.table_widget.columnCount()):
            item = self.table_widget.item(row, col)
            if item:
                item.setForeground(color)

        QTimer.singleShot(500, self.reset_blink)

    def reset_blink(self):
        row = 0
        color = QColor('gray')

        for col in range(self.table_widget.columnCount()):
            item = self.table_widget.item(row, col)
            if item:
                item.setForeground(color)

        QTimer.singleShot(500, self.blink_first_row)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparentWindow()
    window.show()
    sys.exit(app.exec_())

    