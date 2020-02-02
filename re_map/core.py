import re
from math import ceil, floor
from json import dump, load
from .utils import decorate
from .slow import intersect, intersection, span_len_delta, span_length, span_rtrim

def span_offset(span, replacement_span_map, delta_start=0, delta_end=0, delta_i=0):
    cached_delta_start = 0
    cached_delta_end = 0
    cached_delta_count = 0
    for span_source, span_target, _ in replacement_span_map[delta_i:]:
        if span_target[1] <= span[0]:
            d = span_len_delta(span_target, span_source)
            delta_start += d
            delta_end += d
            cached_delta_start = delta_start
            cached_delta_end = delta_end
            cached_delta_count += 1
        else:
            target_trimmed_end = span_rtrim(span_target, span[1])
            if target_trimmed_end:
                d = span_len_delta(span_target, span_source)
                # int() and 1.0 multipliers for 2.7 compatibility
                ratio_end = 1.0 * span_length(target_trimmed_end) / span_length(span_target)
                delta_end += int(floor(d * ratio_end))

                target_trimmed_start = span_rtrim(span_target, span[0])
                if target_trimmed_start:
                    ratio_start = 1.0 * span_length(target_trimmed_start) / span_length(span_target)
                    delta_start += int(ceil(d * ratio_start))
            else:
                break

    return delta_start, delta_end, cached_delta_start, cached_delta_end, delta_i + cached_delta_count

def insert(entry, replacement_span_map, allow_intersect=True, offset=0):
    i = 0
    for source_span, target_span, _ in replacement_span_map[offset:]:
        if ((source_span[0] >= entry[0][1] or source_span[0] >= entry[0][0]) or
            (target_span[0] >= entry[1][1] or target_span[0] >= entry[1][0]) or
            (intersect(source_span, entry[0])) or
            (intersect(target_span, entry[1]))):
            break
        i+=1

    merge_entries = []
    for e in replacement_span_map[offset:]:
        source_span, target_span, _ = e
        if source_span[0] >= entry[0][1] and target_span[0] >= entry[1][1]:
            break
        if intersect(source_span, entry[0]):
            if not allow_intersect:
                raise ValueError("Intersecting groups not allowed.")
            merge_entries.append(e)

    if merge_entries:
        entry_source_length = span_length(entry[0])
        entry_target_length = span_length(entry[1])
        source_length, target_length = 0, 0
        source_span_start, target_span_start = entry[0][0], entry[1][0]

        aligned_entry_target_span = (entry[1][0], entry[1][1] - entry[2])
        for e in merge_entries:
            source_intersection = intersection(e[0], entry[0])
            entry_source_length -= span_length(source_intersection) if source_intersection else 0
            target_intersection = intersection(e[1], aligned_entry_target_span)
            entry_target_length -= span_length(target_intersection) if target_intersection else 0
            source_length += span_length(e[0])
            target_length += span_length(e[1])
            source_span_start = min(source_span_start, e[0][0])
            target_span_start = min(target_span_start, e[1][0])

        source_span = (source_span_start, source_span_start + source_length + entry_source_length)
        target_span = (target_span_start, target_span_start + target_length + entry_target_length)

        entry = source_span, (target_span[0], target_span[1]), entry[2]

        for e in merge_entries:
            replacement_span_map.remove(e)

    replacement_span_map.insert(offset + i, entry)

    for j, (source_span, target_span, len_delta) in enumerate(replacement_span_map[i+offset+1:]):
        replacement_span_map[i + offset + 1 + j] = source_span, (target_span[0] + entry[2], target_span[1] + entry[2]), len_delta

    return i + offset

