import unittest

from htmlnode import ParentNode
from markdown_html import markdown_to_html_node


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self) -> None:
        markdown: str = (
            "This is **bolded** paragraph\n"
            "text in a p\n"
            "tag here\n\n"
            "This is another paragraph with *italic* text "
            "and `code` here"
        )

        node: ParentNode = markdown_to_html_node(markdown)

        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bolded</b> paragraph "
            "text in a p tag here</p>"
            "<p>This is another paragraph with <i>italic</i> "
            "text and <code>code</code> here</p></div>",
        )

    def test_all_heading_levels(self) -> None:
        level: int
        for level in range(1, 7):
            with self.subTest(level=level):
                markdown: str = "#" * level + " A **heading**"

                self.assertEqual(
                    markdown_to_html_node(markdown).to_html(),
                    f"<div><h{level}>A <b>heading</b>"
                    f"</h{level}></div>",
                )

    def test_codeblock_preserves_contents(self) -> None:
        markdown: str = (
            "```\n"
            "This is text that _should_ remain\n"
            "the **same** even with inline stuff\n"
            "```"
        )

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><pre><code>"
            "This is text that _should_ remain\n"
            "the **same** even with inline stuff\n"
            "</code></pre></div>",
        )

    def test_codeblock_preserves_indentation(self) -> None:
        markdown: str = (
            "```\n"
            "    indented *literal* text\n"
            "      more indentation\n"
            "```"
        )

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><pre><code>"
            "    indented *literal* text\n"
            "      more indentation\n"
            "</code></pre></div>",
        )

    def test_quote(self) -> None:
        markdown: str = "> A **bold** quote\n>without a space"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><blockquote>A <b>bold</b> quote "
            "without a space</blockquote></div>",
        )

    def test_unordered_list(self) -> None:
        markdown: str = "- **First** item\n- Second *item*"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><ul>"
            "<li><b>First</b> item</li>"
            "<li>Second <i>item</i></li>"
            "</ul></div>",
        )

    def test_ordered_list(self) -> None:
        markdown: str = "1. First\n2. Second with `code`"

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            "<div><ol>"
            "<li>First</li>"
            "<li>Second with <code>code</code></li>"
            "</ol></div>",
        )

    def test_ordered_list_double_digit_markers(self) -> None:
        number: int
        markdown: str = "\n".join(
            f"{number}. Item {number}" for number in range(1, 11)
        )
        expected_items: str = "".join(
            f"<li>Item {number}</li>" for number in range(1, 11)
        )

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            f"<div><ol>{expected_items}</ol></div>",
        )

    def test_links_and_images(self) -> None:
        markdown: str = (
            "[Boot.dev](https://boot.dev) and ![cat](cat.png)"
        )

        self.assertEqual(
            markdown_to_html_node(markdown).to_html(),
            '<div><p><a href="https://boot.dev">Boot.dev</a>'
            ' and <img src="cat.png" alt="cat"></img></p></div>',
        )

    def test_mixed_blocks_preserve_order(self) -> None:
        markdown: str = (
            "# Title\n\n"
            "A paragraph.\n\n"
            "- Item\n\n"
            "> Quote"
        )

        node: ParentNode = markdown_to_html_node(markdown)

        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "div")
        self.assertIsNotNone(node.children)
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<h1>Title</h1>"
            "<p>A paragraph.</p>"
            "<ul><li>Item</li></ul>"
            "<blockquote>Quote</blockquote>"
            "</div>",
        )

    def test_empty_document(self) -> None:
        self.assertEqual(
            markdown_to_html_node("").to_html(),
            "<div></div>",
        )


if __name__ == "__main__":
    unittest.main()
