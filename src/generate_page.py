from pathlib import Path

from markdown_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    line: str
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()

    raise ValueError("Markdown must contain an h1 heading")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(
        f"Generating page from {from_path} to {dest_path} "
        f"using {template_path}"
    )
    markdown: str = Path(from_path).read_text(encoding="utf-8")
    template: str = Path(template_path).read_text(encoding="utf-8")
    content: str = markdown_to_html_node(markdown).to_html()
    title: str = extract_title(markdown)
    page: str = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    destination: Path = Path(dest_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(page, encoding="utf-8")
