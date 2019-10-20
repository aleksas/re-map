def span_rtrim(span, value):
    if span[0] < value:
        return (min(span[0], value), min(span[1], value))

def intersect(span_a, span_b):
    return max(span_a[0], span_b[0]) < min(span_a[1], span_b[1])

def intersection(span_a, span_b):
    span = (max(span_a[0], span_b[0]), min(span_a[1], span_b[1]))
    if span[0] < span[1]:
        return span

def span_len_delta(span_1, span_2):
    return (span_1[1] - span_1[0]) - (span_2[1] - span_2[0])

def span_length(span):
    return span[1] - span[0]