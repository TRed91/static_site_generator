import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_converts_props_to_html(self):
        node = HTMLNode("a", "some value", props={"href": "http://example.com"})

        self.assertEqual(node.props_to_html(), ' href="http://example.com"')

    def test_converts_multiple_props_to_html(self):
        node = HTMLNode("a", "some value", props={
            "href": "http://example.com", 
            "target": "_blank"
            })

        self.assertEqual(node.props_to_html(), ' href="http://example.com" target="_blank"')
    
    def test_converts_props_to_html_empty(self):
        node = HTMLNode("div", "some value", props={})
        self.assertEqual(node.props_to_html(), "")
    
    def test_converts_props_to_html_missing(self):
        node = HTMLNode("div", "some value")
        self.assertEqual(node.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()