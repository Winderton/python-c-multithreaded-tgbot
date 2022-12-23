from time import time
from multiprocessing import Process
from threading import Thread
import build.nogil as ng
import multiprocessing as mp
from multiprocessing import Pool


def performance(f):
    def handler(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()

        resultString = (f'Elapsed time: {(end - start):.3f} with result: {result}')
        return resultString
    return handler


@performance
def linear_pi(S):
    results = []


    ng.calc_pi(S, results)
    ng.calc_pi(S, results)
    ng.calc_pi(S, results)

    return results


@performance
def mt_pi(S):
    results = []

    t1 = Thread(target=ng.calc_pi, args=(S, results))
    t2 = Thread(target=ng.calc_pi, args=(S, results))
    t3 = Thread(target=ng.calc_pi, args=(S, results))

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    return results


@performance
def mp_pi(S):
    results = mp.Manager().list()

    with Pool(3) as p:
        p.starmap(ng.calc_pi, [(S, results),(S, results),(S, results)])

    return results


@performance
def linear(N):
    results = []
    ng.binary_search(N, results)
    ng.binary_search(N, results)
    ng.binary_search(N, results)
    ng.binary_search(N, results)
    ng.binary_search(N, results)

    return results


@performance
def multithreaded(N):
    results = []

    t1 = Thread(target=ng.binary_search, args=(N, results))
    t2 = Thread(target=ng.binary_search, args=(N, results))
    t3 = Thread(target=ng.binary_search, args=(N, results))
    t4 = Thread(target=ng.binary_search, args=(N, results))
    t5 = Thread(target=ng.binary_search, args=(N, results))


    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()


    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()

    return results

@performance
def multiprocessed(N):
    results = mp.Manager().list()

    p1 = Process(target=ng.binary_search, args=(N, results))
    p2 = Process(target=ng.binary_search, args=(N, results))
    p3 = Process(target=ng.binary_search, args=(N, results))
    p4 = Process(target=ng.binary_search, args=(N, results))
    p5 = Process(target=ng.binary_search, args=(N, results))

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()
    p5.join()

    return results


