from sys import path
path.append('..')

from unittest import TestCase, main
from re_map import process, utils

class BundledModifierTestCase(TestCase):
    def test_a(self):
        text = 'ABAB'
        modifiers = [
            ( r'(A)',  { 1: 'CC'} ),
            ( r'(B)',  { 1: 'D'} )
        ]

        processed_text, span_map = process(text, modifiers)
        self.assertEqual( processed_text, 'CCDCCD' )
        self.assertEqual( span_map, [((0, 1), (0, 2)), ((1, 2), (2, 3)), ((2, 3), (3, 5)), ((3, 4), (5, 6))] )

        decorated_text, decorated_processed_text = utils.decorate(text, processed_text, span_map)

        self.assertEqual( decorated_text, '0123' )
        self.assertEqual( decorated_processed_text, '001223' )

    def test_b(self):
        text = 'AABAAB'
        modifiers = [
            ( r'(AA)',  { 1: 'C'} ),
            ( r'(B)',  { 1:'D'} )
        ]

        processed_text, span_map = process(text, modifiers)
        self.assertEqual( processed_text, 'CDCD' )
        self.assertEqual( span_map, [((0, 2), (0, 1)), ((2, 3), (1, 2)), ((3, 5), (2, 3)), ((5, 6), (3, 4))] )

        decorated_text, decorated_processed_text = utils.decorate(text, processed_text, span_map)

        self.assertEqual( decorated_text, '001223' )
        self.assertEqual( decorated_processed_text, '0123' )

    def test_c(self):
        text = 'ABBABB'
        modifiers = [
            ( r'(A)',  { 1: 'CC'} ),
            ( r'(BB)',  { 1:'D'} )
        ]

        processed_text, span_map = process(text, modifiers)
        self.assertEqual( processed_text, 'CCDCCD' )
        self.assertEqual( span_map, [((0, 1), (0, 2)), ((1, 3), (2, 3)), ((3, 4), (3, 5)), ((4, 6), (5, 6))] )

        decorated_text, decorated_processed_text = utils.decorate(text, processed_text, span_map)

        self.assertEqual( decorated_text, '011233' )
        self.assertEqual( decorated_processed_text, '001223' )

    def test_empty(self):
        text = 'BAAB'

        modifiers = [
            ( r'(AA)',  { 1: 'CC'} ),
            ( r'(B)',  { 1:''} )
        ]

        processed_text, span_map = process(text, modifiers)
        self.assertEqual( processed_text, 'CC' )
        self.assertEqual( span_map, [((0, 1), (0, 0)), ((1, 3), (0, 2)), ((3, 4), (2, 2))] )

        decorated_text, decorated_processed_text = utils.decorate(text, processed_text, span_map)

        self.assertEqual( decorated_text, '0112' )
        self.assertEqual( decorated_processed_text, '11' )

if __name__ == '__main__':
    main()