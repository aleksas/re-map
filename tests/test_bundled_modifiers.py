from sys import path
path.append('..')

from unittest import TestCase, main
from re_map import Processor

class BundledModifiersTestCase(TestCase):
    def test_bundled_1(self):
        text = 'ABAB'
        modifiers = [
            ( r'(A)',  { 1: 'CC'} ),
            ( r'(B)',  { 1: 'D'} )
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'CCDCCD' )
        self.assertEqual( procesor.span_map, [((0, 1), (0, 2)), ((1, 2), (2, 3)), ((2, 3), (3, 5)), ((3, 4), (5, 6))] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, '0123' )
        self.assertEqual( decorated_processed_text, '001223' )

    def test_bundled_2(self):
        text = 'AABAAB'
        modifiers = [
            ( r'(AA)',  { 1: 'C'} ),
            ( r'(B)',  { 1:'D'} )
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'CDCD' )
        self.assertEqual( procesor.span_map, [((0, 2), (0, 1)), ((2, 3), (1, 2)), ((3, 5), (2, 3)), ((5, 6), (3, 4))] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, '001223' )
        self.assertEqual( decorated_processed_text, '0123' )

    def test_bundled_3(self):
        text = 'ABBABB'
        modifiers = [
            ( r'(A)',  { 1: 'CC'} ),
            ( r'(BB)',  { 1:'D'} )
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'CCDCCD' )
        self.assertEqual( procesor.span_map, [((0, 1), (0, 2)), ((1, 3), (2, 3)), ((3, 4), (3, 5)), ((4, 6), (5, 6))] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, '011233' )
        self.assertEqual( decorated_processed_text, '001223' )

    def test_bundled_4(self):
        text = 'BAAB'

        modifiers = [
            ( r'(AA)',  { 1: 'CC'} ),
            ( r'(B)',  { 1:''} )
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'CC' )
        self.assertEqual( procesor.span_map, [((0, 1), (0, 0)), ((1, 3), (0, 2)), ((3, 4), (2, 2))] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, '0112' )
        self.assertEqual( decorated_processed_text, '11' )

if __name__ == '__main__':
    main()