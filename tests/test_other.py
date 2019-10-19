# -*- coding: utf-8 -*-

from sys import path
path.append('..')

from unittest import TestCase, main
from re_map import Processor

class OtherTestCase(TestCase):
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

    modifiers_3 = [
        ( r'(AAA) (BBB)',  { 1: 'CCC', 2: 'CCC' } ),
        ( r'(DDD)',  { 1: 'CCC' } ),
    ]

    modifiers_4 = [
        ( r'(AAA) (BBB) (CCC)',  { 1: 'CCCC', 2: 'CCCC', 3: 'CCCC' } ),
        ( r'(DDD)',  { 1: 'CCCC' } ),
    ]

    span_map = [
        ((1, 4), (1, 4)),
        ((5, 8), (5, 8)),
        ((9, 12), (9, 12)),
        ((13, 16), (13, 16))
    ]

    span_map_1_1 = [
        ((1, 4), (1, 4)),
        ((9, 12), (9, 12))
    ]

    span_map_2 = [
        ((1, 4), (1, 4)),
        ((5, 8), (5, 8)),
        ((13, 16), (13, 16))
    ]

    span_map_3 = [
        ((1, 4), (1, 5)),
        ((5, 8), (6, 10)),
        ((9, 12), (11, 15)),
        ((13, 16), (16, 20))
    ]

    def test_0(self):
        with Processor(self.text_0) as procesor:
            for pattern, replacement_map in self.modifiers_0:
                procesor.process(pattern, replacement_map)
                
        self.assertEqual( procesor.processed_text, ' ZZZ YYY XXX WWW ' )
        self.assertEqual( procesor.span_map, self.span_map )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 000 111 222 333 ' )
        self.assertEqual( decorated_processed_text, ' 000 111 222 333 ' )

    def test_1(self):
        with Processor(self.text_1) as procesor:
            for pattern, replacement_map in self.modifiers_0:
                procesor.process(pattern, replacement_map)
                
        self.assertEqual( procesor.processed_text, ' ZZZ YYY ZZZ YYY ' )
        self.assertEqual( procesor.span_map, self.span_map )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 000 111 222 333 ' )
        self.assertEqual( decorated_processed_text, ' 000 111 222 333 ' )

    def test_2(self):
        with Processor(self.text_1) as procesor:
            for pattern, replacement_map in self.modifiers_1:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, ' BBB BBB BBB BBB ' )
        self.assertEqual( procesor.span_map, self.span_map_1_1 )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 000 BBB 111 BBB ' )
        self.assertEqual( decorated_processed_text, ' 000 BBB 111 BBB ' )

    def test_3(self):
        with Processor(self.text_3) as procesor:
            for pattern, replacement_map in self.modifiers_1:
                procesor.process(pattern, replacement_map)

        self.assertEqual( procesor.processed_text, ' BBB BBB BBB BBB ' )
        self.assertEqual( procesor.span_map, self.span_map )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 000 111 222 333 ' )
        self.assertEqual( decorated_processed_text, ' 000 111 222 333 ' )

    def test_4(self):
        with Processor(self.text_2) as procesor:
            for pattern, replacement_map in self.modifiers_0:
                procesor.process(pattern, replacement_map)
                
        self.assertEqual( procesor.processed_text, ' YYY ZZZ ZZZ YYY ' )
        self.assertEqual( procesor.span_map, self.span_map )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 000 111 222 333 ' )
        self.assertEqual( decorated_processed_text, ' 000 111 222 333 ' )

    def test_5(self):
        with Processor(self.text_0) as procesor:
            for pattern, replacement_map in self.modifiers_3:
                procesor.process(pattern, replacement_map)
                
        self.assertEqual( procesor.processed_text, ' CCC CCC CCC CCC ' )
        self.assertEqual( procesor.span_map, self.span_map_2 )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 000 111 CCC 222 ' )
        self.assertEqual( decorated_processed_text, ' 000 111 CCC 222 ' )

    def test_6(self):
        with Processor(self.text_0) as procesor:
            for pattern, replacement_map in self.modifiers_4:
                procesor.process(pattern, replacement_map)
                
        self.assertEqual( procesor.processed_text, ' CCCC CCCC CCCC CCCC ' )
        self.assertEqual( procesor.span_map, self.span_map_3 )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, ' 000 111 222 333 ' )
        self.assertEqual( decorated_processed_text, ' 0000 1111 2222 3333 ' )

    def test_7(self):
        text = 'ab'
        pattern, replacement_map = r'((a)(b))', { 1: 'c', 2:'d', 3:'e'}

        with self.assertRaises(ValueError):
            with Processor(text) as procesor:
                procesor.process(pattern, replacement_map)

    def test_9(self):
        text = 'AA BBBB& CC&CCCC'

        pattern_1, replacement_map_1 = r'([A-Za-z&]+)',  { 1: lambda x: x.replace('&', '') }
        pattern_2, replacement_map_2 = r'(AA) ',  { 1: 'DDD DDD' }

        with Processor(text) as procesor:
            procesor.process(pattern_1, replacement_map_1)            
            procesor.swap()
            procesor.process(pattern_2, replacement_map_2)

        self.assertEqual( procesor.text, 'AA BBBB CCCCCC' )
        self.assertEqual( procesor.processed_text, 'DDD DDD BBBB& CC&CCCC' )
        self.assertEqual( procesor.span_map, [((0, 2), (0, 7)), ((3, 7), (8, 13)), ((8, 14), (14, 21)) ] )

        decorated_text, decorated_processed_text = procesor.decorate()

        self.assertEqual( decorated_text, '00 1111 222222' )
        self.assertEqual( decorated_processed_text, '0000000 11111 2222222' )

if __name__ == '__main__':
    main()