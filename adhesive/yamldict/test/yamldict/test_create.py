import unittest
import yamldict
import yaml


class TestCreateFunction(unittest.TestCase):
    """
    Tests the `create` function.
    """

    def test_create_dict(self):
        """
        Tests if creation of YAML works using
        yamldict.create() to get a dictionary.
        """
        data = yamldict.create(
            """
          x: 3
          y: 4
        """
        )

        self.assertEqual(3, data.x)
        self.assertEqual(4, data.y)

    def test_create_list(self):
        """
        Tests if creation of lists works
        using yamldict.create().
        """
        data = yamldict.create(
            """
        - "item 1"
        - "item 2"
        """
        )

        self.assertEqual(2, len(data))
        self.assertEqual("item 1", data[0])
        self.assertEqual("item 2", data[1])

    def test_create_serialization(self):
        """
        Test if serializing data is working.
        """
        data = yamldict.create(
            """
            x: 3
            y: 3
        """
        )

        data_string = yaml.safe_dump(data)
        self.assertTrue("x: 3" in data_string)
        self.assertTrue("y: 3" in data_string)


if __name__ == "__main__":
    unittest.main()
