import sys
import threading
import hashlib
import time
from random import randint
from ecdsa import BadSignatureError
from MUASCoin import generateBlock
from threading import Lock


class Node(threading.Thread):
    printLock = Lock()
    def __init__(self, queue, blockChain, difficulty, startTransaction):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.difficulty = difficulty
        self.startTransactions = startTransaction
        self.unverifiedTransacton = []
        self.allThreads = []
        self.blockChain = blockChain
        self.transactionToWorkIsVerifiyed = False
        self.logAll("first blockchain:", str(self.blockChain))
        self.printBalances()

    def run(self):

        self.reciveThreads()
        self.waitForFirstMessage()
        self.work()

    def gotNewTransaction(self, message):
        message = message.get("message")
        self.unverifiedTransacton.append(message)
        self.logAll("new unverified transaction: ", ('[%s]' % ', '.join(map(str, self.unverifiedTransacton))))

    def gotNewBlock(self, newBlock):
        block = newBlock.get("message")

        if self.verifyNewBlock(block):
            self.blockChain.append(block)
            if len(self.unverifiedTransacton) > 0:
                self.removeTransaction()
            self.logAll("block confirmed", str(block))
        else:
            self.logAll("block denied ", str(block))

    def reciveThreads(self):
        val = self.queue.get()
        for t in val:
            if t != self:
                self.allThreads.append(t)

        self.logAll("all other threads", str(self.allThreads))

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
            if self.verifyTransaction(self.unverifiedTransacton[0], False):
                return self.unverifiedTransacton[0]
            else:
                return None
        else:
            self.logAll("no more transactions", "")
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
            self.logAll("new hash", "tried: " + str(i) + "   found: " + hashOfI.hexdigest())

            self.foundHash(i)

    def foundHash(self, nonce):
        generatedBlock = generateBlock(self.transactionToWork, nonce)
        if not self.queue.empty():
            raise Exception("Maxi was laberst du?")
        self.lastBlock = self.transactionToWork.get("transaction")
        self.blockChain.append(generatedBlock)
        self.distributeNewBlock(generatedBlock)
        self.logAll("blockchain updated:", str(self.blockChain))
        self.removeTransaction()
        self.printBalances()

    def verifyTransaction(self, unverifiedTransaction, isBlock):

        if (not self.transactionToWorkIsVerifiyed) or isBlock:
            transactionSignatureIsRight = self.verifyTransactionSignature(unverifiedTransaction)
            transactionMoneyIsRight = self.verifyTransationMoney(unverifiedTransaction)
            transactionNoDoubleSpending = self.verifyNoDoubleSpending(unverifiedTransaction)
            transactionIsRight = transactionSignatureIsRight and transactionMoneyIsRight and transactionNoDoubleSpending
            self.transactionToWorkIsVerifiyed = transactionIsRight

            if not transactionIsRight:
                if len(self.unverifiedTransacton) > 0:
                    self.removeTransaction()
            return transactionIsRight
        return True

    def verifyTransactionSignature(self, unverifiedTransaction):
        transaction = unverifiedTransaction
        if transaction.get("input") == None:
            return False
        for i in range(len(transaction.get("input"))):
            input = transaction.get("input")[i]
            if input[0] > len(self.blockChain) - 1:
                self.logAll("transaction not confirmed   wrong siganture ", str(transaction))
                return False
            previousBlock = self.blockChain[input[0]]
            previousOwner = previousBlock.get("transaction").get("output")[input[1]][0]
            signature = transaction.get("signatures")[i]
            message = transaction.get("HashOfTransaction")
            try:
                previousOwner.verify(signature, message)
            except BadSignatureError:
                self.logAll("transaction not confirmed   wrong siganture ", str(transaction))
                return False
        return True

    def verifyTransationMoney(self, unverifiedTransaction):
        self.logAll("transaction to Verify: ", str(unverifiedTransaction))
        #self.log(self.transactionToWork)
        previousInputs = unverifiedTransaction.get("input")
        outputs = unverifiedTransaction.get("output")
        sumOfOutputs = sum([element[1] for element in outputs])  # adds all the money in the outputs together

        # sum of values of specified output in specified block
        try:
            sumOfInPuts = sum([self.blockChain[element[0]].get("transaction").get("output")[element[1]][1] for element in previousInputs])
        except IndexError:
            self.logAll("transaction not confirmed   wrong money1 ", str(unverifiedTransaction))
            return False

        if sumOfInPuts == sumOfOutputs:
            self.logAll("transaction not confirmed   wrong money2 ", str(unverifiedTransaction))

        return sumOfInPuts == sumOfOutputs

    def verifyNoDoubleSpending(self, unverifiedTransaction):
        inputsToVerify = unverifiedTransaction.get("input")
        # check if input was already used in blockchain
        for inputToVerify in inputsToVerify:
            for block in self.blockChain:
                for previousInput in block.get("transaction").get("input"):
                    if previousInput == inputToVerify:
                        self.logAll("transaction not confirmed   double spending1 ", str(unverifiedTransaction))
                        return False
        # check if same input is used twice
        lenIsEqually = len(inputsToVerify) == len(set(inputsToVerify))
        if not lenIsEqually:
            self.logAll("transaction not confirmed   double spending2 ", str(unverifiedTransaction))
        return lenIsEqually

    def distributeNewBlock(self, newBlock):
        for t in self.allThreads:
            t.queue.put({"messageType": "newBlock", "message": newBlock})

    def verifyNewBlock(self, block):
        nounce = block.get("nounce")
        transaction = block.get("transaction")
        hash = hashlib.sha256(str(transaction) + str(nounce)).hexdigest()
        difficultyString = "0"
        index = 0
        while index < self.difficulty:
            difficultyString += "0"
            index += 1
        isTransactionVerified = self.verifyTransaction(transaction, True)
        return hash[0 : self.difficulty + 1] == difficultyString and isTransactionVerified

    def logAll(self, messageType, message):
        logging = False
        all = False
        with self.printLock:
            if logging:
                if all:
                    print(threading.currentThread().getName() + "  " + messageType + "   " + message)
                else:
                    print(threading.currentThread().getName() + "  " + messageType)

    def log(self, message):
        self.logAll(message, "")

    def getBlockchain(self):
        return self.blockChain

    def removeTransaction(self):
        self.unverifiedTransacton.pop(0)
        self.transactionToWorkIsVerifiyed = False

    def printBalances(self):
        balances = {}
        for block in self.blockChain:
            for output in block.get("transaction").get("output"):
                if output[0].getName() in balances:
                    balances[output[0].getName()] += output[1]
                else:
                    balances[output[0].getName()] = output[1]
        for block in self.blockChain:
            for input in block.get("transaction").get("input"):
                if input != None:
                    previousBlock = self.blockChain[input[0]]
                    previousOutputs = previousBlock.get("transaction").get("output")
                    balances[previousOutputs[input[1]][0].getName()] -= previousOutputs[input[1]][1]
        with self.printLock:
            print(threading.currentThread().getName() + "  " + str(balances))


