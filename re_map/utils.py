def decorate(text, text_modified, span_map):
    text = str(text)
    text_modified = str(text_modified)
    for i, span in enumerate(span_map):
        span = span_map[i]
        a = span[0][1] - span[0][0]
        b = span[1][1] - span[1][0]
        v = '{:x}'.format(i%16).upper()
        text = text[0:span[0][0]] + a*v + text[span[0][1]:]
        text_modified = text_modified[0:span[1][0]] + b*v + text_modified[span[1][1]:]

    return text, text_modified