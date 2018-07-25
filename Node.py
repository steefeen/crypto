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
            if len(self.unverifiedTransacton) > 0:
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
            raise Exception("Maxi was laberst du?")
        self.lastBlock = self.transactionToWork.get("transAction")
        self.blockChain.append(generatedBlock)
        self.distributeNewBlock(generatedBlock)
        self.log("blockchain:" + str(self.blockChain))
        self.unverifiedTransacton.pop(0)
        self.transactionToWorkIsVerifiyed = False
        self.printBalances()

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
        if transaction.get("input") == None:
            return False
        for i in range(len(transaction.get("input"))):
            input = transaction.get("input")[i]
            if input[0] > len(self.blockChain) - 1:
                return False
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

    def printBalances(self):
        print("maxiiiiiiiiiiiiiiiiix")

#     blockchain:[
#    {
#       'nounce':0,
#       'transaction':{
#          'output':[
#             (< person.person instance at 0x10cf38200 >,
#             25            )
#          ],
#          'signatures':[
#
#          ],
#          'HashOfTransaction':'8198b72539a0e13e3ba3867c02f8bf85d578f0df691d02300019ea63fc024022',
#          'input':[
#             None
#          ]
#       }
#    },
#    {
#       'nounce':3868783673210654595,
#       'transaction':{
#          'output':[
#             (< person.person instance at 0x10cf38200 >,
#             5            ),
#             (< person.person instance at 0x10cf508c0 >,
#             20            )
#          ],
#          'signatures':[
#             "\xb9/=\x05\x90w+\x90t\x04O\xda\xe4\xee\xb7\xb1\xd1\xf6\x85V\xf6r\xb3\x10\xe2\xf4rC\xbaj\x04\x10\xe7\x8e.:\xc7'\xfd\xad\x8a\x85]\x9d \xbeF\xb9"
#          ],
#          'HashOfTransaction':'49aaa4ff230deff6973a420efafc4506136410831876416f5e0866b8e6e19c71',
#          'input':[
#             (0,
#             0            )
#          ]
#       }
#    },
#    {
#       'nounce':80197979391901477,
#       'transaction':{
#          'output':[
#             (< person.person instance at 0x10cf38200 >,
#             5            )
#          ],
#          'signatures':[
#             '\xb4\xdftK\xf5k\xca\x80\xc3S\x0b\xc76\x88H\x9e\xae\x8cm\x92\x04ol\xed\xd0\x8f\xb7\x1dn\xd5\x89\x14\xb5\\\x9dq\x9f\xea\xb7\t\xbak\xc0\xa1\xce\x0e\x89\x0c'
#          ],
#          'HashOfTransaction':'d2f6a923c0a27265aec168329d76468b0eb97918eb6217903be138069a4f6e27',
#          'input':[
#             (1,
#             0            )
#          ]
#       }
#    },
#    {
#       'nounce':2150418254134293154,
#       'transaction':{
#          'output':[
#             (< person.person instance at 0x10cf50a28 >,
#             5            )
#          ],
#          'signatures':[
#             '\xab\xc6\xc4M\xb2\xf8\x05\x87\xd8}6\x06\xc1.\xe1\x10\xaa\x13\xf9+\xdcVR1\xa6\xed\xad\xbdV\xbf\xdfS\xd8\x1b\x8a]y7\xb1\xddO\xea\xedX\x12r\xb0|'
#          ],
#          'HashOfTransaction':'1affcc088d1551eb0bdc7f7c763751610fda567a633d234ae4a0c0b553eed49e',
#          'input':[
#             (2,
#             0            )
#          ]
#       }
#    },
#    {
#       'nounce':8148766975993033673,
#       'transaction':{
#          'output':[
#             (< person.person instance at 0x10cf38200 >,
#             5            )
#          ],
#          'signatures':[
#             '^\x85\xd4\xf8Q\xafR\xa7\xdd\x1d\x9c\x9aR8\xcbr\x92\xea\xd2\x01e\xe4\xda\xfd\x8d\xa5\x86\x15\xd7@tVP\xe0\x8d8-KH\xcc\x83_P\x85\x18\xe8\xb6\x06'
#          ],
#          'HashOfTransaction':'b2576179a7cdb2982ff54ab28ee2bdd3a1f154dfbdd96326f231dea0296f34c6',
#          'input':[
#             (3,
#             0            )
#          ]
#       }
#    }
# ]
