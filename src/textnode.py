import re

from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid TextNode TextType! {text_node.text_type} is not a valid TextType!")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for old_node in old_nodes:
        # Only concerned with TEXT nodes
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        delim_count = old_node.text.count(delimiter)
        # If the TEXT node does not contain any of the delimiters, move on
        if delim_count == 0:
            new_nodes.append(old_node)
            continue
        # Ensure there are matching closing delimiters
        if delim_count % 2 != 0:
            raise Exception(f"Cannot convert {old_node} to TextType {text_type}, delimiters are invalid!")

        text = old_node.text
        for _ in range(0, delim_count // 2):
            begin = text.find(delimiter)
            if begin > 0:
                new_nodes.append(TextNode(text[0:begin], TextType.TEXT))

            text = text[begin + len(delimiter):]
            end = text.find(delimiter)
            new_nodes.append(TextNode(text[0:end], text_type))
            text = text[end + len(delimiter):]

        if len(text) > 0:
            new_nodes.append(TextNode(text[0:], TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    images = []

    # md images look like ![alt](src)
    images = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)

    return images

def extract_markdown_links(text):
    links = []

    # md links look like [alt](href)
    links = re.findall(r"\[(.*?)\]\((.*?)\)", text)

    return links

def split_nodes_images(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        for image in images:
            delimiter = f'![{image[0]}]({image[1]})'
            begin = text.find(delimiter)
            if begin > 0:
                new_nodes.append(TextNode(text[0:begin], TextType.TEXT))

            text = text[begin + len(delimiter):]
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))

        if len(text) > 0:
            new_nodes.append(TextNode(text[0:], TextType.TEXT))

    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        for link in links:
            delimiter = f'[{link[0]}]({link[1]})'
            begin = text.find(delimiter)
            if begin > 0:
                new_nodes.append(TextNode(text[0:begin], TextType.TEXT))

            text = text[begin + len(delimiter):]
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))

        if len(text) > 0:
            new_nodes.append(TextNode(text[0:], TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    text_nodes = []

    text_node = TextNode(text, TextType.TEXT)
    text_nodes = split_nodes_delimiter([text_node], '`', TextType.CODE)
    text_nodes = split_nodes_delimiter(text_nodes, '**', TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, '*', TextType.ITALIC)
    text_nodes = split_nodes_images(text_nodes)
    text_nodes = split_nodes_links(text_nodes)

    return text_nodes
