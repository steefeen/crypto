from Queue import Queue
import time
from Node import Node
from MUASCoin import generateTransaction
from MUASCoin import generateBlock
from random import randint
from person import person


class MakeTransaction:
    threads = []
    persons = [person("Alice"), person("Bob"), person("Carol")]

    def __init__(self):

        self.createThreads(1)

        self.distributeThreads()

        message = generateTransaction([(0, 0), (0, 0)], [(self.persons[0], 25), (self.persons[1], 10)], "generate")

        self.sendTransactionMessage(message)

        self.generateRandomTransactions()

        for t in self.threads:
            t.join()

    def distributeThreads(self):
        time.sleep(1)
        for t in self.threads:
            t.queue.put(self.threads)
            time.sleep(0.3)

    def createThreads(self, number):

        firstTransaction = generateTransaction([None], [(self.persons[0], 25)], "generate")
        firstBlock = generateBlock(firstTransaction, 0)
        for t in range(number):
            q = Queue()
            self.threads.append(Node(q, [firstBlock], args=(True, 1)))
            self.threads[t].start()
            time.sleep(0.1)

    def sendTransactionMessage(self, message):
        time.sleep(1)
        for t in self.threads:
            t.queue.put({"messageType": "newTransaction", "message": message})
            time.sleep(0.3)

    def generateRandomTransactions(self):

        #while True:
        message = generateTransaction([(1, 0)], [(self.persons[0], 25)], "generate")
        self.sendMessages(message)
        time.sleep(randint(10, 20))
