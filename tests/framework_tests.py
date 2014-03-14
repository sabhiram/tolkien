import unittest as ULT
import sys, os
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import tolkien

"""
    Base tests for framework
"""
class TestTolkienFramework(ULT.TestCase):
    
    def setUp(self):
        # nothing to do
        return

    def tearDown(self):
        # nothing to do
        return

    def test_test(self):
        self.assertEqual(0, 0)


"""
    Mock plugin for the filter test (only relevant arg is the name)
"""
class MockPlugin:
    def __init__(self, n):
        self.name = n


"""
    Test the filtering of plugins
"""
class TestPluginFilter(ULT.TestCase):
    def setUp(self):
        self.plugins = []
        self.plugins.append(MockPlugin("foo"))
        self.plugins.append(MockPlugin("bar"))
        self.plugins.append(MockPlugin("baz"))
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