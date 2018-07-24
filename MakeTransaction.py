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

        self.createThreads(number = 1, difficulty = 3)

        self.distributeThreads()

        message = generateTransaction([(0, 0), (0, 0)], [(self.persons[0], 40), (self.persons[1], 10)], "generate")

        self.sendTransactionMessage(message)

        self.generateRandomTransactions()

        for t in self.threads:
            t.join()

    def distributeThreads(self):
        time.sleep(1)
        for t in self.threads:
            t.queue.put(self.threads)
            time.sleep(0.3)

    def createThreads(self, number, difficulty):

        firstTransaction = generateTransaction([None], [(self.persons[0], 25)], "generate")
        firstBlock = generateBlock(firstTransaction, 0)
        for t in range(number):
            q = Queue()
            self.threads.append(Node(q, [firstBlock], difficulty, args=(True, 1)))
            self.threads[t].start()
            time.sleep(0.1)

    def sendTransactionMessage(self, message):
        time.sleep(1)
        for t in self.threads:
            t.queue.put({"messageType": "newTransaction", "message": message})
            time.sleep(0.3)

    def generateRandomTransactions(self):
        number = 0
        while number < 5:
            message = generateTransaction([(number, 0)], [(self.persons[0], 25)], "generate")
            self.sendTransactionMessage(message)
            time.sleep(randint(5, 10))
            number += 1
