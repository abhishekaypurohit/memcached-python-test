from pymemcache.client import base
from pymemcache.client.base import PooledClient
import time
import threading
import logging
from random import seed
from random import choice



# client = base.Client(('localhost', 11211), connect_timeout=1, timeout=0.5)
# client = PooledClient(('127.0.0.1', 11211), max_pool_size=20, connect_timeout=1, timeout=0.5)
# m=no maxpool means its higher limit - 2147483648L
client = PooledClient(('127.0.0.1', 11211), connect_timeout=1, timeout=0.5)


def test_memcached(id=0, fr=0, lim=10000):
    print(f'throttling for  {fr}+{lim - 1} sequential requests')

    ms_start = time.time() * 1000.0

    for i in range(fr, lim):
        val = client.get(f'some_key_{i}')
        # print(val)
        if val is None:
            print('cache miss')

    print(f'finished - {id}')


def fill_cache_entries(num_entries):
    if not client:
        print("not connected")
        return

    for i in range(num_entries):
        client.set(f'some_key_{i}', f'some value num {i}')


def sequential_test(lim):
    ms_start = time.time() * 1000.0
    fill_cache_entries(num_entries)
    ms_end = time.time() * 1000.0
    ms_diff = ms_end - ms_start
    print(f'time took to fill sequentially: {ms_diff}')

    ms_start = time.time() * 1000.0
    test_memcached(0, num_entries)
    ms_end = time.time() * 1000.0
    ms_diff = ms_end - ms_start
    print(f'time took to fill sequentially: {ms_diff}')


if __name__ == '__main__':

    num_entries = 10000

    # sequential_test(num_entries)

    # ----------------------------- Parallel test

    format = "%(asctime)s: %(message)s"
    lim = num_entries // 20

    ms_start = time.time() * 1000.0
    fill_cache_entries(num_entries)
    ms_end = time.time() * 1000.0
    ms_diff = ms_end - ms_start
    print(f'total time in filling: {ms_diff}')


    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")

    ms_start = time.time() * 1000.0
    threads = list()
    seed(1)
    sequence = [i for i in range(20)]
    for _ in range(20):
        index = choice(sequence)

    # for index in range(20):
        logging.info("Main    : create and start thread %d.", index)

        # x = threading.Thread(target=test_memcached, args=(index, index * lim, lim))
        x = threading.Thread(target=test_memcached, args=(index, 0, 10000))
        # x = threading.Thread(target=test_memcached, args=(index, 0, num_entries))

        threads.append(x)
        x.start()

    # time.sleep(10)
    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)

    logging.info("Main    : all done")

    ms_end = time.time() * 1000.0
    ms_diff = ms_end - ms_start
    logging.info(f'total time: {ms_diff}')
