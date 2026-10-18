import os
import tempfile
import unittest
from pathlib import Path

from generate_page import extract_title, generate_page, generate_pages_recursive


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


class TestGeneratePagesRecursive(unittest.TestCase):
    def test_generates_nested_pages_and_preserves_relative_filenames(self) -> None:
        temporary: str
        with tempfile.TemporaryDirectory() as temporary:
            root: Path = Path(temporary)
            content: Path = root / "content"
            output: Path = root / "public"
            template: Path = root / "template.html"
            template.write_text(
                "<title>{{ Title }}</title><article>{{ Content }}</article>",
                encoding="utf-8",
            )
            pages: dict[str, str] = {
                "index.md": "Home",
                "contact/index.md": "Contact",
                "blog/post/index.md": "Café",
                "blog/post/extra.md.notes.md": "Notes",
            }
            relative_path: str
            title: str
            for relative_path, title in pages.items():
                source: Path = content / relative_path
                source.parent.mkdir(parents=True, exist_ok=True)
                source.write_text(f"# {title}\n\nA **page**.", encoding="utf-8")

            generate_pages_recursive(str(content), str(template), str(output))

            actual_paths: set[str] = {
                str(path.relative_to(output)) for path in output.rglob("*.html")
            }
            self.assertEqual(
                actual_paths,
                {str(Path(path).with_suffix(".html")) for path in pages},
            )
            for relative_path, title in pages.items():
                with self.subTest(path=relative_path):
                    destination: Path = output / Path(relative_path).with_suffix(".html")
                    self.assertEqual(
                        destination.read_text(encoding="utf-8"),
                        f"<title>{title}</title><article><div><h1>{title}</h1>"
                        "<p>A <b>page</b>.</p></div></article>",
                    )

    def test_ignores_non_markdown_and_preserves_existing_static_assets(self) -> None:
        temporary: str
        with tempfile.TemporaryDirectory() as temporary:
            root: Path = Path(temporary)
            content: Path = root / "content"
            output: Path = root / "public"
            content.mkdir()
            output.mkdir()
            template: Path = root / "template.html"
            template.write_text("{{ Content }}", encoding="utf-8")
            (content / "index.md").write_text("# Home", encoding="utf-8")
            (content / "notes.txt").write_text("Not Markdown", encoding="utf-8")
            (output / "index.css").write_text("body {}", encoding="utf-8")

            generate_pages_recursive(str(content), str(template), str(output))

            self.assertEqual(
                {path.name for path in output.iterdir()}, {"index.html", "index.css"}
            )
            self.assertEqual((output / "index.css").read_text(encoding="utf-8"), "body {}")

    def test_handles_empty_directories(self) -> None:
        temporary: str
        with tempfile.TemporaryDirectory() as temporary:
            root: Path = Path(temporary)
            content: Path = root / "content"
            (content / "empty").mkdir(parents=True)
            output: Path = root / "public"
            template: Path = root / "template.html"
            template.write_text("{{ Content }}", encoding="utf-8")

            generate_pages_recursive(str(content), str(template), str(output))

            self.assertEqual(list(output.rglob("*.html")), [])

    def test_missing_content_directory_raises(self) -> None:
        temporary: str
        with tempfile.TemporaryDirectory() as temporary:
            root: Path = Path(temporary)
            with self.assertRaises(FileNotFoundError):
                generate_pages_recursive(
                    str(root / "missing"),
                    str(root / "template.html"),
                    str(root / "public"),
                )


if __name__ == "__main__":
    unittest.main()
