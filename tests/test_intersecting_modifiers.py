from sys import path
path.append('..')

from unittest import TestCase, main
from re_map import process, core, utils

core.__verbose__ = True

class IntersectingModifierTestCase(TestCase):
    def test_intersection_1(self):
        text = 'C AAA C'

        modifiers = [
            ( r'(AAA)',  { 1: 'BBBBB' } ),
            ( r'(C BBBBB C)',  { 1: 'DD' } ),
        ]

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, 'DD' )
        self.assertEqual( span_map, [ ((0, 7), (0, 2)) ] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, '0000000' )
        self.assertEqual( text_processed_decorated, '00' )

    def test_intersection_2(self):
        text = 'C AAA C'

        modifiers = [
            ( r'(AAA)',  { 1: 'BBBBB' } ),
            ( r'(C BBBBB)',  { 1: 'DD' } ),
        ]

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, 'DD C' )
        self.assertEqual( span_map, [ ((0, 5), (0, 2)) ] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, '00000 C' )
        self.assertEqual( text_processed_decorated, '00 C' )

    def test_intersection_3(self):
        text = 'C AAA C'

        modifiers = [
            ( r'(AAA)',  { 1: 'BBBBB' } ),
            ( r'(BBBBB C)',  { 1: 'DD' } ),
        ]

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, 'C DD' )
        self.assertEqual( span_map, [ ((2, 7), (2, 4)) ] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, 'C 00000' )
        self.assertEqual( text_processed_decorated, 'C 00' )

    def test_intersection_4(self):
        text = 'C AAA C'

        modifiers = [
            ( r'(AAA)',  { 1: 'BBEBB' } ),
            ( r'(BBEBB)',  { 1: 'DD' } ),
        ]

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, 'C DD C' )
        self.assertEqual( span_map, [ ((2, 5), (2, 4)) ] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, 'C 000 C' )
        self.assertEqual( text_processed_decorated, 'C 00 C' )

    def test_intersection_5(self):
        text = ' C AAA C '

        modifiers = [
            ( r' (AAA) C',  { 1: 'BBEBB' } ),
            ( r'C (BBEBB)',  { 1: 'DD' } ),
            ( r'(C D)D',  { 1: 'FF' } ),
        ]

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, ' FFD C ' )
        self.assertEqual( span_map, [ ((1, 6), (1, 4)) ] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, ' 00000 C ' )
        self.assertEqual( text_processed_decorated, ' 000 C ' )

    def test_multiple_intersections_1(self):
        text = ' C AAA C D '

        modifiers = [
            ( r'(C) (AAA) (C) (D) ',  { 1: 'GG',  2: 'BB',  3: 'GG',  4: 'DD' } ),
            ( r'( GG BB G)G',  { 1: 'HJK' } ),
            ( r'(HJK)G',  { 1: 'FF' } ),
        ]

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, 'FFG DD ' )
        self.assertEqual( span_map, [ ((0, 8), (0, 3)), ((9, 10), (4, 6)) ] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, '00000000 1 ' )
        self.assertEqual( text_processed_decorated, '000 11 ' )

if __name__ == '__main__':
    main()