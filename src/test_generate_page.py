import os
import tempfile
import unittest
from pathlib import Path

from generate_page import extract_title, generate_page


class TestExtractTitle(unittest.TestCase):
    def test_extracts_and_trims_h1(self) -> None:
        self.assertEqual(extract_title("# Hello"), "Hello")
        self.assertEqual(extract_title("#   Tolkien Fan Club  "), "Tolkien Fan Club")

    def test_finds_first_h1_among_other_blocks(self) -> None:
        markdown: str = "## Subtitle\n\nText\n\n# First title\n\n# Second title"
        self.assertEqual(extract_title(markdown), "First title")

    def test_requires_single_hash_followed_by_space(self) -> None:
        markdown: str
        for markdown in ("", "Paragraph", "## Subtitle", "#No space", "Text # Heading"):
            with self.subTest(markdown=markdown):
                with self.assertRaisesRegex(ValueError, "h1"):
                    extract_title(markdown)


class TestGeneratePage(unittest.TestCase):
    def test_generates_utf8_html_and_creates_destination_directories(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root: Path = Path(temporary)
            source: Path = root / "index.md"
            template: Path = root / "template.html"
            destination: Path = root / "public" / "nested" / "index.html"
            source.write_text("# Café\n\nHello **world**.", encoding="utf-8")
            template.write_text(
                "<title>{{ Title }}</title><article>{{ Content }}</article>",
                encoding="utf-8",
            )

            generate_page(str(source), str(template), str(destination))

            self.assertEqual(
                destination.read_text(encoding="utf-8"),
                "<title>Café</title><article><div><h1>Café</h1>"
                "<p>Hello <b>world</b>.</p></div></article>",
            )
            self.assertEqual(source.read_text(encoding="utf-8"), "# Café\n\nHello **world**.")

    def test_writes_destination_filename_without_directory_component(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root: Path = Path(temporary)
            source: Path = root / "index.md"
            template: Path = root / "template.html"
            source.write_text("# Title", encoding="utf-8")
            template.write_text("{{ Title }}: {{ Content }}", encoding="utf-8")
            previous_directory: str = os.getcwd()
            try:
                os.chdir(root)
                generate_page(str(source), str(template), "index.html")
            finally:
                os.chdir(previous_directory)

            self.assertEqual(
                (root / "index.html").read_text(encoding="utf-8"),
                "Title: <div><h1>Title</h1></div>",
            )

    def test_missing_title_preserves_existing_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root: Path = Path(temporary)
            source: Path = root / "index.md"
            template: Path = root / "template.html"
            destination: Path = root / "index.html"
            source.write_text("No title here.", encoding="utf-8")
            template.write_text("{{ Title }} {{ Content }}", encoding="utf-8")
            destination.write_text("Previous output", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "h1"):
                generate_page(str(source), str(template), str(destination))

            self.assertEqual(destination.read_text(encoding="utf-8"), "Previous output")


if __name__ == "__main__":
    unittest.main()
