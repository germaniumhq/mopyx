from robotlibcore import HybridCore

from GermaniumLibrary import GermaniumLocators


class GermaniumLibrary(HybridCore):
    def __init__(self):
        super(GermaniumLibrary, self).__init__(library_components=[GermaniumLocators()])

    @staticmethod
    def noop():
        """
        Method to keep the optimizing imports from removing the
        class.
        :return:
        """
        pass