def repl(match, replacement_map, replacement_map_keys, replacement_span_map, cache, exceptions):
    match_string = match.group()

    if exceptions:
        for exception in exceptions:
            if isinstance(exception, tuple):
                pattern, replacement = exception 
            else: # str
                 pattern, replacement = exception, exception 
                 
            if re.match(pattern, match_string):
                return replacement

    match_start = match.span(0)[0]
    if len(match.regs) == 1:
        raise Exception('No match groups in regex pattern.')
    _, delta_end, c_delta_start, c_delta_end, c_delta_i = span_offset(match.span(1), replacement_span_map, cache['offset'][0], cache['offset'][1], cache['offset'][2])
    cache['offset'] = (c_delta_start, c_delta_end, c_delta_i)

    current_match_delta = 0

    for i in replacement_map_keys:
        span = match.span(i)
        group_rel_span = span[0] - match_start, span[1] - match_start

        replacement = replacement_map[i] if isinstance(replacement_map[i], str) else replacement_map[i](match.group(i))
        match_string = match_string[0:group_rel_span[0] + current_match_delta] + replacement + match_string[group_rel_span[1] + current_match_delta:]

        match_delta = delta_end + current_match_delta
        group_rel_span_alligned = group_rel_span[0] + match_delta, group_rel_span[1] + match_delta

        span_target = group_rel_span_alligned[0] + match_start, group_rel_span_alligned[0] + len(replacement) + match_start

        new_entry = span, span_target, span_len_delta(span_target, span)

        cache['insert'] = insert(new_entry, replacement_span_map, allow_intersect=False, offset=cache['insert'])
        current_match_delta += new_entry[2]

    return match_string

def normalize_source_spans(replacement_span_map, tmp_replacement_span_map):
    '''
    Corrects the source spans according to earlier length changes
    '''
    cached_delta_start = 0
    cached_delta_end = 0
    delta_i = 0
    for i, (tmp_source_span, _, len_delta) in enumerate(tmp_replacement_span_map):
        delta_start, delta_end, cached_delta_start, cached_delta_end, delta_i = span_offset(tmp_source_span, replacement_span_map, cached_delta_start, cached_delta_end, delta_i)
        tmp_replacement_span_map[i] = (tmp_source_span[0] - delta_start, tmp_source_span[1] - delta_end), tmp_replacement_span_map[i][1], len_delta

def init_replacement_span_map(replacement_span_map):
    new_span_map = []
    new_replacement_span_map = []
    if replacement_span_map:
        for source_span, target_span in replacement_span_map:
            entry =  (tuple(source_span), tuple(target_span), span_len_delta(target_span, source_span))
            new_replacement_span_map.append( entry )
            new_span_map.append( entry[:2] )
    return new_replacement_span_map, new_span_map

class Processor:
    def __init__(self, text, processed_text=None, replacement_span_map=None):
        self.__processing = False
        self.__text = (text + '.')[:-1]
        self.__processed_text = (processed_text + '.')[:-1] if processed_text else (text + '.')[:-1]
        self.__replacement_span_map, self.__span_map = init_replacement_span_map(replacement_span_map)

    def process(self, pattern, replacement_map, count=0, flags=0, exceptions=None):
        if not self.__processing:
            raise Exception("Processing session not initiated")

        tmp_replacement_span_map = []
        cache = {'insert':0, 'offset':(0,0,0)}

        replacement_map_keys = sorted(replacement_map.keys())
        self.__processed_text = re.sub(
            pattern = pattern,
            repl = lambda match: repl(match, replacement_map, replacement_map_keys, tmp_replacement_span_map, cache, exceptions),
            string = self.__processed_text,
            count=count,
            flags = flags
        )

        normalize_source_spans(self.__replacement_span_map, tmp_replacement_span_map)

        offset = 0
        for entry in tmp_replacement_span_map:
            offset = insert(entry, self.__replacement_span_map, offset=offset)

    def swap(self):
        self.__replacement_span_map = [(destination, source, -delta) for source, destination, delta in self.__replacement_span_map]

        tmp = self.__text
        self.__text = self.__processed_text
        self.__processed_text = tmp

    def decorate(self):
        return decorate(self.__text, self.__processed_text, self.span_map)

    @staticmethod
    def load(fp):
        state = load(fp)
        return Processor(state['text'], state['processed_text'], state['span_map'])

    def save(self, fp):
        if self.__processing:
            raise Exception("Saving state in processing mode not allowed")

        state = {
            'text': self.text,
            'processed_text': self.processed_text,
            'span_map': self.span_map
        }

        dump(state, fp)

    @property
    def span_map(self):
        return self.__span_map

    @property
    def text(self):
        return self.__text

    @property
    def processed_text(self):
        return self.__processed_text

    def __enter__(self):
        if self.__processing:
            raise Exception("Already processing.")
        self.__processing = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__processing = False
        self.__span_map = [(src, dst) for src, dst, _ in self.__replacement_span_map]