import unittest

from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_assignment_example(self) -> None:
        markdown: str = (
            "\nThis is **bolded** paragraph\n\n"
            "This is another paragraph with *italic* text "
            "and `code` here\n"
            "This is the same paragraph on a new line\n\n"
            "- This is a list\n"
            "- with items\n"
        )

        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "This is **bolded** paragraph",
                (
                    "This is another paragraph with *italic* text "
                    "and `code` here\n"
                    "This is the same paragraph on a new line"
                ),
                "- This is a list\n- with items",
            ],
        )

    def test_heading_paragraph_and_list(self) -> None:
        markdown: str = (
            "# Heading\n\n"
            "A paragraph with **bold** text.\n\n"
            "- First item\n"
            "- Second item"
        )

        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "# Heading",
                "A paragraph with **bold** text.",
                "- First item\n- Second item",
            ],
        )

    def test_single_newline_stays_inside_block(self) -> None:
        self.assertEqual(
            markdown_to_blocks("First line\nSecond line"),
            ["First line\nSecond line"],
        )

    def test_strips_each_block(self) -> None:
        self.assertEqual(
            markdown_to_blocks("  First block  \n\n\tSecond block\t"),
            ["First block", "Second block"],
        )

    def test_excessive_newlines(self) -> None:
        self.assertEqual(
            markdown_to_blocks("\n\n\nFirst\n\n\n\n\nSecond\n\n\n"),
            ["First", "Second"],
        )

    def test_removes_whitespace_only_blocks(self) -> None:
        self.assertEqual(
            markdown_to_blocks("First\n\n \t \n\nSecond"),
            ["First", "Second"],
        )

    def test_empty_or_whitespace_only_document(self) -> None:
        markdown: str
        for markdown in ["", "   ", "\n\n\n\n", " \t\n\n \t"]:
            with self.subTest(markdown=markdown):
                self.assertEqual(markdown_to_blocks(markdown), [])

    def test_preserves_internal_spacing(self) -> None:
        self.assertEqual(
            markdown_to_blocks("First  line\n    indented line"),
            ["First  line\n    indented line"],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_all_heading_levels(self) -> None:
        level: int
        for level in range(1, 7):
            with self.subTest(level=level):
                self.assertEqual(
                    block_to_block_type("#" * level + " Heading"),
                    BlockType.HEADING,
                )

    def test_invalid_headings_are_paragraphs(self) -> None:
        block: str
        for block in [
            "#Heading",
            "##Heading",
            "####### Heading",
            "#\tHeading",
            "Text with # heading characters",
        ]:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    def test_code_blocks(self) -> None:
        block: str
        for block in [
            "```\nprint('hello')\n```",
            "```\nfirst line\nsecond line\n```",
            "```\n```",
        ]:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.CODE,
                )

    def test_invalid_code_blocks_are_paragraphs(self) -> None:
        block: str
        for block in [
            "```inline```",
            "```\nmissing closing fence",
            "missing opening fence\n```",
            "```python\nprint('hello')\n```",
            "```\ncode\n``` trailing text",
        ]:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    def test_quotes_with_optional_spaces(self) -> None:
        self.assertEqual(
            block_to_block_type("> First line\n>Second line\n>"),
            BlockType.QUOTE,
        )

    def test_quote_requires_every_line(self) -> None:
        self.assertEqual(
            block_to_block_type("> First line\nUnmarked line"),
            BlockType.PARAGRAPH,
        )

    def test_unordered_list(self) -> None:
        self.assertEqual(
            block_to_block_type("- First\n- Second\n- Third"),
            BlockType.UNORDERED_LIST,
        )

    def test_invalid_unordered_lists(self) -> None:
        block: str
        for block in [
            "- First\n-Second",
            "- First\nPlain text",
            "- First\n - Indented marker",
            "* First\n* Second",
        ]:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    def test_ordered_list(self) -> None:
        self.assertEqual(
            block_to_block_type("1. First\n2. Second\n3. Third"),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_with_double_digit_numbers(self) -> None:
        number: int
        block: str = "\n".join(
            f"{number}. Item" for number in range(1, 12)
        )

        self.assertEqual(
            block_to_block_type(block),
            BlockType.ORDERED_LIST,
        )

    def test_invalid_ordered_lists(self) -> None:
        block: str
        for block in [
            "0. First\n1. Second",
            "2. First\n3. Second",
            "1. First\n3. Third",
            "1. First\n1. Repeated",
            "1. First\n2.Second",
            "1. First\nPlain text",
            "01. First\n02. Second",
        ]:
            with self.subTest(block=block):
                self.assertEqual(
                    block_to_block_type(block),
                    BlockType.PARAGRAPH,
                )

    def test_single_item_lists(self) -> None:
        self.assertEqual(
            block_to_block_type("- One item"),
            BlockType.UNORDERED_LIST,
        )
        self.assertEqual(
            block_to_block_type("1. One item"),
            BlockType.ORDERED_LIST,
        )

    def test_paragraph(self) -> None:
        self.assertEqual(
            block_to_block_type(
                "A paragraph with **bold** and `inline code`.\n"
                "It continues on another line."
            ),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
