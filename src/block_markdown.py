from enum import Enum


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []
    candidates: list[str] = markdown.split("\n\n")

    candidate: str
    for candidate in candidates:
        block: str = candidate.strip()

        if block != "":
            blocks.append(block)

    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    level: int
    for level in range(1, 7):
        if block.startswith("#" * level + " "):
            return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines: list[str] = block.split("\n")

    line: str
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    index: int
    if all(
        line.startswith(f"{index}. ")
        for index, line in enumerate(lines, start=1)
    ):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
