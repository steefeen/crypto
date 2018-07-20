import sys
import threading
import hashlib
import time
from random import randint
from MUASCoin import generateBlock

class Node(threading.Thread):

    def __init__(self, queue, blockChain ,args=()):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True
        self.receive_messages = args[0]
        self.startTransactions = args[1]
        self.unverifiedTransacton = []
        self.allThreads = []
        self.blockChain = {blockChain.get("transaction").get("transActionNumber") : blockChain}
        self.lastBlock = blockChain.get("transaction").get("transActionNumber")
        print(self.blockChain)
    def run(self):

        print(threading.currentThread().getName(), self.receive_messages)

        self.reciveThreads()

        self.waitForFirstMessage()

        self.work()

    def do_thing_with_message(self, message):
        if self.receive_messages:
            self.unverifiedTransacton.append(message)
            print(threading.currentThread().getName(), "Received {}".format(message))
            print(threading.currentThread().getName(), ('[%s]' % ', '.join(map(str, self.unverifiedTransacton))))

    def reciveThreads(self):
        val = self.queue.get()
        for t in val:
            if t != self:
                self.allThreads.append(t)

        print('[%s]' % ', '.join(map(str, self.allThreads)))

    def waitForFirstMessage(self):
        income = True
        while income:
            time.sleep(1)
            val = self.queue.get()
            if(val != None):
                self.do_thing_with_message(val)
                income = False

    def work(self):
        while True:
            self.checkForNewMessages()
            self.transactionToWork = self.getRandomTransaction()
            if(self.transactionToWork != None):
                self.findHash()

    def getRandomTransaction(self):
        if (len(self.unverifiedTransacton) > 0):
            return self.unverifiedTransacton[0]
        else:
            return None
        # if(len(self.unverifiedTransacton)>0):
        #     number = randint(0, len(self.unverifiedTransacton)-1)
        #     return self.unverifiedTransacton[number]
        # return None

    def checkForNewMessages(self):

        while not self.queue.empty():
            val = self.queue.get()
            if(val != None):
                self.do_thing_with_message(val)



    def findHash(self):
        i = randint(0, sys.maxint)
        #print(i)
        hashOfI = hashlib.sha256(str(self.transactionToWork)+ str(i))
        #print(str(self.transactionToWork))
        #print("tried: " + str(i) + "found: " + hashOfI.hexdigest())
        if(hashOfI.hexdigest()[0:5] == "00000"):
            print("tried: " + str(i) + "found: " + hashOfI.hexdigest())
            print("successful!")
            self.foundHash(i)

    def foundHash(self, nonce):


        generatedBlock = generateBlock(self.transactionToWork, nonce, self.lastBlock)
        self.lastBlock = self.transactionToWork.get("transActionNumber")
        self.blockChain[generatedBlock.get("transaction").get("transActionNumber")] = generatedBlock
        print(self.blockChain)
        self.unverifiedTransacton.pop(0)

        # {'d316e4b1d0eb616873e40d7e751f13167677cefe99b55bff3caca46d1a1bc6d9': {'nounce': 48034001894148745,
        #                                                                       'previousBlock': '5b7e4c88a98a731a10f30ec294cae0790d90878db0b1ba686a4389647be0ee89',
        #                                                                       'transaction': {'output': [{'Bob': 27}],
        #                                                                                       'transActionNumber': 'd316e4b1d0eb616873e40d7e751f13167677cefe99b55bff3caca46d1a1bc6d9',
        #                                                                                       'signatures': None,
        #                                                                                       'type': 'generate',
        #                                                                                       'input': [None]}},
        #  'db38787f7508a45fcfa87153ee454a55e1b31115e4e891e427eb9bce50605da2': {'nounce': 658971777253565240,
        #                                                                       'previousBlock': '1ef2a2c90feeafd54a89200e89b22b2b01901c23af5c4ba32254ebc11f851340',
        #                                                                       'transaction': {'output': [{'Bob': 25}],
        #                                                                                       'transActionNumber': 'db38787f7508a45fcfa87153ee454a55e1b31115e4e891e427eb9bce50605da2',
        #                                                                                       'signatures': None,
        #                                                                                       'type': 'generate',
        #                                                                                       'input': [None]}},
        #  '1ef2a2c90feeafd54a89200e89b22b2b01901c23af5c4ba32254ebc11f851340': {'nounce': 0, 'previousBlock': 0,
        #                                                                       'transaction': {'output': [{'Bob': 24}],
        #                                                                                       'transActionNumber': '1ef2a2c90feeafd54a89200e89b22b2b01901c23af5c4ba32254ebc11f851340',
        #                                                                                       'signatures': None,
        #                                                                                       'type': 'generate',
        #                                                                                       'input': [None]}},
        #  '5b7e4c88a98a731a10f30ec294cae0790d90878db0b1ba686a4389647be0ee89': {'nounce': 373632305728762512,
        #                                                                       'previousBlock': 'db38787f7508a45fcfa87153ee454a55e1b31115e4e891e427eb9bce50605da2',
        #                                                                       'transaction': {'output': [{'Bob': 26}],
        #                                                                                       'transActionNumber': '5b7e4c88a98a731a10f30ec294cae0790d90878db0b1ba686a4389647be0ee89',
        #                                                                                       'signatures': None,
        #                                                                                       'type': 'generate',
        #                                                                                       'input': [None]}},
        #  '69c810c2ac5f1b4e79e8e89f6418710c4a8fc491adaeb930278dc2922fe79b7b': {'nounce': 3065130957103389172,
        #                                                                       'previousBlock': 'd316e4b1d0eb616873e40d7e751f13167677cefe99b55bff3caca46d1a1bc6d9',
        #                                                                       'transaction': {'output': [{'Bob': 28}],
        #                                                                                       'transActionNumber': '69c810c2ac5f1b4e79e8e89f6418710c4a8fc491adaeb930278dc2922fe79b7b',
        #                                                                                       'signatures': None,
        #                                                                                       'type': 'generate',
        #                                                                                       'input': [None]}},
        #  '0d5d331bc6338393b676830b5d0aa4ea13db619ed381b153072c6b4aec0de9ce': {'nounce': 576752414274413228,
        #                                                                       'previousBlock': '69c810c2ac5f1b4e79e8e89f6418710c4a8fc491adaeb930278dc2922fe79b7b',
        #                                                                       'transaction': {'output': [{'Bob': 29}],
        #                                                                                       'transActionNumber': '0d5d331bc6338393b676830b5d0aa4ea13db619ed381b153072c6b4aec0de9ce',
        #                                                                                       'signatures': None,
        #                                                                                       'type': 'generate',
        #                                                                                       'input': [None]}}}
