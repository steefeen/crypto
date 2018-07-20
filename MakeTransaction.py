from Queue import Queue
import time
from Node import Node
from MUASCoin import generateTransaction
from MUASCoin import generateBlock
from random import randint

class MakeTransaction:
    threads = []

    def __init__(self):

        self.createThreads(1)

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

        firstTransaction = generateTransaction([None], [{"Bob": 24}], 0, "generate")
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
        number = 1
        while True:
            message = generateTransaction([None], [{"Bob": 25 + number}], number, "generate")
            self.sendMessages(message)
            number += 1
            time.sleep(randint(10, 20))

[{'nounce': 0, 'previousBlock': 0, 'transaction': {'output': [{'Bob': 24}], 'transActionNumber': '1ef2a2c90feeafd54a89200e89b22b2b01901c23af5c4ba32254ebc11f851340', 'signatures': None, 'type': 'generate', 'input': [None]}}, {'nounce': 6117517034023623977, 'previousBlock': '1ef2a2c90feeafd54a89200e89b22b2b01901c23af5c4ba32254ebc11f851340', 'transaction': {'output': [{'Bob': 25}], 'transActionNumber': 'db38787f7508a45fcfa87153ee454a55e1b31115e4e891e427eb9bce50605da2', 'signatures': None, 'type': 'generate', 'input': [None]}}, {'nounce': 3075861720232679229, 'previousBlock': 'db38787f7508a45fcfa87153ee454a55e1b31115e4e891e427eb9bce50605da2', 'transaction': {'output': [{'Bob': 26}], 'transActionNumber': '5b7e4c88a98a731a10f30ec294cae0790d90878db0b1ba686a4389647be0ee89', 'signatures': None, 'type': 'generate', 'input': [None]}}, {'nounce': 388666371360118067, 'previousBlock': '5b7e4c88a98a731a10f30ec294cae0790d90878db0b1ba686a4389647be0ee89', 'transaction': {'output': [{'Bob': 27}], 'transActionNumber': 'd316e4b1d0eb616873e40d7e751f13167677cefe99b55bff3caca46d1a1bc6d9', 'signatures': None, 'type': 'generate', 'input': [None]}}, {'nounce': 6656015203774969805, 'previousBlock': 'd316e4b1d0eb616873e40d7e751f13167677cefe99b55bff3caca46d1a1bc6d9', 'transaction': {'output': [{'Bob': 28}], 'transActionNumber': '69c810c2ac5f1b4e79e8e89f6418710c4a8fc491adaeb930278dc2922fe79b7b', 'signatures': None, 'type': 'generate', 'input': [None]}}, {'nounce': 3272984176080170469, 'previousBlock': '69c810c2ac5f1b4e79e8e89f6418710c4a8fc491adaeb930278dc2922fe79b7b', 'transaction': {'output': [{'Bob': 29}], 'transActionNumber': '0d5d331bc6338393b676830b5d0aa4ea13db619ed381b153072c6b4aec0de9ce', 'signatures': None, 'type': 'generate', 'input': [None]}}]
