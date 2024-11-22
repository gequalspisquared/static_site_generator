import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "This is a text", [], {"href": "https://text.com"})
        self.assertEqual(node.props_to_html(), ' href="https://text.com"')

        node = HTMLNode("a", "This is a text", [], {"href": "https://text.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://text.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode("a", "This is a text", [], {"href": "https://text.com"})
        self.assertEqual(str(node), "HTMLNode(tag=a, value=This is a text, children=[], props={'href': 'https://text.com'})")

if __name__ == "__main__":
    unittest.main()
