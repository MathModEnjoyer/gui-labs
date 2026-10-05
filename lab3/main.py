import sys
from pathlib import Path
from PyQt5 import QtSql, QtWidgets


class DatabaseWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа 3 — таблицы и SQL")
        self.resize(1050, 680)
        self.connection = None
        self.models = []
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        root = QtWidgets.QVBoxLayout(central)

        bar = QtWidgets.QHBoxLayout()
        set_btn = QtWidgets.QPushButton("Set connection")
        close_btn = QtWidgets.QPushButton("Close connection")
        query_btn = QtWidgets.QPushButton("SELECT name")
        score_btn = QtWidgets.QPushButton("Оценки по убыванию")
        group_btn = QtWidgets.QPushButton("Группы и средний балл")
        for button in (set_btn, close_btn, query_btn, score_btn, group_btn):
            bar.addWidget(button)
        root.addLayout(bar)
        self.tabs = QtWidgets.QTabWidget()
        root.addWidget(self.tabs)
        self.status = QtWidgets.QLabel("Соединение не установлено")
        root.addWidget(self.status)
        set_btn.clicked.connect(self.open_database)
        close_btn.clicked.connect(self.close_database)
        query_btn.clicked.connect(lambda: self.run_query("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name", "Имена таблиц"))
        score_btn.clicked.connect(lambda: self.run_query("SELECT name, group_name, printf('%.2f', score) AS score FROM students ORDER BY score DESC", "Рейтинг"))
        group_btn.clicked.connect(lambda: self.run_query("SELECT group_name, ROUND(AVG(score), 2) AS average_score FROM students GROUP BY group_name", "Средний балл по группам"))

    def open_database(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Выберите SQLite-базу", str(Path(__file__).parent), "SQLite (*.sqlite *.db);;Все файлы (*)")
        if not path:
            return
        self.close_database()
        self.connection = QtSql.QSqlDatabase.addDatabase("QSQLITE", "lab3_connection")
        self.connection.setDatabaseName(path)
        if not self.connection.open():
            self.status.setText(f"Ошибка подключения: {self.connection.lastError().text()}")
            return
        self.status.setText(f"Подключено: {path}")
        self.tabs.clear()
        self.run_query("SELECT * FROM sqlite_master", "Tab 1 — sqlite_master")

    def run_query(self, sql, title):
        if not self.connection or not self.connection.isOpen():
            self.status.setText("Сначала установите соединение с базой данных")
            return
        model = QtSql.QSqlQueryModel(self)
        model.setQuery(sql, self.connection)
        if model.lastError().isValid():
            self.status.setText(f"Ошибка SQL: {model.lastError().text()}")
            return
        view = QtWidgets.QTableView()
        view.setModel(model)
        view.setSortingEnabled(True)
        view.resizeColumnsToContents()
        self.tabs.addTab(view, title)
        self.models.append(model)

    def close_database(self):
        self.tabs.clear()
        self.models.clear()
        if self.connection:
            name = self.connection.connectionName()
            self.connection.close()
            QtSql.QSqlDatabase.removeDatabase(name)
            self.connection = None
        self.status.setText("Соединение закрыто")

    def closeEvent(self, event):
        self.close_database()
        event.accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DatabaseWindow()
    window.show()
    sys.exit(app.exec_())

