class HTMLNode:
    def __init__(
        self, tag: str | None = None, value: str | None = None,
        children: list[HTMLNode] | None = None, props: dict[str, str] | None = None,
    ) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.props: dict[str, str] | None = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if not self.props:
            return ""

        return "".join(
            f' {key}="{value}"' for key, value in self.props.items()
        )

    def __repr__(self) -> str:
        return (
            f"HTMLNode(tag={self.tag!r}, value={self.value!r}, "
            f" children={self.children!r}, props={self.props!r})"
        )


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str | None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            tag=tag,
            value=value,
            children=None,
            props=props
        )

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        return (
            f"<{self.tag}{self.props_to_html()}>"
            f"{self.value}"
            f"</{self.tag}>"
        )

    def __repr__(self) -> str:
        return (
            f"LeafNode(tag={self.tag!r}, "
            f"value={self.value!r}, props={self.props!r})"
        )

class ParentNode(HTMLNode):
    def __init__(
        self, tag: str | None, children: list[HTMLNode] | None,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            tag=tag,
            value=None,
            children=children,
            props=props
        )

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")

        children_html = "".join(
            child.to_html() for child in self.children
        )

        return (
            f"<{self.tag}{self.props_to_html()}>"
            f"{children_html}"
            f"</{self.tag}>"
        )

    def __repr__(self) -> str:
        return (
            f"ParentNode(tag={self.tag!r}, "
            f"children={self.children!r}, props={self.props!r})"
        )
