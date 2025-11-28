from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code block"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(md_block : str) -> BlockType:
    if __is_heading(md_block):
        return BlockType.HEADING

    if __is_code(md_block):
        return BlockType.CODE
    
    if __is_quote(md_block):
        return BlockType.QUOTE
        
    if __is_unordered_list(md_block):
        return BlockType.UNORDERED_LIST
    
    if __is_ordered_list(md_block):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def __is_heading(md_block:str) -> bool:
    if md_block[0] != "#":
        return False
    count = 0
    for i in range(len(md_block)):
        if md_block[i] == "#":
            count += 1
        else:
            break

    return count <= 6


def __is_code(md_block:str) -> bool:
    return md_block[:3] == "```" and md_block[-3:] == "```"

def __is_quote(md_block:str) -> bool:
    is_valid_quote = True
    for line in md_block.split("\n"):
        if line[0] != ">":
            is_valid_quote = False
    return is_valid_quote

def __is_unordered_list(md_block:str) -> bool:
    is_valid_list = True
    for line in md_block.split("\n"):
        if line[0:2] != "- ":
            is_valid_list = False
    return is_valid_list

def __is_ordered_list(md_block:str) -> bool:
    is_valid_list = True
    lines = md_block.split("\n")
    for i in range(len(lines)):
        if lines[i][:3] != f"{i+1}. ":
            is_valid_list = False
    return is_valid_list