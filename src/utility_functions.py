from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from blocktype import BlockType, block_to_block_type
import re

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
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

def markdown_to_blocks(markdown : str) -> list[str]:
    blocks = markdown.split("\n\n")
    
    for i in range(len(blocks)):
        blocks[i] = blocks[i].strip()

    blocks = list(filter(lambda b: b != "", blocks))  
    return blocks

def markdown_to_html_node(markdown : str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    parent_nodes = []
    
    for block in blocks:
        node = get_parent_node_from_block(block)
        parent_nodes.append(node)
    
    return ParentNode("div", parent_nodes)

def get_parent_node_from_block(block : str) -> ParentNode:
    block_type = block_to_block_type(block)

    match block_type:
        case BlockType.HEADING:
            heading_level = __get_heading_level(block)
            sanitized = __sanitize_heading(block, heading_level)
            children = text_to_children(sanitized)
            return ParentNode(heading_level, children)
        case BlockType.CODE:
            sanitized = block[3:-3]
            if sanitized[0] == "\n":
                sanitized = sanitized[1:]
            text_node = TextNode(sanitized, TextType.PLAIN)

            code_node = ParentNode("code", [text_node_to_html_node(text_node)])
            return ParentNode("pre", [code_node])
        case BlockType.QUOTE:
            sanitized = __sanitize_quote(block)
            return ParentNode("blockquote", text_to_children(sanitized))
        case BlockType.UNORDERED_LIST:
            return ParentNode("ul", __get_list_item_html_nodes(block, block_type))
        case BlockType.ORDERED_LIST:
            return ParentNode("ol", __get_list_item_html_nodes(block, block_type))
        case BlockType.PARAGRAPH:
            return ParentNode("p", text_to_children(block))
        case _: 
            raise Exception("Invalid Block Type")

def text_to_children(text : str) -> list[LeafNode]:
    sanitized = text.replace("\n", " ")
    sanitized = ' '.join(sanitized.split())
    child_text_nodes = text_to_text_nodes(sanitized)
    return list(map(text_node_to_html_node, child_text_nodes))

def __get_heading_level(text : str) -> str:
    count = 0
    for char in text:
        if char == "#":
            count += 1
        else:
            break

    match count:
        case 1: return "h1"
        case 2: return "h2"
        case 3: return "h3"
        case 4: return "h4"
        case 5: return "h5"
        case _: return "h6"

def __sanitize_heading(text : str, heading_level : str) -> str:
    match heading_level:
        case "h1":
            return text[2:]
        case "h2":
            return text[3:]
        case "h3":
            return text[4:]
        case "h4":
            return text[5:]
        case "h5":
            return text[6:]
        case "h6":
            return text[7:]
        case _:
            raise Exception(f"Invalid heading level: {heading_level}")
        
def __sanitize_quote(text : str) -> str:
    return text.replace(">", "")

def __get_list_item_html_nodes(text : str, block_type : BlockType) -> list[HTMLNode]:
    text_items = text.split("\n")
    list_items = []
    for item in text_items:
        sanitized = item
        if block_type == BlockType.UNORDERED_LIST:
            sanitized = item[2:]
        else:
            sanitized = item[3:]
        children = text_to_children(sanitized)
        list_items.append(ParentNode("li", children))
    return list_items

def extract_title(markdown:str) -> str:
    for line in markdown.split("\n"):
        if line[:2] == "# ":
            return line[2:].strip()
    raise Exception(f"No h1 header in markdown: {markdown}")