from sys import path
path.append('..')

from unittest import TestCase, main
from re_map import process, utils

class MultipleModifierTestCase(TestCase):
    def test_a(self):
        text = 'ABAB'
        modifiers = [
            ( r'(A)',  { 1: 'CC'} ),
            ( r'(B)',  { 1: 'D'} )
        ]

        text_processed, span_map = process(text, modifiers)
        self.assertEqual( text_processed, 'CCDCCD' )
        self.assertEqual( span_map, [((0, 1), (0, 2)), ((1, 2), (2, 3)), ((2, 3), (3, 5)), ((3, 4), (5, 6))] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, '0123' )
        self.assertEqual( text_processed_decorated, '001223' )

    def test_b(self):
        text = 'AABAAB'
        modifiers = [
            ( r'(AA)',  { 1: 'C'} ),
            ( r'(B)',  { 1:'D'} )
        ]

        text_processed, span_map = process(text, modifiers)
        self.assertEqual( text_processed, 'CDCD' )
        self.assertEqual( span_map, [((0, 2), (0, 1)), ((2, 3), (1, 2)), ((3, 5), (2, 3)), ((5, 6), (3, 4))] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, '001223' )
        self.assertEqual( text_processed_decorated, '0123' )

    def test_c(self):
        text = 'ABBABB'
        modifiers = [
            ( r'(A)',  { 1: 'CC'} ),
            ( r'(BB)',  { 1:'D'} )
        ]

        text_processed, span_map = process(text, modifiers)
        self.assertEqual( text_processed, 'CCDCCD' )
        self.assertEqual( span_map, [((0, 1), (0, 2)), ((1, 3), (2, 3)), ((3, 4), (3, 5)), ((4, 6), (5, 6))] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, '011233' )
        self.assertEqual( text_processed_decorated, '001223' )

if __name__ == '__main__':
    tc = MultipleModifierTestCase()
    tc.test_b()
    main()