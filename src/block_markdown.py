def markdown_to_blocks(markdown: str) -> list[str]:
    blocks: list[str] = []
    candidates: list[str] = markdown.split("\n\n")

    candidate: str
    for candidate in candidates:
        block: str = candidate.strip()

        if block != "":
            blocks.append(block)

    return blocks
