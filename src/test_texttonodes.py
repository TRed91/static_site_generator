import unittest
from textnode import TextNode, TextType
from utility_functions import text_to_text_nodes

class TestTextToNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        res = text_to_text_nodes(text)

        self.assertEqual(len(res), 10)
        self.assertEqual(res[0].text_type, TextType.PLAIN)
        self.assertEqual(res[1].text_type, TextType.BOLD)
        self.assertEqual(res[3].text_type, TextType.ITALIC)
        self.assertEqual(res[5].text_type, TextType.CODE)
        self.assertEqual(res[7].text_type, TextType.IMAGE)
        self.assertEqual(res[9].text_type, TextType.LINK)

if __name__ == "__main__":
    unittest.main()