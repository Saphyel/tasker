import sys

from PySide6.QtWidgets import (
    QMainWindow,
    QApplication,
    QTableWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QTableWidgetItem,
    QHeaderView,
)

from src.widgets.add_task_dialog import AddTaskDialog

task_list_db = [
    ("random1", "2022-11-24 12:30:00", "Football", "Watch something"),
    ("random2", "2022-11-24 13:30:00", "Videogames", "Watch some gamers"),
    ("random3", "2022-11-25 12:30:00", "Python", "Python 4 release!"),
    ("random4", "2022-11-26 12:30:00", "Shop", "Buy chocolate"),
    ("random5", "2022-11-26 13:30:00", "Secret", "reveal the fire"),
]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My App")

        self.table = QTableWidget(len(task_list_db), len(task_list_db[0]))

        self.table.setHorizontalHeaderLabels(["ID", "Date", "Tag", "Description"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        for row, item in enumerate(task_list_db):
            for column, cell in enumerate(item):
                self.table.setItem(row, column, QTableWidgetItem(cell))

        self.button_add = QPushButton("Add")
        self.button_add.clicked.connect(self.add_action)

        self.button_remove = QPushButton("Remove")
        self.button_remove.clicked.connect(self.remove_action)

        options = QHBoxLayout()
        options.addWidget(self.button_add)
        options.addWidget(self.button_remove)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(options)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.resize(widget.size())

    def add_action(self, s):
        dlg = AddTaskDialog()
        if dlg.exec():
            for index, item in enumerate(dlg.form):
                self.table.setItem(self.table.rowCount(), index, QTableWidgetItem(item))

    def remove_action(self, s):
        self.table.removeRow(self.table.currentRow())


app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
