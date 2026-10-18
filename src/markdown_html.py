from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
)
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node

def text_to_children(text: str) -> list[HTMLNode]:
    children: list[HTMLNode] = []
    text_nodes: list[TextNode] = text_to_textnodes(text)

    text_node: TextNode
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))

    return children

def paragraph_to_html_node(block: str) -> ParentNode:
    text: str = block.replace("\n", " ")
    return ParentNode("p", text_to_children(text))

def heading_to_html_node(block: str) -> ParentNode:
    marker: str
    text: str
    marker, text = block.split(" ", 1)

    level: int = len(marker)
    return ParentNode(f"h{level}", text_to_children(text.strip()))

def code_to_html_node(block: str) -> ParentNode:
    text: str = block[4:-3]
    code_node: TextNode = TextNode(text, TextType.CODE)
    children: list[HTMLNode] = [
        text_node_to_html_node(code_node)
    ]

    return ParentNode("pre", children)

def quote_to_html_node(block: str) -> ParentNode:
    quote_lines: list[str] = []

    line: str
    for line in block.split("\n"):
        quote_lines.append(line[1:].strip())

    text: str = " ".join(quote_lines)
    return ParentNode("blockquote", text_to_children(text))

def list_to_html_node(block: str, tag: str) -> ParentNode:
    items: list[HTMLNode] = []

    line: str
    for line in block.split("\n"):
        text: str = line.split(" ", 1)[1].strip()
        items.append(ParentNode("li", text_to_children(text)))

    return ParentNode(tag, items)

def block_to_html_node(block: str) -> ParentNode:
    block_type: BlockType = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)

    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)

    if block_type == BlockType.CODE:
        return code_to_html_node(block)

    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)

    if block_type == BlockType.UNORDERED_LIST:
        return list_to_html_node(block, "ul")

    if block_type == BlockType.ORDERED_LIST:
        return list_to_html_node(block, "ol")

    raise ValueError(f"Unsupported block type: {block_type!r}")

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks: list[str] = markdown_to_blocks(markdown)
    children: list[HTMLNode] = []

    block: str
    for block in blocks:
        children.append(block_to_html_node(block))

    return ParentNode("div", children)
