import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

        node2 = ParentNode(
            "a",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("a", "imagetext", {"href": "image.png"}),
                node
            ],
            {"href": "https://text.com"}
        )
        self.assertEqual(node2.to_html(), f'<a href="https://text.com"><b>Bold text</b>Normal text<a href="image.png">imagetext</a>{node.to_html()}</a>')

        with self.assertRaises(ValueError):
            ParentNode(None, node).to_html()

        with self.assertRaises(ValueError):
            ParentNode("p", None).to_html()

    def test_repr(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        children = f'{node.children[0]}, {node.children[1]}, {node.children[2]}, {node.children[3]}'
        self.assertEqual(str(node), f'ParentNode(tag=p, children=[{children}], props=None)')

if __name__ == "__main__":
    unittest.main()
