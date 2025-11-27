import unittest
from utility_functions import split_nodes_link, split_nodes_image
from textnode import TextNode, TextType

class TestLinkImageSplitters(unittest.TestCase):
    def test_link_split(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.PLAIN)
        res = split_nodes_link([node])
        self.assertEqual(len(res), 4)
        self.assertEqual(res[0].text_type, TextType.PLAIN)
        self.assertEqual(res[1].text_type, TextType.LINK)
        self.assertEqual(res[2].text_type, TextType.PLAIN)
        self.assertEqual(res[3].text_type, TextType.LINK)

    def test_link_split_multi(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.PLAIN)
        node2 = TextNode("Another link [click here!](https://www.example.com) of mine", TextType.PLAIN)
        res = split_nodes_link([node, node2])
        self.assertEqual(len(res), 7)
        self.assertEqual(res[0].text_type, TextType.PLAIN)
        self.assertEqual(res[1].text_type, TextType.LINK)
        self.assertEqual(res[2].text_type, TextType.PLAIN)
        self.assertEqual(res[3].text_type, TextType.LINK)
        self.assertEqual(res[4].text_type, TextType.PLAIN)
        self.assertEqual(res[5].text_type, TextType.LINK)
        self.assertEqual(res[5].text, "click here!")
        self.assertEqual(res[6].text_type, TextType.PLAIN)

    def test_link_split_no_links(self):
        node = TextNode("No link here!", TextType.PLAIN)
        res = split_nodes_link([node])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].text_type, TextType.PLAIN)
    
    def test_link_split_only_links(self):
        node = TextNode("[click here!](https://www.example.com)[or here!](https://www.example.com)", TextType.PLAIN)
        res = split_nodes_link([node])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].text_type, TextType.LINK)
        self.assertEqual(res[1].text_type, TextType.LINK)
    
    

    def test_image_split(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN)
        res = split_nodes_image([node])
        self.assertEqual(len(res), 4)
        self.assertEqual(res[0].text_type, TextType.PLAIN)
        self.assertEqual(res[1].text_type, TextType.IMAGE)
        self.assertEqual(res[2].text_type, TextType.PLAIN)
        self.assertEqual(res[3].text_type, TextType.IMAGE)

    def test_image_split_multi(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.PLAIN)
        node2 = TextNode("Another image ![third image](https://www.example.com) of mine", TextType.PLAIN)
        res = split_nodes_image([node, node2])
        self.assertEqual(len(res), 7)
        self.assertEqual(res[0].text_type, TextType.PLAIN)
        self.assertEqual(res[1].text_type, TextType.IMAGE)
        self.assertEqual(res[2].text_type, TextType.PLAIN)
        self.assertEqual(res[3].text_type, TextType.IMAGE)
        self.assertEqual(res[4].text_type, TextType.PLAIN)
        self.assertEqual(res[5].text_type, TextType.IMAGE)
        self.assertEqual(res[5].text, "third image")
        self.assertEqual(res[6].text_type, TextType.PLAIN)

    def test_image_split_no_images(self):
        node = TextNode("No images here!", TextType.PLAIN)
        res = split_nodes_image([node])
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].text_type, TextType.PLAIN)
    
    def test_image_split_only_images(self):
        node = TextNode("![first image](https://www.example.com)![second image](https://www.example.com)", TextType.PLAIN)
        res = split_nodes_image([node])
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0].text_type, TextType.IMAGE)
        self.assertEqual(res[0].text, "first image")
        self.assertEqual(res[1].text_type, TextType.IMAGE)
        self.assertEqual(res[1].text, "second image")

if __name__ == "__main__":
    unittest.main()