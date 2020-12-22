from PySide2.QtCore import QSize


class QPixmap:
    def __init__(self,
                 icon_path: str) -> None:
        pass


class QIcon:
    Normal: int
    Off: int

    def addPixmap(self,
                  pixmap: QPixmap,
                  flag1: int,
                  flag2: int) -> None:
        pass

    def pixmap(self, size: QSize) -> QPixmap:
        pass


class QTextCharFormat:
    pass


class QSyntaxHighlighter:
    pass


class QFont:
    pass


class QMovie:
    def __init__(self,
                 movie_path: str) -> None:
        pass

    def start(self) -> None:
        pass
