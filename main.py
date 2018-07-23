
from MakeTransaction import MakeTransaction






if __name__ == '__main__':
    t = MakeTransaction()

# from multiprocessing import Process
# import os
#
#
# def info(title):
#     print title
#     print 'module name:', __name__
#     if hasattr(os, 'getppid'):  # only available on Unix
#         print 'parent process:', os.getppid()
#     print 'process id:', os.getpid()
#
#
# def f(name):
#     info('function f')
#     while True:
#         a=2
#
#
# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob1',))
#     p.start()
#     p = Process(target=f, args=('bob2',))
#     p.start()
#     p = Process(target=f, args=('bob3',))
#     p.start()
#     p = Process(target=f, args=('bob4',))
#     p.start()
#     p = Process(target=f, args=('bob5',))
#     p.start()
#     p = Process(target=f, args=('bob6',))
#     p.start()
#     p = Process(target=f, args=('bob7',))
#     p.start()
#     p = Process(target=f, args=('bob8',))
#     p.start()
#
#     p.join()
