from sys import path
path.append('..')

from unittest import TestCase, main
from re_map import Processor

class SingleModifierTestCase(TestCase):
    def test_single_1(self):
        text = 'ABAB'
        pattern, replacement_map = r'(A)(B)',  { 1: 'CC', 2:'D'}

        with Processor(text) as procesor:
            procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'CCDCCD' )
        self.assertEqual( procesor.span_map, [((0, 1), (0, 2)), ((1, 2), (2, 3)), ((2, 3), (3, 5)), ((3, 4), (5, 6))] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, '0123' )
        self.assertEqual( decorated_processed_text, '001223' )

    def test_single_2(self):
        text = 'AABAAB'
        pattern, replacement_map = r'(AA)(B)',  { 1: 'C', 2:'D'}

        with Processor(text) as procesor:
            procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'CDCD' )
        self.assertEqual( procesor.span_map, [((0, 2), (0, 1)), ((2, 3), (1, 2)), ((3, 5), (2, 3)), ((5, 6), (3, 4))] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, '001223' )
        self.assertEqual( decorated_processed_text, '0123' )

    def test_single_3(self):
        text = 'ABBABB'
        pattern, replacement_map = r'(A)(BB)',  { 1: 'CC', 2:'D'}

        with Processor(text) as procesor:
            procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'CCDCCD' )
        self.assertEqual( procesor.span_map, [((0, 1), (0, 2)), ((1, 3), (2, 3)), ((3, 4), (3, 5)), ((4, 6), (5, 6))] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, '011233' )
        self.assertEqual( decorated_processed_text, '001223' )

if __name__ == '__main__':
    main()