import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()