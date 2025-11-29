from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from utility_functions import markdown_to_html_node
from generate_pages import generate_pages_recursive
from copy_files import copy_files

def main():
   
    copy_files("static", "public")
    generate_pages_recursive("content", "template.html", "public")
    
main()