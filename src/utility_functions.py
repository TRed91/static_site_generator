from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
import re

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url if text_node.url else ""})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url if text_node.url else "", "alt": text_node.text})
        case _:
            raise Exception(f"Unsupported TextType: {text_node.text_type}")
        
def text_to_text_nodes(text : str) -> list[TextNode]:
    node = TextNode(text, TextType.PLAIN)
    bolds = split_nodes_delimeter([node], "**", TextType.BOLD)
    italics = split_nodes_delimeter(bolds, "_", TextType.ITALIC)
    codes = split_nodes_delimeter(italics, "`", TextType.CODE)
    images = split_nodes_image(codes)
    links = split_nodes_link(images)
    return links

def split_nodes_delimeter(old_nodes : list[TextNode], delimeter : str, text_type : TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            segments = node.text.split(delimeter)
            if len(segments) % 2 == 0:
                raise Exception(f"Missing delimeter in text: {node.text}")
            
            for i in range(len(segments)):
                if segments[i] == "":
                    continue

                if i == 0 or i % 2 == 0:
                    new_nodes.append(TextNode(segments[i], TextType.PLAIN))
                else:
                    new_nodes.append(TextNode(segments[i], text_type))
    
    return new_nodes

def split_nodes_image(old_nodes : list[TextNode]):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            split_images_rec(node.text, new_nodes)

    return new_nodes

def split_images_rec(segment : str, new_nodes : list) -> None:
    if segment == "":
        return
    
    images = extract_markdown_images(segment)
    if len(images) == 0:
        text_node = TextNode(segment, TextType.PLAIN)
        if text_node not in new_nodes:
            new_nodes.append(text_node)
    else:
        for image in images:
            image_node = TextNode(image[0], TextType.IMAGE, image[1])
            segments = segment.split(f"![{image[0]}]({image[1]})", 1)
            if segments[0] == "" and image_node not in new_nodes:
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            for s in segments:
                split_images_rec(s, new_nodes)
                if image_node not in new_nodes:
                    new_nodes.append(image_node)


def split_nodes_link(old_nodes : list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
        else:
            split_links_rec(node.text, new_nodes)

    return new_nodes

def split_links_rec(segment : str, new_nodes : list) -> None:
    if segment == "":
        return
    
    links = extract_markdown_links(segment)
    if len(links) == 0:
        text_node = TextNode(segment, TextType.PLAIN)
        if text_node not in new_nodes:
            new_nodes.append(text_node)
    else:
        for link in links:
            link_node = TextNode(link[0], TextType.LINK, link[1])
            segments = segment.split(f"[{link[0]}]({link[1]})", 1)
            if segments[0] == "" and link_node not in new_nodes:
                new_nodes.append(link_node)
            for s in segments:
                split_links_rec(s, new_nodes)
                if link_node not in new_nodes:
                    new_nodes.append(link_node)

def extract_markdown_images(text : str) -> list[tuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text : str) -> list[tuple]:
    return re. findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)