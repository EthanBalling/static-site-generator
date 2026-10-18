# from textnode import TextNode, TextType
#
# def main() -> None:
#     node: TextNode = TextNode(
#         "This is some anchor text",
#         TextType.LINK,
#         "https://www.boot.dev",
#     )
#     print(node)
#
# if __name__ == "__main__":
#     print("hello world")
#     main()

import os
import shutil
import sys

from generate_page import generate_pages_recursive


def copy_directory_contents(source: str, destination: str) -> None:
    entries: list[str] = os.listdir(source)

    entry: str
    for entry in entries:
        source_path: str = os.path.join(source, entry)
        destination_path: str = os.path.join(destination, entry)

        if os.path.isfile(source_path):
            print(f"Copying {source_path} -> {destination_path}")
            shutil.copy(source_path, destination_path)

        elif os.path.isdir(source_path):
            os.mkdir(destination_path)
            copy_directory_contents(source_path, destination_path)


def copy_static(source: str, destination: str) -> None:
    source = os.path.realpath(source)
    destination = os.path.realpath(destination)

    if not os.path.isdir(source):
        raise FileNotFoundError(
            f"Source directory does not exist: {source}"
        )

    common_path: str = os.path.commonpath([source, destination])
    if common_path == source or common_path == destination:
        raise ValueError(
            "Source and destination must be separate, "
            "non-nested directories. "
        )

    if os.path.exists(destination):
        print(f"Removing old output: {destination}")
        shutil.rmtree(destination)

    os.mkdir(destination)
    copy_directory_contents(source, destination)


def main() -> None:
    basepath: str = sys.argv[1] if len(sys.argv) > 1 else "/"
    project_root: str = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
    source: str = os.path.join(project_root, "static")
    destination: str = os.path.join(project_root, "docs")

    copy_static(source, destination)
    generate_pages_recursive(
        os.path.join(project_root, "content"),
        os.path.join(project_root, "template.html"),
        destination,
        basepath,
    )


if __name__ == "__main__":
    main()
