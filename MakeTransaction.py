from Queue import Queue
import time
from Node import Node
from MUASCoin import generateTransaction, makeHash
from MUASCoin import generateBlock
from random import randint
from person import person


class MakeTransaction:
    threads = []
    persons = [person("Alice"), person("Bob"), person("Carol")]

    def __init__(self):

        self.createThreads(number = 3, difficulty = 3)

        self.distributeThreads()

        originOutput = [(0, 0)]
        originalOwner = self.persons[0]
        newOutput = [(originalOwner, 20), (self.persons[1], 5)]
        signatureOrginalOwner = originalOwner.sign(makeHash(originOutput, newOutput))
        message = generateTransaction(originOutput, newOutput, [signatureOrginalOwner])

        self.sendTransactionMessage(message)

        originOutput = [(1, 1)]
        originalOwner = self.persons[1]
        newOutput = [(originalOwner, 0), (self.persons[2], 5)]
        signatureOrginalOwner = originalOwner.sign(makeHash(originOutput, newOutput))
        message = generateTransaction(originOutput, newOutput, [signatureOrginalOwner])

        self.sendTransactionMessage(message)

        originOutput = [(1, 0), (2, 0)]
        originalOwner = self.persons[1]
        newOutput = [(originalOwner, 0), (self.persons[2], 5)]
        signatureOrginalOwner = originalOwner.sign(makeHash(originOutput, newOutput))
        message = generateTransaction(originOutput, newOutput, [signatureOrginalOwner])

        self.sendTransactionMessage(message)

        self.generateRandomValidTransactions()

        for t in self.threads:
            t.join()

    def distributeThreads(self):
        time.sleep(1)
        for t in self.threads:
            t.queue.put(self.threads)
            time.sleep(0.3)

    def createThreads(self, number, difficulty):

        firstTransaction = generateTransaction([None], [(self.persons[0], 25)], [])
        firstBlock = generateBlock(firstTransaction, 0)
        for t in range(number):
            q = Queue()
            self.threads.append(Node(q, [firstBlock], difficulty, startTransaction=1))
            self.threads[t].start()
            time.sleep(0.1)

    def sendTransactionMessage(self, message):
        for t in self.threads:
            t.queue.put({"messageType": "newTransaction", "message": message})

    def generateRandomValidTransactions(self):
        number = 0
        while number < 50:
            blockChain = self.threads[0].getBlockchain()
            #rotate through all the persons
            newOwner = self.persons[randint(0, len(self.persons) - 1)]
            newInputs = [(number, 0)] #ToDo: Make inputs random
            #nicht anfassen, am besten auch nicht lesen
            oldOwner = blockChain[-1].get("transaction").get("output")[newInputs[0][1]][0]
            newOutputs = [(newOwner, 5)] #ToDo: Make payout random, maybe more than one new owner
            message = generateTransaction(newInputs, newOutputs, [oldOwner.sign(makeHash(newInputs, newOutputs))])
            self.sendTransactionMessage(message)
            time.sleep(randint(5, 10))
            number += 1

