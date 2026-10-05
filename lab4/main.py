import base64
import sys
from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine


class Interface(QObject):
    saved = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        base_dir = Path(sys.executable).resolve().parent if getattr(sys, "frozen", False) else Path(__file__).resolve().parent
        self.output_dir = base_dir / "saved_drawings"
        self.output_dir.mkdir(exist_ok=True)

    @pyqtSlot(str)
    def save_canvas(self, data_url):
        """Save the QML Canvas data URL as a timestamped PNG file."""
        try:
            encoded = data_url.split(",", 1)[1] if "," in data_url else data_url
            image = QImage.fromData(base64.b64decode(encoded))
            if image.isNull():
                self.saved.emit("Ошибка: Canvas не содержит изображения")
                return
            filename = self.output_dir / f"drawing_{datetime.now():%Y%m%d_%H%M%S}.png"
            image.save(str(filename), "PNG")
            self.saved.emit(f"Сохранено: {filename.name}")
        except (ValueError, TypeError, base64.binascii.Error) as error:
            self.saved.emit(f"Ошибка сохранения: {error}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = Interface()
    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("backend", interface)
    base_dir = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    engine.load(QUrl.fromLocalFile(str(base_dir / "mainWindow.qml")))
    if not engine.rootObjects():
        sys.exit("Не удалось загрузить QML")
    sys.exit(app.exec_())
