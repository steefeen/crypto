import sys
import threading
import hashlib
import time
from random import randint
from ecdsa import BadSignatureError
from MUASCoin import generateBlock


class Node(threading.Thread):

    def __init__(self, queue, blockChain, difficulty, args=()):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True
        self.difficulty = difficulty
        self.receive_messages = args[0]
        self.startTransactions = args[1]
        self.unverifiedTransacton = []
        self.allThreads = []
        self.blockChain = blockChain
        self.transactionToWorkIsVerifiyed = False
        self.log("blockchain:" + str(self.blockChain))

    def run(self):

        self.log(threading.currentThread().getName() + "  " +  str(self.receive_messages))

        self.reciveThreads()

        self.waitForFirstMessage()

        self.work()

    def gotNewTransaction(self, message):
        if self.receive_messages:
            message = message.get("message")
            self.unverifiedTransacton.append(message)
            self.log("unverified: " + threading.currentThread().getName() + ('[%s]' % ', '.join(map(str, self.unverifiedTransacton))))

    def gotNewBlock(self, newBlock):
        block = newBlock.get("message")

        if self.verifyNewBlock(block):
            self.blockChain.append(block)
            self.unverifiedTransacton.pop(0)
            self.log("block confirmed")

    def reciveThreads(self):
        val = self.queue.get()
        for t in val:
            if t != self:
                self.allThreads.append(t)

        self.log('[%s]' % ', '.join(map(str, self.allThreads)))

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
            if self.verifyTransaction(self.unverifiedTransacton[0]):
                return self.unverifiedTransacton[0]
            else:
                return None
        else:
            self.log(threading.currentThread().getName() + "  no more transactions")
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
        #self.log(hashOfI.hexdigest())
        difficultyString = "0"
        index = 0
        while index < self.difficulty:
            difficultyString += "0"
            index += 1
        if hashOfI.hexdigest()[0 : self.difficulty + 1] == difficultyString:
            self.log("tried: " + str(i) + "   found: " + hashOfI.hexdigest())

            self.foundHash(i)

    def foundHash(self, nonce):
        generatedBlock = generateBlock(self.transactionToWork, nonce)
        if not self.queue.empty():
            raise Exception("Maxi was laberst du")
        self.lastBlock = self.transactionToWork.get("transAction")
        self.blockChain.append(generatedBlock)
        self.distributeNewBlock(generatedBlock)
        self.log("blockchain:" + str(self.blockChain))
        self.unverifiedTransacton.pop(0)
        self.transactionToWorkIsVerifiyed = False

    def verifyTransaction(self, unverifiedTransaction):
        if not self.transactionToWorkIsVerifiyed:
            transactionIsRight = self.verifyTransactionSignature(unverifiedTransaction) and self.verifyTransationMoney(unverifiedTransaction) and self.verifyNoDoubleSpending(unverifiedTransaction)
            self.transactionToWorkIsVerifiyed = transactionIsRight
            if not transactionIsRight:
                if len(self.unverifiedTransacton) > 0:
                    self.unverifiedTransacton.pop(0)
                self.log("unverified transactions:  " + str(self.unverifiedTransacton))
            return transactionIsRight
        return True

    def verifyTransactionSignature(self, unverifiedTransaction):
        transaction = unverifiedTransaction
        for i in range(len(transaction.get("input"))):
            input = transaction.get("input")[i]
            previousBlock = self.blockChain[input[0]]
            previousOwner = previousBlock.get("transaction").get("output")[input[1]][0]
            signature = transaction.get("signatures")[i]
            message = transaction.get("HashOfTransaction")
            try:
                previousOwner.verify(signature, message)
            except BadSignatureError:
                return False
        return True

    def verifyTransationMoney(self, unverifiedTransaction):
        self.log( "to Verify: " + str(unverifiedTransaction))
        #self.log(self.transactionToWork)
        previousInputs = unverifiedTransaction.get("input")
        outputs = unverifiedTransaction.get("output")
        sumOfOutputs = sum([element[1] for element in outputs])  # adds all the money in the outputs together

        # sum of values of specified output in specified block
        try:
            sumOfInPuts = sum([self.blockChain[element[0]].get("transaction").get("output")[element[1]][1] for element in previousInputs])
        except IndexError:
            return False
        self.log(str(sumOfInPuts) + "  " + str(sumOfOutputs))

        return sumOfInPuts == sumOfOutputs

    def distributeNewBlock(self, newBlock):
        for t in self.allThreads:
            t.queue.put({"messageType": "newBlock", "message": newBlock})

    def verifyNoDoubleSpending(self, unverifiedTransaction):
        inputsToVerify = unverifiedTransaction.get("input")
        # check if input was already used in blockchain
        for inputToVerify in inputsToVerify:
            for block in self.blockChain:
                for previousInput in block.get("transaction").get("input"):
                    if previousInput == inputToVerify:
                        return False
        # check if same input is used twice
        return len(inputsToVerify) == len(set(inputsToVerify))

    def verifyNewBlock(self, block):
        nounce = block.get("nounce")
        transaction = block.get("transaction")
        hash = hashlib.sha256(str(transaction) + str(nounce)).hexdigest()
        difficultyString = "0"
        index = 0
        while index < self.difficulty:
            difficultyString += "0"
            index += 1
        return hash[0 : self.difficulty + 1] == difficultyString and self.verifyTransaction(transaction)

    def log(self, message):
        lock = True
        if lock:
            print(message)

    def getBlockchain(self):
        return self.blockChain