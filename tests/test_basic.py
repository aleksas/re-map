import unittest
from re_map import process, core

core.__verbose__ = True

class BasicTest(unittest.TestCase):
    text_0 = ' AAA BBB CCC DDD '
    text_1 = ' AAA BBB AAA BBB '
    text_2 = ' BBB AAA AAA BBB '
    text_3 = ' AAA AAA AAA AAA '

    modifiers_0 = [ 
        ( r'(AAA)',  { 1: 'ZZZ' } ),
        ( r'(BBB)',  { 1: 'YYY' } ),
        ( r'(CCC)',  { 1: 'XXX' } ),
        ( r'(DDD)',  { 1: 'WWW' } )
    ]

    modifiers_1 = [ 
        ( r'(AAA)',  { 1: 'BBB' } ),
    ]

    modifiers_2 = [ 
        ( r'(AAA)',  { 1: 'BBB' } ),
        ( r'(BBB)',  { 1: 'YYY' } ),
    ]

    change_map = [ 
        ((1, 4), (1, 4)), 
        ((5, 8), (5, 8)), 
        ((9, 12), (9, 12)),
        ((13, 16), (13, 16))
    ]

    change_map_1_1 = [
        ((1, 4), (1, 4)), 
        ((9, 12), (9, 12))
    ]

    def test_0(self):
        text = str(self.text_0)
        text_modified, change_map = process(text, self.modifiers_0)
        self.assertEqual( text_modified, ' ZZZ YYY XXX WWW ' )
        self.assertEqual( change_map, self.change_map )

    def test_1(self):
        text = str(self.text_1)
        text_modified, change_map = process(text, self.modifiers_0)
        self.assertEqual( text_modified, ' ZZZ YYY ZZZ YYY ' )
        self.assertEqual( change_map, self.change_map )

    def test_2a(self):
        text = str(self.text_1)
        text_modified, change_map = process(text, self.modifiers_1)

        self.assertEqual( text_modified, ' BBB BBB BBB BBB ' )
        self.assertEqual( change_map, self.change_map_1_1 )

    def test_2b(self):
        text = str(self.text_3)
        text_modified, change_map = process(text, self.modifiers_1)

        self.assertEqual( text_modified, ' BBB BBB BBB BBB ' )
        self.assertEqual( change_map, self.change_map )

    def test_3(self):
        text = str(self.text_2)
        text_modified, change_map = process(text, self.modifiers_0)
        self.assertEqual( text_modified, ' YYY ZZZ ZZZ YYY ' )
        self.assertEqual( change_map, self.change_map )

    def test_chain(self):
        text = str(self.text_2)
        text_modified, change_map = process(text, self.modifiers_2)

        self.assertEqual( text_modified, ' YYY YYY YYY YYY ' )
        self.assertEqual( change_map, self.change_map )