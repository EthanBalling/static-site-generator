import re

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType,
) -> list[TextNode]:
    if delimiter == "":
        raise ValueError("Delimiter must not be empty")

    new_nodes: list[TextNode] = []

    node: TextNode
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        sections: list[str] = node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError(
                f"Invalid Markdown: unmatched delimiter {delimiter!r}"
            )

        index: int
        section: str
        for index, section in enumerate(sections):
            if section == "":
                continue

            section_type: TextType = TextType.TEXT
            if index % 2 == 1:
                section_type = text_type

            new_nodes.append(TextNode(section, section_type))

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches: list[tuple[str, str]] = re.findall(
        r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",
        text,
    )
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches: list[tuple[str, str]] = re.findall(
        r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",
        text,
    )
    return matches

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    node: TextNode
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        cursor: int = 0

        match: re.Match[str]
        for match in re.finditer(
            r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",
            node.text,
        ):
            if match.start() > cursor:
                new_nodes.append(
                    TextNode(
                        node.text[cursor:match.start()],
                        TextType.TEXT,
                    )
                )

            new_nodes.append(
                TextNode(
                    match.group(1),
                    TextType.IMAGE,
                    match.group(2),
                )
            )
            cursor = match.end()

        if cursor < len(node.text):
            new_nodes.append(
                TextNode(node.text[cursor:], TextType.TEXT)
            )

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    node: TextNode
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        cursor: int = 0

        match: re.Match[str]
        for match in re.finditer(
            r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",
            node.text,
        ):
            if match.start() > cursor:
                new_nodes.append(
                    TextNode(
                        node.text[cursor:match.start()],
                        TextType.TEXT,
                    )
                )

            new_nodes.append(
                TextNode(
                    match.group(1),
                    TextType.LINK,
                    match.group(2),
                )
            )
            cursor = match.end()

        if cursor < len(node.text):
            new_nodes.append(
                TextNode(node.text[cursor:], TextType.TEXT)
            )

    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
