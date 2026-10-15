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
