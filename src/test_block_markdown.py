import unittest

from block_markdown import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
