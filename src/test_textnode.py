import unittest
from textnode import TextNode, TextType

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


if __name__ == "__main__":
    unittest.main()
