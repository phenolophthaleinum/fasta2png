import cython


cdef extern from 'math.h':
    long double floorl(long double x)


cdef extern from 'math.h':
    long double sqrtl(long double x)


cpdef long double calc_dim(long double b_len):
    return floorl(sqrtl(b_len)) + 1


cpdef long double calc_diff(long double dim, long double b_len):
    cdef target = dim * dim
    return target - b_len
