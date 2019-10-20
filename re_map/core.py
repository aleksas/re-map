import re
from math import ceil, floor
from .utils import decorate
from .fast import intersect, span_len_delta, span_length, span_rtrim

def span_offset(span, replacement_span_map):
    delta_start, delta_end = 0, 0
    for span_source, span_target, _ in replacement_span_map:
        d = span_len_delta(span_target, span_source)
        if span_target[1] <= span[0]:
            delta_end += d
            delta_start += d
        else:
            target_trimmed_start = span_rtrim(span_target, span[0])
            target_trimmed_end = span_rtrim(span_target, span[1])

            if target_trimmed_end:
                # int() and 1.0 multipliers for 2.7 compatibility
                ratio_end = 1.0 * span_length(target_trimmed_end) / span_length(span_target)
                delta_end += int(floor(d * ratio_end))
                if target_trimmed_start:
                    ratio_start = 1.0 * span_length(target_trimmed_start) / span_length(span_target)
                    delta_start += int(ceil(d * ratio_start))
            else:
                break

    return delta_start, delta_end

def insert(entry, replacement_span_map, allow_intersect=True):
    def validate(source_span, ref_source_span):
        if intersect(ref_source_span, source_span):
            raise Exception("Illegal span intersection")

    intersecting = []

    i = 0
    for i, (source_span, target_span, _) in enumerate(replacement_span_map):
        if (
            (source_span[0] >= entry[0][1] or source_span[0] >= entry[0][0]) or
            (target_span[0] >= entry[1][1] or target_span[0] >= entry[1][0]) or
            (intersect(source_span, entry[0])) or
            (intersect(target_span, entry[1]))
            ):
            break
        i+=1

    for j in range(i, len(replacement_span_map)):
        source_span, target_span, _ = replacement_span_map[j]
        if source_span[0] >= entry[0][1] and target_span[0] >= entry[1][1]:
            break
        if intersect(source_span, entry[0]):
            intersecting.append(j)
            if not allow_intersect:
                raise ValueError("Intersecting groups not allowed.")

    if len(intersecting):
        entry_source_length = span_length(entry[0])
        entry_target_length = span_length(entry[1])
        source_length, target_length = 0, 0
        source_span_start, target_span_start = entry[0][0], entry[1][0]

        merge_entries = [replacement_span_map[k] for k in intersecting]

        aligned_entry_target_span = (entry[1][0], entry[1][1] - entry[2])
        for e in merge_entries:
            source_intersection = intersect(e[0], entry[0])
            entry_source_length -= span_length(source_intersection) if source_intersection else 0
            target_intersection = intersect(e[1], aligned_entry_target_span)
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

    if i > 0:
        validate(entry[0], replacement_span_map[i-1][0])

    replacement_span_map.insert(i, entry)

    if i < len(replacement_span_map) - 1:
        validate(entry[0], replacement_span_map[i+1][0])

    for j in range(i+1, len(replacement_span_map)):
        replacement_span_map[j] = replacement_span_map[j][0], (replacement_span_map[j][1][0] + entry[2], replacement_span_map[j][1][1] + entry[2]), replacement_span_map[j][2]

def repl(match, replacement_map, replacement_span_map):
    match_string = match.group()
    match_start = match.span(0)[0]
    if len(match.regs) == 1:
        raise Exception('No match groups in regex pattern.')
    delta = span_offset(match.span(1), replacement_span_map)

    current_match_delta = 0

    for i in replacement_map.keys():
        span = match.span(i)
        group_rel_span = span[0] - match_start, span[1] - match_start

        replacement = replacement_map[i] if isinstance(replacement_map[i], str) else replacement_map[i](match.group(i))
        match_string = match_string[0:group_rel_span[0] + current_match_delta] + replacement + match_string[group_rel_span[1] + current_match_delta:]

        match_delta = delta[1] + current_match_delta
        group_rel_span_alligned = group_rel_span[0] + match_delta, group_rel_span[1] + match_delta

        span_target = group_rel_span_alligned[0] + match_start, group_rel_span_alligned[0] + len(replacement) + match_start

        new_entry = span, span_target, span_len_delta(span_target, span)

        insert(new_entry, replacement_span_map, allow_intersect=False)
        current_match_delta += new_entry[2]

    return match_string

def normalize_source_spans(replacement_span_map, tmp_replacement_span_map):
    '''
    Corrects the source spans according to earlier length changes
    '''
    for i, (tmp_source_span, _, len_delta) in enumerate(tmp_replacement_span_map):
        delta_span = span_offset(tmp_source_span, replacement_span_map)
        tmp_replacement_span_map[i] = (tmp_source_span[0] - delta_span[0], tmp_source_span[1] - delta_span[1]), tmp_replacement_span_map[i][1], len_delta

def update_span_map(replacement_span_map, tmp_replacement_span_map):
    for entry in tmp_replacement_span_map:
        insert(entry, replacement_span_map)

class Processor:
    def __init__(self, text):
        self.__processing = False
        self.__text = str(text)
        self.__processed_text = str(text)
        self.__replacement_span_map = []
        self.__span_map = []

    def process(self, pattern, replacement_map, count=0, flags=0):
        if not self.__processing:
            raise Exception("Processing session not initiated")

        tmp_replacement_span_map = []

        self.__processed_text = re.sub(
            pattern = pattern,
            repl = lambda match: repl(match, replacement_map, tmp_replacement_span_map),
            string = self.__processed_text,
            count=count,
            flags = flags
        )

        normalize_source_spans(self.__replacement_span_map, tmp_replacement_span_map)

        update_span_map(self.__replacement_span_map, tmp_replacement_span_map)

    def swap(self):
        self.__replacement_span_map = [(destination, source, -delta) for source, destination, delta in self.__replacement_span_map]

        tmp = self.__text
        self.__text = self.__processed_text
        self.__processed_text = tmp

    def decorate(self):
        return decorate(self.__text, self.__processed_text, self.span_map)

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