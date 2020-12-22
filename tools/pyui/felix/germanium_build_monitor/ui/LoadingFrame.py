from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QMovie

from germanium_build_monitor.ui.generated.Ui_LoadingFrame import Ui_Form
from germanium_build_monitor.resources import icons


class LoadingFrame(QWidget, Ui_Form):
    def __init__(self) -> None:
        super().__init__()

        self.setupUi(self)

        movie = QMovie(icons.get_icon_path("loader.gif"))
        self.load_image_label.setMovie(movie)

        movie.start()

