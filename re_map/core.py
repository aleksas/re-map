import re
from .utils import decorate

__verbose__ = False
__extended__ = False

def span_len_delta(span_1, span_2):
    return (span_1[1] - span_1[0]) - (span_2[1] - span_2[0])

def len_delta(span, replacement_span_map):
    delta_start, delta_end = 0, 0
    for span_source, span_target in replacement_span_map:
        if span_target[1] <= span[1]:
            d = span_len_delta(span_target, span_source)
            delta_end += d
            if span_target[1] <= span[0]:
                delta_start += d

    return delta_start, delta_end

def insert(entry, replacement_span_map):
    def validate(source_span, ref_source_span):
        if ref_source_span[0] < source_span[0] and ref_source_span[1] > source_span[0]:
            raise Exception("Illegal san intersection")
        elif ref_source_span[0] < source_span[1] and ref_source_span[1] > source_span[1]:
            raise Exception("Illegal span intersection")

    i = 0
    replace=False

    for source_span, _ in replacement_span_map:
        if source_span[0] >= entry[0][1]:
            break
        if source_span == entry[0]:
            replace = True
            break

        i+=1

    if replace:
        # calculate delta from new entry target and old entry target
        delta = span_len_delta(entry[1], replacement_span_map[i][1])
        del replacement_span_map[i]
    else:
        delta = span_len_delta(entry[1], entry[0])

    if i > 0:
        validate(entry[0], replacement_span_map[i-1][0])

    replacement_span_map.insert(i, entry)

    if i < len(replacement_span_map) - 1:
        validate(entry[0], replacement_span_map[i+1][0])

    for j in range(i+1, len(replacement_span_map)):
        replacement_span_map[j] = replacement_span_map[j][0], (replacement_span_map[j][1][0] + delta, replacement_span_map[j][1][1] + delta)

    return delta

def repl(match, replacement_map, replacement_span_map):
    match_string = match.group()
    match_start = match.span(0)[0]
    delta = len_delta(match.span(1), replacement_span_map)
    if delta[0] != delta[1]:
        print ("hmm")

    current_match_delta = 0

    for i in replacement_map.keys():
        span = match.span(i)
        group_rel_span = span[0] - match_start, span[1] - match_start

        replacement = replacement_map[i] if isinstance(replacement_map[i], str) else replacement_map[i](match.group(i))
        match_string = match_string[0:group_rel_span[0] + current_match_delta] + replacement + match_string[group_rel_span[1] + current_match_delta:]

        match_delta = delta[1] + current_match_delta
        group_rel_span_alligned = group_rel_span[0] + match_delta, group_rel_span[1] + match_delta

        span_target = group_rel_span_alligned[0] + match_start, group_rel_span_alligned[0] + len(replacement) + match_start

        new_entry = span, span_target

        current_match_delta += insert(new_entry, replacement_span_map)

    return match_string

def normalize_source_spans(replacement_span_map, tmp_replacement_span_map):
    '''
    Corrects the source spans according to earlier length changes
    '''
    for i, (tmp_source_span, _) in enumerate(tmp_replacement_span_map):
        delta_span = len_delta(tmp_source_span, replacement_span_map)
        tmp_replacement_span_map[i] = (tmp_source_span[0] - delta_span[0], tmp_source_span[1] - delta_span[1]), tmp_replacement_span_map[i][1]

def update_span_map(replacement_span_map, tmp_replacement_span_map):
    for entry in tmp_replacement_span_map:
        insert(entry, replacement_span_map)

def process(text, modifiers):
    processed_text = str(text)
    replacement_span_map = []

    for i, (pattern, replacement_map) in enumerate(modifiers):
        tmp_replacement_span_map = []

        if(__verbose__):
            print ('in:', processed_text, i)

        processed_text = re.sub(
            pattern = pattern,
            repl = lambda match: repl(match, replacement_map, tmp_replacement_span_map),
            string = processed_text
        )

        normalize_source_spans(replacement_span_map, tmp_replacement_span_map)
        update_span_map(replacement_span_map, tmp_replacement_span_map)

        if(__verbose__):
            decorate(text, processed_text, replacement_span_map)
            print ( replacement_span_map )
            print ('out:', processed_text, i)

        if __extended__:
            pass

    return processed_text, replacement_span_map
