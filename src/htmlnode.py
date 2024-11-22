class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("The to_html method should be defined by the HTMLNode child classes!")

    def props_to_html(self):
        properties = ""
        if self.props == None:
            return properties

        for prop in self.props:
            properties += f' {prop}="{self.props[prop]}"'
        return properties

    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

