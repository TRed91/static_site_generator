import unittest
from utility_functions import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Hello Text"
        res = extract_title(md)

        self.assertEqual(res, "Hello Text")

    def test_extract_title_multiline(self):
        md = """
This is the first test
## This heading should be skipped

# Correct heading

some other stuff
"""
        res = extract_title(md)

        self.assertEqual(res, "Correct heading")

    def test_extract_faile_raises_ex(self):
        md = "## Oops, no h1 heading"
        md2 = "#OOps, also wrong"

        with self.assertRaises(Exception):
            res = extract_title(md)

        with self.assertRaises(Exception):
            res = extract_title(md2)

if __name__ == "__main__":
    unittest.main()