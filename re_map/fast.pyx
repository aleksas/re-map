cimport cython

cdef inline int int_max(int a, int b): return a if a > b else b
cdef inline int int_min(int a, int b): return a if a < b else b

@cython.boundscheck(False)
cpdef span_rtrim((int, int) span, int value):
    if span[0] < value:
        return (int_min(span[0], value), int_min(span[1], value))
    
@cython.boundscheck(False)
cpdef intersect((int, int) span_a, (int, int) span_b):
    return int_max(span_a[0], span_b[0]) < int_min(span_a[1], span_b[1])

@cython.boundscheck(False)
cpdef intersection((int, int) span_a, (int, int) span_b):
    cdef (int, int) span = (int_max(span_a[0], span_b[0]), int_min(span_a[1], span_b[1]))
    if span[0] < span[1]:
        return span

@cython.boundscheck(False)
cpdef span_len_delta((int, int) span_1, (int, int) span_2):
    return (span_1[1] - span_1[0]) - (span_2[1] - span_2[0])

@cython.boundscheck(False)
cpdef span_length((int, int) span):
    return span[1] - span[0]