# cython: boundscheck=False


cdef extern from "lowlevel/module.c" nogil:
    int binary_search_impl(int index);
    float pi_impl(long S);


cdef int b_search(int index) nogil:
    return binary_search_impl(index);

cdef float pi(long S) nogil:
    return pi_impl(S);


def binary_search(int index, results = None):
    cdef int result;

    with nogil:
        result = b_search(index);

    if results is not None:
        results.append(result)
    
    return result



def calc_pi(long S, results = None):
    cdef float result;

    with nogil:
        result = pi(S);

    if results is not None:
        results.append(result)
    
    return result
