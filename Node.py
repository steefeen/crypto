import sys
import threading
import hashlib
import time
from random import randint

from ecdsa import BadSignatureError

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
        self.blockChain = blockChain
        self.transactionToWorkIsVerifiyed = False
        print("blockchain:" + str(self.blockChain))

    def run(self):

        print(threading.currentThread().getName(), self.receive_messages)

        self.reciveThreads()

        self.waitForFirstMessage()

        self.work()

    def do_thing_with_message(self, message):
        if self.receive_messages:
            self.unverifiedTransacton.append(message)
            print("unverified: " , threading.currentThread().getName(), ('[%s]' % ', '.join(map(str, self.unverifiedTransacton))))

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
            if self.verifyTransaction():
                return self.unverifiedTransacton[0]
            else:
                return None
        else:
            print(threading.currentThread().getName(), "no more transactions")
            time.sleep(5)
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

        hashOfI = hashlib.sha256(str(self.transactionToWork) + str(i))
        #print(hashOfI.hexdigest())
        if(hashOfI.hexdigest()[0:4] == "0000"):
            print("tried: " + str(i) + "   found: " + hashOfI.hexdigest())

            self.foundHash(i)

    def foundHash(self, nonce):
        generatedBlock = generateBlock(self.transactionToWork, nonce)
        self.lastBlock = self.transactionToWork.get("transActionNumber")
        self.blockChain.append(generatedBlock)
        print("blockchain:" + str(self.blockChain))
        self.unverifiedTransacton.pop(0)
        self.transactionToWorkIsVerifiyed = False

    def verifyTransaction(self):
        if not self.transactionToWorkIsVerifiyed:
            transactionIsRight = self.verifyTransactionSignature() and self.verifyTransationMoney()
            self.transactionToWorkIsVerifiyed = True
            return transactionIsRight
        return True

    def verifyTransactionSignature(self):
        transaction = self.unverifiedTransacton[0]
        for out in transaction.get("output"):
            name = out[0].getName()
            signature = transaction.get("signatures")[name]
            message = transaction.get("transActionNumber")
            try:
                out[0].verify(signature, message)
            except BadSignatureError:
                self.unverifiedTransacton.pop(0)
                return False
        return True

    def verifyTransationMoney(self):
        #print(self.transactionToWork)

        return False
# blockchain:{
#     '057c48e453d850ffc3d8abb7b080ba12b01e3651c90c580b3e905f8c6afb9612': {'nounce': 8311886965351671661, 'previousBlock': 'cad27f8b2d5504ae65f18b595523b9c44708ed6e9ce0740d3434b8487da59274', 'transaction': {'output': [(<person.person instance at 0x10b6cc488>, 25)], 'transActionNumber': '057c48e453d850ffc3d8abb7b080ba12b01e3651c90c580b3e905f8c6afb9612', 'signatures': {'Alice': 'N\x116\x8f\xd9\x95\x9e#Cz\xd6"\x82E\x1e\xe15U$\xe7\x15p0\x94\x1f\xed\xed\xb6\x1f\xda\n\xbfJb\x9c\xc4\xdf\x1f\x02H\x0b\x8e[\x17i\x01\x9f\x8e'}, 'type': 'generate', 'input': [('0150ede729f30b7808b0c0e966bfb9f48018b27ab5519a52a854f28f80f2942a', 0)]}},
#     '117692278fa0a46b1cee3d39b41f8ec8f8c2e65318e64f07d275002268d6ec84': {'nounce': 0, 'previousBlock': 0, 'transaction': {'output': [(<person.person instance at 0x10b6cc488>, 25)], 'transActionNumber': '117692278fa0a46b1cee3d39b41f8ec8f8c2e65318e64f07d275002268d6ec84', 'signatures': {'Alice': ',\xc2\x8b\xa01\x90\x08\x1f>\x83\xeb\x95-\xef\x8a\x91\xde\xac\xa5b\xc7u\xf0\x00a%\xa9qr\x19\xaa#d\x96\xfaaG\xc0X\xe9\x1bDc\xb0J\xaa\xcf\xd4'}, 'type': 'generate', 'input': [None]}},
#     'cad27f8b2d5504ae65f18b595523b9c44708ed6e9ce0740d3434b8487da59274': {'nounce': 4399116236312888907, 'previousBlock': '117692278fa0a46b1cee3d39b41f8ec8f8c2e65318e64f07d275002268d6ec84', 'transaction': {'output': [(<person.person instance at 0x10b6cc488>, 25)], 'transActionNumber': 'cad27f8b2d5504ae65f18b595523b9c44708ed6e9ce0740d3434b8487da59274', 'signatures': {'Alice': 'G5&#\x0c\xfcqFtu$d\xe8\xd6\xc20\xaeb\xb4\xa9\xea)\x98\x91\x82,\xd7\x9d\xd9\xe6\xa0\x7fy~\xdb\xf4%\x97\x02\t\xf4\x81\x1c\xc1\xb6\xbf\xce\x8d'}, 'type': 'generate', 'input': [('db38787f7508a45fcfa87153ee454a55e1b31115e4e891e427eb9bce50605da2', 0)]}}}
