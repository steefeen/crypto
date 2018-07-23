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

    def gotNewTransaction(self, message):
        if self.receive_messages:
            message = message.get("message")
            self.unverifiedTransacton.append(message)
            print("unverified: ", threading.currentThread().getName(), ('[%s]' % ', '.join(map(str, self.unverifiedTransacton))))

    def gotNewBlock(self, newBlock):
        print ("newBlock")
        return True

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
                self.gotNewTransaction(val)
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
                messageTyp = val.get("messageType")
                if(messageTyp == "newTransaction"):
                    self.gotNewTransaction(val)
                elif(messageTyp == "newBlock"):
                    self.gotNewBlock(val)


    def findHash(self):
        i = randint(0, sys.maxint)

        hashOfI = hashlib.sha256(str(self.transactionToWork) + str(i))
        #print(hashOfI.hexdigest())
        if(hashOfI.hexdigest()[0:4] == "0000"):
            print("tried: " + str(i) + "   found: " + hashOfI.hexdigest())

            self.foundHash(i)

    def foundHash(self, nonce):
        generatedBlock = generateBlock(self.transactionToWork, nonce)
        self.lastBlock = self.transactionToWork.get("transAction")
        self.blockChain.append(generatedBlock)

        self.distributeNewBlock(generatedBlock)
        print("blockchain:" + str(self.blockChain))
        self.unverifiedTransacton.pop(0)
        self.transactionToWorkIsVerifiyed = False

    def verifyTransaction(self):
        if not self.transactionToWorkIsVerifiyed:
            transactionIsRight = self.verifyTransactionSignature() and self.verifyTransationMoney() and self.verifyNoDoubleSpending()
            self.transactionToWorkIsVerifiyed = transactionIsRight
            if not transactionIsRight:
                self.unverifiedTransacton.pop(0)
                print(self.unverifiedTransacton)
            return transactionIsRight
        return True

    def verifyTransactionSignature(self):
        transaction = self.unverifiedTransacton[0]
        for out in transaction.get("output"):
            name = out[0].getName()
            signature = transaction.get("signatures")[name]
            message = transaction.get("HashOfTransaction")
            try:
                out[0].verify(signature, message)
            except BadSignatureError:
                return False
        return True

    def verifyTransationMoney(self):
        print( "to Verify: " + str(self.unverifiedTransacton[0]))
        #print(self.transactionToWork)
        previousInputs = self.unverifiedTransacton[0].get("input")
        outputs = self.unverifiedTransacton[0].get("output")
        sumOfOutputs = sum([element[1] for element in outputs])  # adds all the money in the outputs together

        # sum of values of specified output in specified block
        sumOfInPuts = sum([self.blockChain[element[0]].get("transaction").get("output")[element[1]][1] for element in previousInputs])
        print(sumOfInPuts, sumOfOutputs)

        return sumOfInPuts == sumOfOutputs

    def distributeNewBlock(self, newBlock):
        for t in self.allThreads:
            t.queue.put({"messageType": "newBlock", "message": newBlock})
    def verifyNoDoubleSpending(self):
        inputsToVerify = self.unverifiedTransacton[0].get("input")
        # check if input was already used in blockchain
        for inputToVerify in inputsToVerify:
            for block in self.blockChain:
                for previousInput in block.get("transaction").get("input"):
                    if previousInput == inputToVerify:
                        return False
        # check if same input is used twice
        return len(inputsToVerify) == len(set(inputsToVerify))


