from Queue import Queue
import time
from Node import Node
from MUASCoin import generateTransaction
from random import randint

class MakeTransaction:
    threads = []

    def __init__(self):

        self.createThreads(4)

        self.distributeThreads()

        message = generateTransaction([None], [{"Bob": 25}], 0, "generate")

        self.sendMessages(message)

        self.generateRandomTransactions()

        for t in self.threads:
            t.join()

    def distributeThreads(self):
        time.sleep(1)
        for t in self.threads:
            t.queue.put(self.threads)
            time.sleep(0.3)

    def createThreads(self, number):
        for t in range(number):
            q = Queue()
            self.threads.append(Node(q, args=(True,)))
            self.threads[t].start()
            time.sleep(0.1)

    def sendMessages(self, message):
        time.sleep(1)
        for t in self.threads:
            t.queue.put(message)
            time.sleep(0.3)

    def generateRandomTransactions(self):
        number = 1
        while True:
            message = generateTransaction([None], [{"Bob": 25}], number, "generate")
            self.sendMessages(message)
            number += 1
            time.sleep(randint(10, 20))
