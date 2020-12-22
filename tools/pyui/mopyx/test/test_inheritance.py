from mopyx import model

import unittest


@model
class File:
    def __init__(self, name: str) -> None:
        self.name = name


@model
class Folder(File):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class TestIfModelInheritanceWorks(unittest.TestCase):
    """
    Instantiates some objects and checks instanceof.
    """

    def test_inheritance(self):
        """
        Just a basic check.
        """
        folder = Folder("/etc")

        self.assertTrue(isinstance(folder, Folder))
        self.assertTrue(isinstance(folder, File))


if __name__ == '__main__':
    unittest.main()
