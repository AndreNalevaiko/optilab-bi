import multiprocessing

bind = '0.0.0.0:5000'

workers = multiprocessing.cpu_count() + 1

worker_class = 'eventlet'

timeout = 120

loglevel = 'info'
