from time import sleep

import requests
from PyQt6.QtCore import pyqtSignal, QThread

from src import values as v
from src.actions import remove_logs


class BaseThread(QThread):
    progress = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent


class ProgressThread(BaseThread):
    def run(self):
        delay = 0.034

        for i in range(16, 702):
            sleep(delay)
            self.progress.emit(i)

        remove_logs()

        while not v.data_loading_try:
            sleep(0.06)


class LoadingThread(BaseThread):
    def run(self):
        # TODO: Добавь сюда в будущем загрузку

        v.data_loading_try = True


class CheckNetworkThread(QThread):
    status_checked = pyqtSignal(bool)

    def run(self):
        try:
            if v.incognito:
                requests.get((
                                 "https://cloudflare.com",
                                 "https://www.google.com",
                                 "https://ya.ru"
                             )
                             [v.network_check], timeout=5)
            else:
                requests.get((
                                 "http://cp.cloudflare.com",
                                 "http://connectivitycheck.gstatic.com/generate_204",
                                 "http://www.msftconnecttest.com/connecttest.txt"
                             )[v.network_check],
                             timeout=5, allow_redirects=False)

            self.status_checked.emit(True)
        except requests.exceptions.RequestException:
            self.status_checked.emit(False)
