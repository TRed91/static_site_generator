import unittest
from blocktype import BlockType, block_to_block_type

class TestBlockToBlockType(unittest.TestCase):
    def test_is_paragraph(self):
        block = "I'm a paragraph"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_is_heading(self):
        block = "######I'm a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_is_not_valid_heading(self):
        block = "#######I'm a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_is_code(self):
        block = "```for i in range(5):\n    print(i)```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)
    
    def test_is_not_valid_code(self):
        block = "```for i in range(5):\n    print(i)``"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_is_quote(self):
        block = ">I breath\n>so I am\n> >-Dinkelberg"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_is_not_valid_quote(self):
        block = ">I breath\n>so I am not\n >-Dinkelberg"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_is_unordered_list(self):
        block = "- Keyboard\n- Mouse\n- Coffee"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_is_not_valid_unordered_list(self):
        block = "- Keyboard\n- Mouse\n-Whoops"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_is_ordered_list(self):
        block = "1. Wake up\n2. Go to work\n3. Sleep"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_is_not_valid_ordered_list(self):
        block = "1. Wake up\n2. Go to work\n3.Whoops"
        block2 = "1. Wake up\n2. Go to work\n4. I can only count to two"
        block_type = block_to_block_type(block)
        block_type2 = block_to_block_type(block2)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
        self.assertEqual(block_type2, BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()