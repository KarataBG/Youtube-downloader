import sys
import threading
from functools import cached_property

from PyQt5 import QtCore, QtWidgets
from pytube import YouTube


class QPyTube(QtCore.QObject):
    initialized = QtCore.pyqtSignal(bool, str)
    download_started = QtCore.pyqtSignal()
    download_progress_changed = QtCore.pyqtSignal(int)
    download_finished = QtCore.pyqtSignal()

    def __init__(self, url):
        super().__init__()
        self._url = url
        self._yt = None
        self._mutex = threading.Lock()

        threading.Thread(target=self._init, daemon=True).start()

    @property
    def url(self):
        return self._url

    @cached_property
    def resolutions(self):
        return list()

    def _init(self):
        with self._mutex:
            self.resolutions.clear()
        try:
            self._yt = YouTube(
                self.url,
                on_progress_callback=self._on_progress,
                on_complete_callback=self._on_complete,
            )
            streams = self._yt.streams.filter(mime_type="video/mp4", progressive=True)
        except Exception as e:
            self.initialized.emit(False, str(e))
            return
        with self._mutex:
            self.resolutions = [stream.resolution for stream in streams]
        self.initialized.emit(True, "")

    def download(self, resolution, directory):
        threading.Thread(
            target=self._download, args=(resolution, directory), daemon=True
        ).start()
        # self._download(resolution,directory)

    def _download(self, resolution, directory):
        stream = self._yt.streams.get_by_resolution(resolution)
        self.download_started.emit()
        stream.download(directory)

    def _on_progress(self, stream, chunk, bytes_remaining):
        self.download_progress_changed.emit(
            100 * (stream.filesize - bytes_remaining) // stream.filesize
        )

    def _on_complete(self, stream, filepath):
        self.download_finished.emit()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.le_url = QtWidgets.QLineEdit("http://youtube.com/watch?v=2lAe1cqCOXo")
        self.lbl_error = QtWidgets.QLabel()
        self.btn_search = QtWidgets.QPushButton("Search")
        self.cmb_resolutions = QtWidgets.QComboBox()
        self.le_directory = QtWidgets.QLineEdit("")
        self.btn_download = QtWidgets.QPushButton("Download")
        self.pgb_download = QtWidgets.QProgressBar()

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        lay = QtWidgets.QGridLayout(central_widget)
        lay.addWidget(self.le_url, 0, 0)
        lay.addWidget(self.btn_search, 0, 1)
        lay.addWidget(self.cmb_resolutions, 1, 0)
        lay.addWidget(self.le_directory, 1, 1)
        lay.addWidget(self.btn_download, 1, 2)
        lay.addWidget(self.pgb_download, 2, 0, 1, 3)

        self.btn_download.setEnabled(False)

        self._qpytube = None

        self.btn_search.clicked.connect(self.handle_search_clicked)
        self.btn_download.clicked.connect(self.handle_download_clicked)

    def handle_search_clicked(self):
        self.cmb_resolutions.clear()
        self.btn_search.setEnabled(False)
        self.btn_download.setEnabled(False)
        self.lbl_error.clear()
        self._qpytube = QPyTube(self.le_url.text())
        self._qpytube.initialized.connect(self.handle_initialized)
        self._qpytube.download_progress_changed.connect(self.pgb_download.setValue)
        self._qpytube.download_started.connect(self.handle_download_started)
        self._qpytube.download_finished.connect(self.handle_download_finished)

    @QtCore.pyqtSlot(bool, str)
    def handle_initialized(self, status, error=""):
        if status:
            self.cmb_resolutions.addItems(self._qpytube.resolutions)
            self.btn_download.setEnabled(True)
        else:
            self.lbl_error.setText(error)
        self.btn_search.setEnabled(True)

    def handle_download_clicked(self):
        self._qpytube.download(
            self.cmb_resolutions.currentText(), self.le_directory.text()
        )
        self.btn_search.setEnabled(False)
        self.btn_download.setEnabled(False)
        self.le_directory.setEnabled(False)

    def handle_download_started(self):
        self.lbl_error.clear()
        print("started")

    def handle_download_finished(self):
        self.pgb_download.setValue(100)
        self.btn_search.setEnabled(True)
        self.btn_download.setEnabled(True)
        self.le_directory.setEnabled(True)
        print("finished")


def main(args):
    app = QtWidgets.QApplication(args)

    w = MainWindow()
    w.show()

    app.exec_()


if __name__ == "__main__":
    main(sys.argv)
