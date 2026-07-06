from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid Markdown syntax, no closing delimiter found")
        
        for i, part in enumerate(parts):
            if part == "":
                continue
            current_type = text_type if i % 2 == 1 else TextType.TEXT
            new_list.append(TextNode(part, current_type))
    return new_list

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list [TextNode]:
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        remaining = node.text
        images = extract_markdown_images(remaining)
        if len(images) == 0:
            new_list.append(node)
            continue
        for image in images:
            sections = remaining.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            remaining = sections[1]
        if remaining != "":
            new_list.append(TextNode(remaining, TextType.TEXT))

    return new_list

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_list = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_list.append(node)
            continue
        remaining = node.text
        links = extract_markdown_links(remaining)
        if len(links) == 0:
            new_list.append(node)
            continue
        for link in links:
            sections = remaining.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_list.append(TextNode(sections[0], TextType.TEXT))
            new_list.append(
                TextNode(
                    link[0],
                    TextType.LINK,
                    link[1],
                )
            )
            remaining = sections[1]
        if remaining != "":
            new_list.append(TextNode(remaining, TextType.TEXT))

    return new_list

def text_to_textnodes(text):
    old_text = [TextNode(text, TextType.TEXT)]
    old_text = split_nodes_delimiter(old_text, "**", TextType.BOLD)
    old_text = split_nodes_delimiter(old_text, "_", TextType.ITALIC)
    old_text = split_nodes_delimiter(old_text, "`", TextType.CODE)
    old_text = split_nodes_image(old_text)
    old_text = split_nodes_link(old_text)
    return old_text