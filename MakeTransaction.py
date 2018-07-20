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

        message = generateTransaction([("db38787f7508a45fcfa87153ee454a55e1b31115e4e891e427eb9bce50605da2", 0)], [(self.persons[0], 25)], "generate")

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

        firstTransaction = generateTransaction([None], [(self.persons[0], 25)], "generate")
        firstBlock = generateBlock(firstTransaction, 0, 0)
        for t in range(number):
            q = Queue()
            self.threads.append(Node(q, firstBlock, args=(True, 1)))
            self.threads[t].start()
            time.sleep(0.1)

    def sendMessages(self, message):
        time.sleep(1)
        for t in self.threads:
            t.queue.put(message)
            time.sleep(0.3)

    def generateRandomTransactions(self):

        #while True:
        message = generateTransaction([("0150ede729f30b7808b0c0e966bfb9f48018b27ab5519a52a854f28f80f2942a", 0)], [(self.persons[0], 25)], "generate")
        self.sendMessages(message)
        time.sleep(randint(10, 20))

{'db38787f7508a45fcfa87153ee454a55e1b31115e4e891e427eb9bce50605da2': {'nounce': 0, 'previousBlock': 0, 'transaction': {'output': [{'Bob': 25}], 'transActionNumber': 'db38787f7508a45fcfa87153ee454a55e1b31115e4e891e427eb9bce50605da2', 'signatures': None, 'type': 'generate', 'input': [None]}},
 '5127bca0d990fe924886bb81a6eedc8eac6038c00cf9eedb6207cb45e5575474': {'nounce': 9153864084616655301, 'previousBlock': '0150ede729f30b7808b0c0e966bfb9f48018b27ab5519a52a854f28f80f2942a', 'transaction': {'output': [('Bob', 25)], 'transActionNumber': '5127bca0d990fe924886bb81a6eedc8eac6038c00cf9eedb6207cb45e5575474', 'signatures': None, 'type': 'generate', 'input': [('0150ede729f30b7808b0c0e966bfb9f48018b27ab5519a52a854f28f80f2942a', 0)]}},
 '0150ede729f30b7808b0c0e966bfb9f48018b27ab5519a52a854f28f80f2942a': {'nounce': 5938097406838539746, 'previousBlock': 'db38787f7508a45fcfa87153ee454a55e1b31115e4e891e427eb9bce50605da2', 'transaction': {'output': [('Bob', 25)], 'transActionNumber': '0150ede729f30b7808b0c0e966bfb9f48018b27ab5519a52a854f28f80f2942a', 'signatures': None, 'type': 'generate', 'input': [('db38787f7508a45fcfa87153ee454a55e1b31115e4e891e427eb9bce50605da2', 0)]}}}
