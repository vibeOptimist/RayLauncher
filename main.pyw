""" (c) 2026 RayLauncher. All rights reserved. """

import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from src.app import MyApplication, MainWindow


def main():
    # Адаптация под высокое разрешение
    high_dpi_scale = Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    QGuiApplication.setHighDpiScaleFactorRoundingPolicy(high_dpi_scale)

    # Приложение
    app = MyApplication(sys.argv)
    window = MainWindow()
    app.main_window = window
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
