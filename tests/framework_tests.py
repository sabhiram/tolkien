import unittest as ULT
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import tolkien

class TestTolkienFramework(ULT.TestCase):
    
    def setUp(self):
        # nothing to do
        return

    def tearDown(self):
        # nothing to do
        return

    def test_test(self):
        self.assertEqual(0, 0)

# Mock plugin for the filter test
class MockPlugin:
    def __init__(self, n, d, g):
        self.name = n
        self.project_dir_name = d
        self.git_repo = g

class TestPluginFilter(ULT.TestCase):
    def setUp(self):
        self.plugins = []
        self.plugins.append(MockPlugin("foo", "foo", "foo"))
        self.plugins.append(MockPlugin("bar", "bar", "bar"))
        self.plugins.append(MockPlugin("baz", "baz", "baz"))
        return

    def tearDown(self):
        # nothing to do
        return

    def test_filter_single(self):
        result = list(tolkien.filter_plugins(self.plugins, ["FOO"]))
        self.assertEqual(len(result), 1)

    def test_filter_multiple(self):
        result = list(tolkien.filter_plugins(self.plugins, ["fOo", "BaR"]))
        self.assertEqual(len(result), 2)
        



if __name__ == "__main__":
    ULT.main()
# END OF FILE