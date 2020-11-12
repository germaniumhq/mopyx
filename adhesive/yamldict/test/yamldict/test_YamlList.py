import pickle
import unittest
import copy

from yamldict.YamlDictClass import YamlDict
from yamldict.YamlListClass import YamlList
from yamldict.YamlNavigator import YamlNavigator


class YamlListTest(unittest.TestCase):
    def test_simple_property_read(self):
        p = YamlList(content=[{"x": 3}])

        self.assertEqual(3, p[0].x)

    def test_nested_property_read(self):
        p = YamlDict(
            content={
                "x": 3,
                "y": {"key": 1, "list": [1, {"more": [1, {"nested": ["nested"]}]}, 3]},
            }
        )

        self.assertEqual(1, p.y.key)
        self.assertEqual(["nested"], p.y.list[1].more[1].nested._raw)

    def test_read_via_get(self):
        p = YamlList(content=[[1, 2, 3]])

        self.assertEqual([1, 2, 3], p[0]._raw)

    def test_write_with_set(self):
        p = YamlList(content=["original"])

        p[0] = "new"

        self.assertEqual("new", p[0])

    def test_iteration_as_iterable(self):
        p = YamlList(content=["x", "y", "z"])
        items = set()

        for item in p:
            items.add(item)

        self.assertSetEqual({"x", "y", "z"}, items)

    def test_deep_copy_really_deep_copies(self):
        items = [1, 2, 3]
        p = YamlList(content=items)

        p_copy = copy.deepcopy(p)
        p_copy[0] = 0

        self.assertEqual(0, p_copy[0])
        self.assertEqual(1, items[0])
        self.assertEqual(1, p[0])

    def test_len_works(self):
        items = [1, 2, 3]
        p = YamlList(content=items)

        self.assertEqual(3, len(p))

    def test_is_empty(self):
        items = [1, 2, 3]

        p = YamlList(content=items)
        self.assertTrue(p)

        p = YamlList()
        self.assertFalse(p)

        p = YamlList(content=[])
        self.assertFalse(p)

    def test_removal(self):
        p = YamlList(content=[1, 2, 3])
        del p[0]

        self.assertEqual([2, 3], p._raw)

    def test_repr(self):
        p = YamlList(property_name="a.b", content=[1, 2, 3])

        representation = f"{p}"

        self.assertEqual("YamlList(a.b) [1, 2, 3]", representation)

    def test_nested_repr(self):
        p = YamlDict(property_name="a.b", content={"x": [{"y": [1, 2, 3]}]})

        representation = f"{p.x[0].y}"
        self.assertEqual("YamlList(a.b.x.0.y) [1, 2, 3]", representation)

        representation = f"{p.x[0].z}"
        self.assertEqual("YamlMissing(a.b.x.0.z)", representation)

    def test_iteration_gives_yaml(self):
        items = YamlList(content=[{"x": 1}])

        for item in items:
            self.assertTrue(
                isinstance(item, YamlNavigator),
                "The iterated instance should be a navigator.",
            )

    def test_set_other_yaml_navigator(self):
        a = YamlList(property_name="a", content=["a"])
        b = YamlDict()

        a[0] = b

        self.assertFalse(isinstance(a._raw[0], YamlNavigator))

    def test_yaml_gets_pickle_serialized(self):
        a = YamlList(property_name="a", content=["a"])

        pickle.dumps(a)


if __name__ == "__main__":
    unittest.main()
