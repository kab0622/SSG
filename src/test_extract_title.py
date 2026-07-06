import unittest
from extract_title import extract_title

class TestExtract(unittest.TestCase):
    def test_extract_title(self):
        markdown = "Hello"
        markdown2 = extract_title("# Hello")
        self.assertEqual(markdown, markdown2)

if __name__ == "__main__":
    unittest.main()