import sys
from PyQt5.QtCore import QSignalBlocker, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QDoubleSpinBox, QFormLayout, QLabel, QMainWindow,
    QVBoxLayout, QWidget,
)


class Converter(QMainWindow):
    value_changed = pyqtSignal(str, float)

    RATES_TO_RUB = {"RUB": 1.0, "USD": 92.5, "EUR": 100.5}

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа 2 — сигналы и слоты")
        self.resize(440, 280)
        self.updating = False
        self.fields = {}

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        title = QLabel("Конвертер валют")
        title.setStyleSheet("font-size: 22px; font-weight: 600;")
        layout.addWidget(title)
        layout.addWidget(QLabel("Измените любое поле — остальные значения обновятся сигналами и слотами."))

        form = QFormLayout()
        for code, label in (("RUB", "Рубли"), ("USD", "Доллары"), ("EUR", "Евро")):
            field = QDoubleSpinBox()
            field.setRange(0, 1_000_000_000)
            field.setDecimals(2)
            field.setSingleStep(100)
            field.valueChanged.connect(lambda value, c=code: self.source_changed(c, value))
            self.fields[code] = field
            form.addRow(f"{label} ({code})", field)
        layout.addLayout(form)
        self.status = QLabel("Курс: 1 USD = 92.50 RUB; 1 EUR = 100.50 RUB")
        self.status.setStyleSheet("color: #53657a;")
        layout.addWidget(self.status)
        self.fields["RUB"].setValue(1000)

    def source_changed(self, source, value):
        if self.updating:
            return
        self.updating = True
        try:
            rubles = value * self.RATES_TO_RUB[source]
            for code, field in self.fields.items():
                if code == source:
                    continue
                with QSignalBlocker(field):
                    field.setValue(rubles / self.RATES_TO_RUB[code])
            self.value_changed.emit(source, value)
        finally:
            self.updating = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Converter()
    window.show()
    sys.exit(app.exec_())
