from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from utility_functions import markdown_to_html_node

def main():
   
    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

    div = markdown_to_html_node(md)
    print(div.to_html())
main()