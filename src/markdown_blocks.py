from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, text_node_to_html_node, TextType
from split_delimiter import text_to_textnodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped == "":
             continue
        else:
            new_blocks.append(stripped)
    return new_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(markdown_block):
    hash_count = len(markdown_block) - len(markdown_block.lstrip("#"))
    if 1 <= hash_count <= 6 and markdown_block.startswith("#" * hash_count + " "):
        return BlockType.HEADING
    
    if markdown_block.startswith("```\n") and markdown_block.endswith("```"):
        return BlockType.CODE
    
    lines = markdown_block.split("\n")

    quote_all_true = True
    for line in lines:
        if not line.startswith('>'):
            quote_all_true = False
            break
    if quote_all_true:
        return BlockType.QUOTE
    
    unordered_all_true = True
    for line in lines:
        if not line.startswith("- "):
            unordered_all_true = False
            break
    if unordered_all_true:
        return BlockType.UNORDERED_LIST
    
    ordered_all_true = True
    num = 0
    for line in lines:
        num += 1
        prefix = str(num) + "."
        if not line.startswith(prefix):
            ordered_all_true = False
            break
    if ordered_all_true:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
    
def text_to_children(text):
    markdowns = text_to_textnodes(text)
    nodes = []
    for node in markdowns:
        nodes.append(text_node_to_html_node(node))
    return nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            clean_block = " ".join(block.split("\n"))
            children = text_to_children(clean_block)
            node = ParentNode("p", children) 
            block_nodes.append(node)         
        elif block_type == BlockType.HEADING:
            hash_count = len(block) - len(block.lstrip("#"))
            clean_block = block.lstrip("#").lstrip(" ")
            children = text_to_children(clean_block)
            node = ParentNode(f"h{hash_count}", children)
            block_nodes.append(node)
        elif block_type == BlockType.CODE:
            clean_block = block[4:-3]
            node = TextNode(clean_block, TextType.CODE)
            code_node = text_node_to_html_node(node)
            block_nodes.append(ParentNode("pre", [code_node]))
        else:
            lines = block.split("\n")
            if block_type == BlockType.QUOTE:
                stripped = []
                for line in lines:
                    stripped.append(line[1:].lstrip(" "))
                clean_block = "\n".join(stripped)
                children = text_to_children(clean_block)
                node = ParentNode("blockquote", children) 
                block_nodes.append(node)
            elif block_type == BlockType.UNORDERED_LIST:
                li_nodes = []
                for line in lines:
                    line_item = line[2:].lstrip(" ")
                    children = text_to_children(line_item)
                    li_nodes.append(ParentNode("li", children))
                block_nodes.append(ParentNode("ul", li_nodes))
            elif block_type == BlockType.ORDERED_LIST:
                num = 0
                li_nodes = []
                for line in lines:
                    num += 1
                    prefix = str(num) + "."
                    line_item = line[len(prefix):].lstrip(" ")
                    children = text_to_children(line_item)
                    li_nodes.append(ParentNode("li", children))
                block_nodes.append(ParentNode("ol", li_nodes))
    parent = ParentNode("div", block_nodes)
    return parent