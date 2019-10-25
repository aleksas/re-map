def decorate(text, processed_text, span_map):
    text = str(text)
    processed_text = str(processed_text)
    for i, span in enumerate(span_map):
        span = span_map[i]
        a = span[0][1] - span[0][0]
        b = span[1][1] - span[1][0]
        v = '{:x}'.format(i%16).upper()
        text = text[0:span[0][0]] + a*v + text[span[0][1]:]
        processed_text = processed_text[0:span[1][0]] + b*v + processed_text[span[1][1]:]

    return text, processed_text


def text_range(text, processed_text, span_map, source_len_limit, target_len_limit):
    span_map_length = len(span_map)
    for start in range(span_map_length):
        for end in range(start, span_map_length):
            source_start = span_map[start][0][0]
            source_end = span_map[end][0][1]
            target_start = span_map[start][1][0]
            target_end = span_map[end][1][1]
            if ( source_end - source_start < source_len_limit and 
                target_end - target_start < source_len_limit) :
                continue
            else:
                yield text[source_start:source_end], processed_text[target_start:target_end]
                break