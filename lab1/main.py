from pathlib import Path
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QHBoxLayout, QLabel, QMainWindow, QPushButton, QVBoxLayout,
    QWidget,
)


class Lab1Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лабораторная работа 1 — кнопки и изображение")
        self.resize(720, 480)

        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("QLabel { color: #1c2733; } QPushButton { color: #1c2733; background: #ffffff; border: 1px solid #aab7c4; border-radius: 6px; padding: 8px 14px; } QPushButton:hover { background: #e8f2ff; }")
        layout = QVBoxLayout(central)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(18)

        self.caption = QLabel("Надпись")
        self.caption.setAlignment(Qt.AlignCenter)
        self.caption.setStyleSheet("font-size: 22px; font-weight: 600;")
        layout.addWidget(self.caption)

        self.image = QLabel()
        self.image.setAlignment(Qt.AlignCenter)
        self.image.setMinimumHeight(230)
        self.image.setStyleSheet("background: #f3f6fb; border: 1px solid #c9d4e3; border-radius: 12px;")
        self.image.hide()
        layout.addWidget(self.image, 1)

        buttons = QHBoxLayout()
        self.button_text = QPushButton("Кнопка 1")
        self.button_image = QPushButton("Кнопка 2 — показать PNG")
        self.button_text.clicked.connect(self.change_caption)
        self.button_image.clicked.connect(self.show_png)
        buttons.addWidget(self.button_text)
        buttons.addWidget(self.button_image)
        layout.addLayout(buttons)

    def change_caption(self):
        self.caption.setText("Надпись изменена после нажатия кнопки")

    def show_png(self):
        base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
        path = base_dir / "assets" / "hello.png"
        pixmap = QPixmap(str(path))
        if pixmap.isNull():
            self.caption.setText("Не удалось загрузить изображение")
            return
        self.image.setPixmap(pixmap.scaled(
            self.image.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        self.image.show()
        self.caption.setText("Изображение загружено из PNG")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Lab1Window()
    window.show()
    sys.exit(app.exec_())



