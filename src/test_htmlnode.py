import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode("a", "click", None, {"href": "https://example.com"})
        node2 = ' href="https://example.com"'
        self.assertEqual(node.props_to_html(), node2)
    
    def test_repr(self):
        node = HTMLNode("a", "value", ["x", "y"], {"href": "https://www.google.com"})
        node2 = "HTMLNode(a, value, ['x', 'y'], {'href': 'https://www.google.com'})"
        self.assertEqual(repr(node), node2)

    def test_short_repr(self):
        node = HTMLNode("a", "value", ["x", "y"])
        node2 = "HTMLNode(a, value, ['x', 'y'], None)"
        self.assertEqual(repr(node), node2)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_mul_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("b", "child")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b>child</b></div>")

    def test_to_html_with_no_children(self):
        with self.assertRaises(ValueError):
            parent_node = ParentNode("div", None)
            parent_node.to_html()


if __name__ == "__main__":
    unittest.main()