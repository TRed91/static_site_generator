import unittest
from utility_functions import extract_markdown_images, extract_markdown_links

class TestExtractors(unittest.TestCase):
    def test_extract_image(self):
        res = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0][0], "image")
        self.assertEqual(res[0][1], "https://i.imgur.com/zjjcJKZ.png")

    def test_extract_links(self):
        res = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    )
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0][0], "to boot dev")
        self.assertEqual(res[0][1], "https://www.boot.dev")
        self.assertEqual(res[1][0], "to youtube")
        self.assertEqual(res[1][1], "https://www.youtube.com/@bootdotdev")


if __name__ == "__main__":
    unittest.main()