from utility_functions import split_nodes_delimeter
from textnode import TextNode, TextType
import unittest

class TestSplitNodesDelimeter(unittest.TestCase):
    def test_splits_bold(self):
        text_node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        res = split_nodes_delimeter([text_node], "`", TextType.CODE)
        
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].text_type, TextType.PLAIN)
        self.assertEqual(res[1].text_type, TextType.CODE)
        self.assertEqual(res[1].text, "code block")

    def test_splits_italic_multiple(self):
        text_node = TextNode("This is text _with_ some _italic_ words", TextType.PLAIN)
        res = split_nodes_delimeter([text_node], "_", TextType.ITALIC)
        
        self.assertEqual(len(res), 5)
        self.assertEqual(res[1].text_type, TextType.ITALIC)
        self.assertEqual(res[3].text, "italic")
        self.assertEqual(res[3].text_type, TextType.ITALIC)

    def test_splits_beginning(self):
        text_node = TextNode("**Some bold text** this is", TextType.PLAIN)
        res = split_nodes_delimeter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].text, "Some bold text")
        self.assertEqual(res[0].text_type, TextType.BOLD)

    def test_splits_beginning_and_end(self):
        text_node = TextNode("**Some bold text** this is **also bold**", TextType.PLAIN)
        res = split_nodes_delimeter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0].text, "Some bold text")
        self.assertEqual(res[0].text_type, TextType.BOLD)
        self.assertEqual(res[1].text_type, TextType.PLAIN)
        self.assertEqual(res[2].text_type, TextType.BOLD)

    def test_raises_missing_closing_delimeter(self):
        text_node = TextNode("Missing **a delimeter", TextType.PLAIN)

        with self.assertRaises(Exception):
            split_nodes_delimeter([text_node], "**", TextType.BOLD)

    def test_no_delimeter(self):
        text_node = TextNode("Missing a delimeter", TextType.PLAIN)
        
        res = split_nodes_delimeter([text_node], "**", TextType.BOLD)

        self.assertEqual(len(res), 1)

    def test_pass_multiple_nodes(self):
        text_node = TextNode("**Some bold text** this is **also bold**", TextType.PLAIN)
        text_node2 = TextNode("Some more **bold** text", TextType.PLAIN)
        res = split_nodes_delimeter([text_node, text_node2], "**", TextType.BOLD)

        self.assertEqual(len(res), 6)
        self.assertEqual(res[2].text, "also bold")
        self.assertEqual(res[2].text_type, TextType.BOLD)
        self.assertEqual(res[4].text, "bold")
        self.assertEqual(res[4].text_type, TextType.BOLD)

if __name__ == "__main__":
    unittest.main()