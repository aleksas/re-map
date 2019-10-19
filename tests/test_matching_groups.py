from sys import path
path.append('..')

from unittest import TestCase, main
from re_map import Processor

class MatchingGroupTestCase(TestCase):
    '''
    Tests perfect matching match group replacements.
    '''
    def test_matching_1(self):
        text = ' BBB AAA AAA BBB '

        modifiers = [
            ( r'(AAA)',  { 1: 'BBB' } ),
            ( r'(BBB)',  { 1: 'YYY' } ),
        ]

        ref_span_map = [
            ((1, 4), (1, 4)),
            ((5, 8), (5, 8)),
            ((9, 12), (9, 12)),
            ((13, 16), (13, 16))
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, ' YYY YYY YYY YYY ' )
        self.assertEqual( procesor.span_map, ref_span_map )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 000 111 222 333 ' )
        self.assertEqual( decorated_processed_text, ' 000 111 222 333 ' )

    def test_matching_2(self):
        text = ' AAA BBB CCC DDD '

        modifiers = [
            ( r'(AAA) (BBB) (CCC)',  { 1: 'ZZZZ', 2: 'YYYYY', 3: 'XXXXXX' } ),
            ( r'((YYYYY)|(ZZZZ))',  { 1: 'WWWWWW' } ),
            ( r'(WWWWWW)',  { 1: 'QQQQQQQ' } ),
        ]

        ref_span_map = [
            ((1, 4), (1, 8)),
            ((5, 8), (9, 16)),
            ((9, 12), (17, 23))
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, ' QQQQQQQ QQQQQQQ XXXXXX DDD ' )
        self.assertEqual( procesor.span_map, ref_span_map )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_processed_text, ' 0000000 1111111 222222 DDD ' )
        self.assertEqual( decorated_text, ' 000 111 222 DDD ' )

    def test_matching_3(self):
        text = 'AZA'

        modifiers = [
            ( r'(A)',  { 1: 'BB' } ),
            ( r'(BB)',  { 1: 'DD' } )
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, 'DDZDD' )
        self.assertEqual( procesor.span_map, [ ((0, 1), (0, 2)), ((2, 3), (3, 5)) ] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, '0Z1' )
        self.assertEqual( decorated_processed_text, '00Z11' )

    def test_matching_4(self):
        text = ' AAA '

        modifiers = [
            ( r'(AAA)',  { 1: 'BBBBB' } ),
            ( r'(BBBBB)',  { 1: 'CC' } ),
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, ' CC ' )
        self.assertEqual( procesor.span_map, [ ((1, 4), (1, 3)) ] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 000 ' )
        self.assertEqual( decorated_processed_text, ' 00 ' )

    def test_matching_5(self):
        text = ' AAA D '

        modifiers = [
            ( r'(AAA) (D)',  { 1: 'BBBBB', 2: 'EE' } ),
            ( r'(BBBBB)',  { 1: 'CC' } ),
            ( r'(EE)',  { 1: 'FFFF' } ),
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, ' CC FFFF ' )
        self.assertEqual( procesor.span_map, [ ((1, 4), (1, 3)), ((5, 6), (4, 8)) ] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 000 1 ' )
        self.assertEqual( decorated_processed_text, ' 00 1111 ' )

    def test_matching_6(self):
        text = ' AAA D AAA D '

        modifiers = [
            ( r'(AAA) (D)',  { 1: 'BBBBB', 2: 'EE' } ),
            ( r'(BBBBB)',  { 1: 'CC' } ),
            ( r'(EE)',  { 1: 'FFFF' } ),
        ]

        with Processor(text) as procesor:
            for pattern, replacement_map in modifiers:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, ' CC FFFF CC FFFF ' )
        self.assertEqual( procesor.span_map, [ ((1, 4), (1, 3)), ((5, 6), (4, 8)), ((7, 10), (9, 11)), ((11, 12), (12, 16)) ] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 000 1 222 3 ' )
        self.assertEqual( decorated_processed_text, ' 00 1111 22 3333 ' )

if __name__ == '__main__':
    main()