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