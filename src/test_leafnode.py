import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is paragraph text")
        self.assertEqual(node.to_html(), '<p>This is paragraph text</p>')

        node = LeafNode("a", "This is text", {"href": "https://text.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://text.com" target="_blank">This is text</a>')

    def test_repr(self):
        node = LeafNode("a", "This is a text", {"href": "https://text.com"})
        self.assertEqual(str(node), "LeafNode(tag=a, value=This is a text, props={'href': 'https://text.com'})")

if __name__ == "__main__":
    unittest.main()

