import unittest
from textnode import TextNode, TextType
from utility_functions import text_node_to_html_node
from leafnode import LeafNode

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")
    
    def test_code(self):
        node = TextNode("Code snippet", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")
        self.assertEqual(html_node.to_html(), "<code>Code snippet</code>")

    def test_link(self):
        node = TextNode("Example", TextType.LINK, "http://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Example")
        self.assertEqual(html_node.props, {"href": "http://example.com"})
        self.assertEqual(html_node.to_html(), '<a href="http://example.com">Example</a>')

    def test_image(self):
        node = TextNode("An image", TextType.IMAGE, "http://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "http://example.com/image.png", "alt": "An image"})
        self.assertEqual(html_node.to_html(), '<img src="http://example.com/image.png" alt="An image"></img>')

    def test_unsupported_texttype(self):
        class FakeTextType:
            pass

        node = TextNode("Unsupported", FakeTextType())
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertIn("Unsupported TextType", str(context.exception))

if __name__ == "__main__":
    unittest.main()
    