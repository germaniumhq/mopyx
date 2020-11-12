import pickle
import unittest
import copy
import yaml

from yamldict.YamlDictClass import YamlDict
from yamldict.YamlNavigator import YamlNavigator


class YamlDictTest(unittest.TestCase):
    def test_simple_property_read(self):
        p = YamlDict(content={"x": 3})

        self.assertEqual(3, p.x)

    def test_nested_property_read(self):
        p = YamlDict(content={"x": 3, "y": {"key": 1, "list": [1, 2, 3]}})

        self.assertEqual(1, p.y.key)
        self.assertEqual([1, 2, 3], p.y.list._raw)

    def test_read_via_get(self):
        p = YamlDict(content={"items": [1, 2, 3]})

        self.assertEqual([1, 2, 3], p["items"]._raw)

    def test_write_with_property(self):
        p = YamlDict(content={"x": "original"})

        p.x = "new"

        self.assertEqual("new", p.x)
        self.assertEqual("new", p["x"])

    def test_write_with_set(self):
        p = YamlDict(content={"x": "original"})

        p["x"] = "new"

        self.assertEqual("new", p.x)
        self.assertEqual("new", p["x"])

    def test_iteration_as_iterable(self):
        p = YamlDict(
            content={
                "x": "original",
                "y": "original",
                "z": "original",
            }
        )
        items = set()

        for item in p:
            items.add(item)

        self.assertSetEqual({"x", "y", "z"}, items)

    def test_iteration_key_value(self):
        p = YamlDict(
            content={
                "x": "x",
                "y": "y",
                "z": "z",
            }
        )

        items = dict()

        for k, v in p._items():
            items[k] = v

        self.assertDictEqual(
            {
                "x": "x",
                "y": "y",
                "z": "z",
            },
            items,
        )

    def test_set_nested_property_navigator(self):
        """
        The `__content` should always be kept as objects pointing to each other,
        not property navigators.
        :return:
        """
        p = YamlDict()
        x = YamlDict()

        p.x = x
        p.x.y1 = "y1"
        x.y2 = "y2"
        p.y = "y"

        self.assertEqual({"x": {"y1": "y1", "y2": "y2"}, "y": "y"}, p._raw)

    def test_deep_copy_really_deep_copies(self):
        dict = {"x": 1}
        p = YamlDict(content=dict)

        p_copy = copy.deepcopy(p)
        p_copy.x = 2

        self.assertEqual(2, p_copy.x)
        self.assertEqual(1, dict["x"])
        self.assertEqual(1, p.x)

    def test_len(self):
        d = YamlDict(content={"x": 1, "y": 2, "z": 3})
        self.assertEqual(3, len(d))

    def test_removal_attribute(self):
        d = YamlDict(content={"x": 1, "y": 2, "z": 3})
        del d.x

        self.assertEqual({"y": 2, "z": 3}, d._raw)

    def test_removal_item(self):
        d = YamlDict(content={"x": 1, "y": 2, "z": 3})
        del d["x"]

        self.assertEqual({"y": 2, "z": 3}, d._raw)

    def test_none_navigation(self):
        d = YamlDict(content={"x": 1, "y": 2, "z": 3})

        self.assertTrue(not d.a)
        self.assertTrue(not d.a.b)

        self.assertTrue("a" not in d)
        self.assertTrue("b" not in d.a)

    def test_repr_dict(self):
        d = YamlDict(property_name="a.b", content={"x": 1})

        representation = f"{d}"

        self.assertEqual("YamlDict(a.b) {'x': 1}", representation)

    def test_repr_missing(self):
        d = YamlDict(property_name="a.b", content={"c": 1})

        representation = f"{d.x}"

        self.assertEqual("YamlMissing(a.b.x)", representation)

    def test_repr_missing_nested(self):
        d = YamlDict(property_name="a.b", content={"c": 1})

        representation = f"{d.x.y}"

        self.assertEqual("YamlMissing(a.b.x.y)", representation)

    def test_items_iteration_gives_yaml(self):
        d = YamlDict(
            content={
                "a": {"x": 1},
            }
        )

        for k, v in d._items():
            self.assertEqual("a", k)
            self.assertTrue(
                isinstance(v, YamlDict),
                "The iterated property over items is not an YamlDict",
            )
            self.assertEqual("YamlDict(.a) {'x': 1}", f"{v}")
            self.assertEqual(1, d.a.x)
            self.assertFalse(d.a.y)

    def test_set_other_yaml_navigator(self):
        a = YamlDict()
        b = YamlDict()

        a.b = b

        self.assertFalse(isinstance(a._raw["b"], YamlNavigator))

    def test_yaml_gets_serialized(self):
        a = YamlDict(content={"x": 3})

        data = yaml.safe_dump(a)
        print(data)

    def test_yaml_gets_pickle_serialized(self):
        a = YamlDict(content={"x": 3})

        pickle.dumps(a)


if __name__ == "__main__":
    unittest.main()
