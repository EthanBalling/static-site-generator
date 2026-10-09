import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_none(self) -> None:
        node: HTMLNode = HTMLNode(props=None)

        self.assertEqual(node.props_to_html(), "")

    def test_props_empty(self) -> None:
        node: HTMLNode = HTMLNode(props={})

        self.assertEqual(node.props_to_html(), "")

    def test_single_property(self) -> None:
        node: HTMLNode = HTMLNode(
            tag="a",
            props={"href": "https://www.google.com"},
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com"',
        )

    def test_multiple_properties(self) -> None:
        node: HTMLNode = HTMLNode(
            tag="a",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank"',
        )

class TestLeafNode(unittest.TestCase):
    def test_paragraph(self) -> None:
        node: LeafNode = LeafNode("p", "Hello, world!")

        self.assertEqual(
            node.to_html(),
            "<p>Hello, world!</p>",
        )

    def test_bold(self) -> None:
        node: LeafNode = LeafNode("b", "Bold text")

        self.assertEqual(
            node.to_html(),
            "<b>Bold text</b>",
        )

    def test_link_with_attributes(self) -> None:
        node: LeafNode = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com"},
        )

        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_raw_text(self) -> None:
        node: LeafNode = LeafNode(None, "Plain text")

        self.assertEqual(node.to_html(), "Plain text")

    def test_empty_string_is_valid(self) -> None:
        node: LeafNode = LeafNode("p", "")

        self.assertEqual(node.to_html(), "<p></p>")

    def test_missing_value_raises(self) -> None:
        node: LeafNode = LeafNode("p", None)

        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()
