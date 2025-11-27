import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq__different_text(self):
        node = TextNode("Some text", TextType.PLAIN)
        node2 = TextNode("This other text", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_eq__different_texttype(self):
        node = TextNode("Same text", TextType.PLAIN)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq__different_url(self):
        node = TextNode("Same text", TextType.PLAIN)
        node2 = TextNode("Same text", TextType.PLAIN, "http://example.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()