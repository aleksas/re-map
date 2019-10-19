from sys import path
path.append('..')

from unittest import TestCase, main
from re_map import Processor

class IntersectingGroupTestCase(TestCase):
    def test_intersection_1(self):
        text = 'C AAA C'

        modifiers = [
            ( r'(AAA)',  { 1: 'BBBBB' } ),
            ( r'(C BBBBB C)',  { 1: 'DD' } ),
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'DD' )
        self.assertEqual( procesor.span_map, [ ((0, 7), (0, 2)) ] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, '0000000' )
        self.assertEqual( decorated_processed_text, '00' )

    def test_intersection_2(self):
        text = 'C AAA C'

        modifiers = [
            ( r'(AAA)',  { 1: 'BBBBB' } ),
            ( r'(C BBBBB)',  { 1: 'DD' } ),
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'DD C' )
        self.assertEqual( procesor.span_map, [ ((0, 5), (0, 2)) ] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, '00000 C' )
        self.assertEqual( decorated_processed_text, '00 C' )

    def test_intersection_3(self):
        text = 'C AAA C'

        modifiers = [
            ( r'(AAA)',  { 1: 'BBBBB' } ),
            ( r'(BBBBB C)',  { 1: 'DD' } ),
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'C DD' )
        self.assertEqual( procesor.span_map, [ ((2, 7), (2, 4)) ] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, 'C 00000' )
        self.assertEqual( decorated_processed_text, 'C 00' )

    def test_intersection_4(self):
        text = 'C AAA C'

        modifiers = [
            ( r'(AAA)',  { 1: 'BBEBB' } ),
            ( r'(BBEBB)',  { 1: 'DD' } ),
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'C DD C' )
        self.assertEqual( procesor.span_map, [ ((2, 5), (2, 4)) ] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, 'C 000 C' )
        self.assertEqual( decorated_processed_text, 'C 00 C' )

    def test_intersection_5(self):
        text = ' C AAA C '

        modifiers = [
            ( r' (AAA) C',  { 1: 'BBEBB' } ),
            ( r'C (BBEBB)',  { 1: 'DD' } ),
            ( r'(C D)D',  { 1: 'FF' } ),
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, ' FFD C ' )
        self.assertEqual( procesor.span_map, [ ((1, 6), (1, 4)) ] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 00000 C ' )
        self.assertEqual( decorated_processed_text, ' 000 C ' )

    def test_intersection_6(self):
        modifiers = [
            ( r' (AAA)B',  { 1: 'CCC CCC'} ),
            ( r'(CCCB)',  { 1: lambda x: x } ),
        ]

        text = ' AAAB'

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, ' CCC CCCB' )
        self.assertEqual( procesor.span_map, [((1, 5), (1, 9))] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 0000' )
        self.assertEqual( decorated_processed_text, ' 00000000' )

    def test_intersection_7(self):
        modifiers = [
            ( r'B(AAA) ',  { 1: 'CCC CCC'} ),
            ( r'(BCCC)',  { 1: lambda x: x } ),
        ]

        text = 'BAAA '

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'BCCC CCC ' )
        self.assertEqual( procesor.span_map, [((0, 4), (0, 8))] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, '0000 ' )
        self.assertEqual( decorated_processed_text, '00000000 ' )

    def test_multiple_intersections_1(self):
        text = ' C AAA C D '

        modifiers = [
            ( r'(C) (AAA) (C) (D) ',  { 1: 'GG',  2: 'BB',  3: 'GG',  4: 'DD' } ),
            ( r'( GG BB G)G',  { 1: 'HJK' } ),
            ( r'(HJK)G',  { 1: 'FF' } ),
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'FFG DD ' )
        self.assertEqual( procesor.span_map, [ ((0, 8), (0, 3)), ((9, 10), (4, 6)) ] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, '00000000 1 ' )
        self.assertEqual( decorated_processed_text, '000 11 ' )


    def test_new(self):
        modifiers = [
            ( r' (etc)\.',  { 1: 'et cetera'} ),
            ( r'([^ ]+)',  { 1: lambda x: x } ),
        ]

        text = ' etc.'

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, ' et cetera.' )
        self.assertEqual( procesor.span_map, [ ((1, 5), (1, 11)) ] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 0000' )
        self.assertEqual( decorated_processed_text, ' 0000000000' )

if __name__ == '__main__':
    main()