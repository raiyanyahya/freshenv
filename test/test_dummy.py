import unittest


class TestDummy(unittest.TestCase):
    def test_dummy(self):
        self.assertEquals("dummy test", "dummy test")


if __name__ == "__main__":
    unittest.main()
