[![Build Status](https://travis-ci.org/aleksas/re-map.svg?branch=master)](https://travis-ci.org/aleksas/re-map)
[![PyPI](https://img.shields.io/pypi/v/re-map?color=success)](https://pypi.org/project/re-map/)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/63e1067e85994870b8f6a39a4ee34ec3)](https://www.codacy.com/manual/aleksas/re-map?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=aleksas/re-map&amp;utm_campaign=Badge_Grade)

# re-map

Package for managing multiple regext pattern replacement change location map.


May be usefull when there is a necesity to have original text, text altered using regex pattern replacements and a map of said replacements.
One scenario where this may proove usefull is machine learning "text2text# problems (e.g. translation, text normalization, etc.).

# install

```bash
$ pip install re-map
```

# example
## Code
```python
from re_map import Processor

numbers = {5: 'five', 8: 'eight', 10: 'ten'}
orginal_numbers = {1: 'first', 2: 'second'}

modifiers = [
    ( r'der (G\.) Be',  { 1: 'Graham'} ),
    ( r' (&) ',  { 1: 'and'} ),
    ( r' (etc)\.',  { 1: 'et cetera'} ),
    ( r' ((\d+)((st)|(nd)|(rd)|(th))) ',  { 2: lambda x: orginal_numbers[int(x)], 3: '' } ),
    ( r' (\d+) ',  { 1: lambda x: numbers[int(x)] } ),
]

text = 'Alexander G. Bell ate 10 apples & 8 cucumbers. The 1st apple was rotten, the 2nd was too, also the third, fourth etc.'

with Processor(text) as procesor:
    for pattern, replacement_map in modifiers:
        procesor.process(pattern, replacement_map)

decorated_text, decorated_processed_text = procesor.decorate()

print (text)
print (decorated_text)
print (procesor.processed_text)
print (decorated_processed_text)
print (span_map)
```

## Output

```shell
Alexander G. Bell ate 10 apples & 8 cucumbers. The 1st apple was rotten, the 2nd was too, also the third, fourth etc.
Alexander 00 Bell ate 11 apples 2 3 cucumbers. The 455 apple was rotten, the 677 was too, also the third, fourth 888.
Alexander Graham Bell ate ten apples and eight cucumbers. The first apple was rotten, the second was too, also the third, fourth et cetera.
Alexander 000000 Bell ate 111 apples 222 33333 cucumbers. The 44444 apple was rotten, the 666666 was too, also the third, fourth 888888888.
[((10, 12), (10, 16)), ((22, 24), (26, 29)), ((32, 33), (37, 40)), ((34, 35), (41, 46)), ((51, 52), (62, 67)), ((52, 54), (67, 67)), ((77, 78), (90, 96)), ((78, 80), (96, 96)), ((113, 116), (129, 138))]
```
