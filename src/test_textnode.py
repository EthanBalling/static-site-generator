import unittest
from typing import cast

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_equal_nodes(self) -> None:
        node: TextNode = TextNode(
            "Read more", TextType.LINK, "https://www.boot.dev"
        )
        other: TextNode = TextNode(
            "Read more", TextType.LINK, "https://www.boot.dev"
        )

        self.assertEqual(node, other)

    def test_default_url_equals_explicit_none(self) -> None:
        node: TextNode = TextNode("Hello", TextType.TEXT)
        other: TextNode = TextNode("Hello", TextType.TEXT, None)

        self.assertEqual(node, other)

    def test_different_text(self) -> None:
            node: TextNode = TextNode("Hello", TextType.BOLD)
            other: TextNode = TextNode("Goodbye", TextType.BOLD)

            self.assertNotEqual(node, other)

    def test_different_text_type(self) -> None:
        node: TextNode = TextNode("Hello", TextType.BOLD)
        other: TextNode = TextNode("Hello", TextType.ITALIC)

        self.assertNotEqual(node, other)

    def test_different_url(self) -> None:
        node: TextNode = TextNode(
            "Read more", TextType.LINK, "https://www.boot.dev"
        )
        other: TextNode = TextNode(
            "Read more", TextType.LINK, "https://example.com"
        )

        self.assertNotEqual(node, other)

    def test_url_differs_from_none(self) -> None:
        node: TextNode = TextNode(
            "Read more", TextType.LINK, "https://www.boot.dev"
        )
        other: TextNode = TextNode("Read more", TextType.LINK, None)

        self.assertNotEqual(node, other)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_and_formatting_types(self) -> None:
        cases: list[tuple[TextType, str | None]] = [
            (TextType.TEXT, None),
            (TextType.BOLD, "b"),
            (TextType.ITALIC, "i"),
            (TextType.CODE, "code"),
        ]

        for text_type, expected_tag in cases:
            with self.subTest(text_type=text_type):
                node: TextNode = TextNode("Example", text_type)
                html_node: LeafNode = text_node_to_html_node(node)

                self.assertEqual(html_node.tag, expected_tag)
                self.assertEqual(html_node.value, "Example")
                self.assertIsNone(html_node.props)

    def test_link(self) -> None:
        node: TextNode = TextNode(
            "Visit Boot.dev",
            TextType.LINK,
            "https://www.boot.dev",
        )
        html_node: LeafNode = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Visit Boot.dev")
        self.assertEqual(
            html_node.props,
            {"href": "https://www.boot.dev"},
        )

    def test_image(self) -> None:
        node: TextNode = TextNode(
            "A mountain",
            TextType.IMAGE,
            "https://example.com/mountain.png",
        )
        html_node: LeafNode = text_node_to_html_node(node)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {
                "src": "https://example.com/mountain.png",
                "alt": "A mountain",
            },
        )

    def test_unsupported_type_raises(self) -> None:
        node: TextNode = TextNode(
            "Example",
            cast(TextType, "unsupported"),
        )

        with self.assertRaises(ValueError):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
