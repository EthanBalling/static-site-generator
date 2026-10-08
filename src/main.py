from textnode import TextNode, TextType

def main() -> None:
    node: TextNode = TextNode(
        "This is some anchor text",
        TextType.LINK,
        "https://www.boot.dev",
    )
    print(node)

if __name__ == "__main__":
    print("hello world")
    main()
