import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_delimiters_and_positions(self) -> None:
        formats: list[tuple[str, TextType]] = [
            ("**", TextType.BOLD),
            ("_", TextType.ITALIC),
            ("`", TextType.CODE),
        ]

        delimiter: str
        text_type: TextType
        for delimiter, text_type in formats:
            cases: list[tuple[str, list[TextNode]]] = [
                (
                    "plain text",
                    [TextNode("plain text", TextType.TEXT)],
                ),
                (
                    f"before {delimiter}inside{delimiter} after",
                    [
                        TextNode("before ", TextType.TEXT),
                        TextNode("inside", text_type),
                        TextNode(" after", TextType.TEXT),
                    ],
                ),
                (
                    f"{delimiter}inside{delimiter} after",
                    [
                        TextNode("inside", text_type),
                        TextNode(" after", TextType.TEXT),
                    ],
                ),
                (
                    f"before {delimiter}inside{delimiter}",
                    [
                        TextNode("before ", TextType.TEXT),
                        TextNode("inside", text_type),
                    ],
                ),
                (
                    f"{delimiter}inside{delimiter}",
                    [TextNode("inside", text_type)],
                ),
                (
                    f"{delimiter}one{delimiter} and "
                    f"{delimiter}two{delimiter}",
                    [
                        TextNode("one", text_type),
                        TextNode(" and ", TextType.TEXT),
                        TextNode("two", text_type),
                    ],
                ),
                ("", []),
            ]

            text: str
            expected: list[TextNode]
            for text, expected in cases:
                with self.subTest(delimiter=delimiter, text=text):
                    self.assertEqual(
                        split_nodes_delimiter(
                            [TextNode(text, TextType.TEXT)],
                            delimiter,
                            text_type,
                        ),
                        expected,
                    )

    def test_unmatched_delimiters(self) -> None:
        cases: list[tuple[str, str, TextType]] = [
            ("before **unfinished", "**", TextType.BOLD),
            ("unfinished_", "_", TextType.ITALIC),
            ("`one` and `unfinished", "`", TextType.CODE),
        ]

        text: str
        delimiter: str
        text_type: TextType
        for text, delimiter, text_type in cases:
            with self.subTest(text=text):
                with self.assertRaisesRegex(
                    ValueError, "unmatched delimiter"
                ):
                    split_nodes_delimiter(
                        [TextNode(text, TextType.TEXT)],
                        delimiter,
                        text_type,
                    )

    def test_multiple_nodes_and_preserves_existing_node(self) -> None:
        existing: TextNode = TextNode("literal **", TextType.CODE)
        old_nodes: list[TextNode] = [
            existing,
            TextNode("a **bold**", TextType.TEXT),
            TextNode(" tail", TextType.TEXT),
        ]

        result: list[TextNode] = split_nodes_delimiter(
            old_nodes, "**", TextType.BOLD
        )

        self.assertEqual(
            result,
            [
                existing,
                TextNode("a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" tail", TextType.TEXT),
            ],
        )
        self.assertIs(result[0], existing)
        self.assertIsNot(result, old_nodes)
        self.assertEqual(len(old_nodes), 3)
        self.assertEqual(old_nodes[1].text, "a **bold**")

    def test_multiple_passes(self) -> None:
        nodes: list[TextNode] = [
            TextNode(
                "`literal **` and **bold** and _italic_",
                TextType.TEXT,
            )
        ]

        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

        self.assertEqual(
            nodes,
            [
                TextNode("literal **", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
        )

    def test_empty_input(self) -> None:
        self.assertEqual(
            split_nodes_delimiter([], "**", TextType.BOLD),
            [],
        )

    def test_empty_delimiter(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not be empty"):
            split_nodes_delimiter(
                [TextNode("hello", TextType.TEXT)],
                "",
                TextType.BOLD,
            )


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_single_image(self) -> None:
        text: str = (
            "This is text with an "
            "![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertEqual(
            extract_markdown_images(text),
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
        )

    def test_extract_multiple_images(self) -> None:
        text: str = (
            "![rick roll](https://i.imgur.com/aKaOqIh.gif) and "
            "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )

        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_single_link(self) -> None:
        self.assertEqual(
            extract_markdown_links(
                "Visit [Boot.dev](https://www.boot.dev)!"
            ),
            [("Boot.dev", "https://www.boot.dev")],
        )

    def test_extract_multiple_links(self) -> None:
        text: str = (
            "[to boot dev](https://www.boot.dev) and "
            "[to youtube](https://www.youtube.com/@bootdotdev)"
        )

        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_images_and_links_stay_separate(self) -> None:
        text: str = (
            "![logo](logo.png)"
            "[homepage](https://example.com)"
            "![cat](cat.png)"
        )

        self.assertEqual(
            extract_markdown_images(text),
            [("logo", "logo.png"), ("cat", "cat.png")],
        )
        self.assertEqual(
            extract_markdown_links(text),
            [("homepage", "https://example.com")],
        )

    def test_image_is_not_a_link(self) -> None:
        self.assertEqual(
            extract_markdown_links("![image](image.png)"),
            [],
        )

    def test_no_matches(self) -> None:
        text: str
        for text in ["", "plain text", "[unfinished](url"]:
            with self.subTest(text=text):
                self.assertEqual(extract_markdown_images(text), [])
                self.assertEqual(extract_markdown_links(text), [])

    def test_empty_labels(self) -> None:
        self.assertEqual(
            extract_markdown_images("![](image.png)"),
            [("", "image.png")],
        )
        self.assertEqual(
            extract_markdown_links("[](https://example.com)"),
            [("", "https://example.com")],
        )

    def test_duplicate_matches_are_preserved(self) -> None:
        self.assertEqual(
            extract_markdown_images("![cat](cat.png)![cat](cat.png)"),
            [("cat", "cat.png"), ("cat", "cat.png")],
        )
        self.assertEqual(
            extract_markdown_links("[page](/page)[page](/page)"),
            [("page", "/page"), ("page", "/page")],
        )


if __name__ == "__main__":
    unittest.main()
