from sys import path
path.append('..')

from unittest import TestCase, main
from re_map import process, core, utils

core.__verbose__ = True

class ChainModifierTestCase(TestCase):
    def test_chain_1(self):
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

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, ' YYY YYY YYY YYY ' )
        self.assertEqual( span_map, ref_span_map )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, ' 000 111 222 333 ' )
        self.assertEqual( text_processed_decorated, ' 000 111 222 333 ' )

    def test_chain_2(self):
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

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, ' QQQQQQQ QQQQQQQ XXXXXX DDD ' )
        self.assertEqual( span_map, ref_span_map )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_processed_decorated, ' 0000000 1111111 222222 DDD ' )
        self.assertEqual( text_decorated, ' 000 111 222 DDD ' )

    def test_chain_3(self):
        text = 'AZA'

        modifiers = [
            ( r'(A)',  { 1: 'BB' } ),
            ( r'(BB)',  { 1: 'DD' } )
        ]

        text_processed, span_map = process(text, modifiers)

        self.assertEqual( text_processed, 'DDZDD' )
        self.assertEqual( span_map, [ ((0, 1), (0, 2)), ((2, 3), (3, 5)) ] )

        text_decorated, text_processed_decorated = utils.decorate(text, text_processed, span_map)

        self.assertEqual( text_decorated, '0Z1' )
        self.assertEqual( text_processed_decorated, '00Z11' )


if __name__ == '__main__':
    main()