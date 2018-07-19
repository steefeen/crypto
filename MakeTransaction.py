from queue import Queue
import time
from Node import Node
import MUASCoin

class MakeTransaction:
    threads = []
    transaction = {'a': 1}

    def __init__(self):

        for t in range(1):
            q = Queue()
            self.threads.append(Node(q, args=(True,)))
            self.threads[t].start()
            time.sleep(0.1)

        time.sleep(1)
        for t in self.threads:
            t.queue.put(self.threads)
            time.sleep(0.3)

        time.sleep(1)
        for t in self.threads:
            t.queue.put(self.transaction)
            time.sleep(0.3)

        time.sleep(2)
        newTransaction = {'a' : 1}
        for t in self.threads:
            t.queue.put(newTransaction)
            time.sleep(0.3)

        time.sleep(2)
        newTransaction = {'a' : 2}
        for t in self.threads:
            t.queue.put(newTransaction)
            time.sleep(0.3)



        for t in self.threads:
            t.join()