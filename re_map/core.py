import re 

__verbose__ = False
__extended__ = False

def span_len_delta(span_1, span_2):
    return (span_1[1] - span_1[0]) - (span_2[1] - span_2[0])

def len_delta(match_start, modifier_index, replacement_span_map):
    other_modifier_delta, same_modifier_delta, same_modifier_source_delta = 0, 0, 0
    for span_source, span_target, span_modifier_index, span_chain_source in replacement_span_map:
        if span_target[0] < match_start:
            delta = span_len_delta(span_target, span_chain_source)
            if span_modifier_index != modifier_index:
                other_modifier_delta += delta
            else:
                same_modifier_delta += delta
                same_modifier_source_delta += span_len_delta(span_chain_source, span_source)

    return other_modifier_delta, same_modifier_delta, same_modifier_source_delta

def validate(entry_1, i, replacement_span_map):
    if len(replacement_span_map) <= i or i < 0:
        return

    entry_2 = replacement_span_map[i]

    ops = [ # uses assum[ption that span[0] < span[1] 
        lambda x, y : (x[0] < y[0]) == (x[1] < y[0]), 
        lambda x, y : (x[0] > y[0]) == (x[0] > y[1]), 
        lambda x, y : (x[0] == y[0]) == (x[1] == y[1])
    ]

    def cmp(span1, span2):
        valid = True
        for op in ops:
            valid = valid and op(span1, span2)
        return valid

    valid = cmp(entry_1[0], entry_2[0])
    valid = valid and cmp(entry_1[1], entry_2[1])

    #if not valid:
    #    raise Exception("New entry intersects with other entry")

def sub(span, value):
    return span[0] - value, span[1] - value

def insert(entry, current_span, other_modifier_delta, same_modifier_current_match_delta, replacement_span_map):
    delta = span_len_delta(entry[1], entry[3]) 

    i=0
    replace=False
    for i in range(len(replacement_span_map) + 1): # +1 for i to actually reach last element
        if i == len(replacement_span_map):
            break        
        if replacement_span_map[i][0][0] > entry[0][1]:
            break
        if sub(replacement_span_map[i][1], delta) == current_span:
            replace = True
            break
        if replacement_span_map[i][1] == current_span:
            replace = True
            break

    if replace:
        entry = replacement_span_map[i][0], entry[1], entry[2], entry[0]
        del replacement_span_map[i]

    validate(entry, i - 1, replacement_span_map)
    replacement_span_map.insert(i, entry)
    validate(entry, i + 1, replacement_span_map)

    for j in range(i+1, len(replacement_span_map)):
        replacement_span_map[j] = replacement_span_map[j][0], (replacement_span_map[j][1][0] + delta, replacement_span_map[j][1][1] + delta), replacement_span_map[j][2], replacement_span_map[j][0]

    return delta
    
def repl(match, replacement_map, modifier_index, replacement_span_map):
    match_string = match.group()
    match_start = match.span(0)[0]
    other_modifier_delta, same_modifier_previous_match_delta, same_modifier_source_delta = len_delta(match.span(1)[0], modifier_index, replacement_span_map)
    
    same_modifier_current_match_delta = 0
    
    for i in replacement_map.keys():
        span = match.span(i)
        
        span_source = span[0] - other_modifier_delta - same_modifier_source_delta, span[1] - other_modifier_delta - same_modifier_source_delta
        assert(span_source[0] < span_source[1])

        group_rel_span = span[0] - match_start, span[1] - match_start

        replacement = replacement_map[i] if isinstance(replacement_map[i], str) else replacement_map[i](match.group(i))
        match_string = match_string[0:group_rel_span[0] + same_modifier_current_match_delta] + replacement + match_string[group_rel_span[1] + same_modifier_current_match_delta:]

        same_modifier_match_delta = same_modifier_previous_match_delta + same_modifier_current_match_delta
        group_rel_span_alligned = group_rel_span[0] + same_modifier_match_delta, group_rel_span[1] + same_modifier_match_delta

        span_target = group_rel_span_alligned[0] + match_start, group_rel_span_alligned[0] + len(replacement) + match_start
        assert(span_target[0] < span_target[1])
        
        new_entry = span_source, span_target, modifier_index, span_source
        
        delta = insert(new_entry, span, other_modifier_delta, same_modifier_current_match_delta, replacement_span_map)
        same_modifier_current_match_delta += delta

    return match_string

def decorate(text, text_modified, span_map):
    text = str(text)
    text_modified = str(text_modified)
    for i in range(len(span_map)):
        so, to = span_map[i]
        a = so[1] - so[0]
        b = to[1] - to[0]
        v = '{:x}'.format(i).upper()
        text = text[0:so[0]] + a*v + text[so[1]:]
        text_modified = text_modified[0:to[0]] + b*v + text_modified[to[1]:]
    
    return text, text_modified

def process(text, modifiers):
    processed_text = str(text)
    replacement_span_map = []

    for i in range(len(modifiers)):
        pattern, replacement_map = modifiers[i]

        if(__verbose__):
            print ('in:', processed_text, i)

        processed_text = re.sub(
            pattern = pattern, 
            repl = lambda match: repl(match, replacement_map, i, replacement_span_map), 
            string = processed_text
        )

        if(__verbose__):
            span_map = [(a, b) for a,b,_,_ in replacement_span_map]
            decorate(text, processed_text, span_map)
            print ( span_map )
            print ('out:', processed_text, i)

        if __extended__:
            pass

    return processed_text, [(a, b) for a,b,_,_ in replacement_span_map]
