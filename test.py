from pymemcache.client import base
import time
import threading
import logging

client = base.Client(('localhost', 11211))


def test_memcached(fr=0, lim=10000):
    print(f'throttling for  {fr}+{lim - 1} sequential requests')

    ms_start = time.time() * 1000.0

    for i in range(fr, lim):
        val = client.get(f'some_key_{fr}')
        if val is None:
            print('cache miss')


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

    num_entries = 100000

    # sequential_test(num_entries)
    
    # ----------------------------- Parallel test


    format = "%(asctime)s: %(message)s"
    lim = num_entries//20

    fill_cache_entries(num_entries)    

    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.info("Main    : before creating thread")

    ms_start = time.time() * 1000.0

    threads = list()
    for index in range(20):
        logging.info("Main    : create and start thread %d.", index)
        x = threading.Thread(target=test_memcached, args=(index * lim, lim))
        threads.append(x)
        x.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)

    logging.info("Main    : all done")

    ms_end = time.time() * 1000.0
    ms_diff = ms_end - ms_start
    logging.info(f'time took to fill sequentially: {ms_diff}')

