import threading
import hashlib
import time
import json
from random import randint

class Node(threading.Thread):

    def __init__(self, queue, args=()):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue = queue
        self.daemon = True
        self.receive_messages = args[0]
        self.unverifiedTransacton = []
        self.allThreads = []




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
        if(len(self.unverifiedTransacton)>0):
            number = randint(0, len(self.unverifiedTransacton)-1)
            return self.unverifiedTransacton[number]
        return None

    def checkForNewMessages(self):

        while not self.queue.empty():
            val = self.queue.get()
            if(val != None):
                self.do_thing_with_message(val)



    def findHash(self):
        i = randint(0, 9999999)
        #print(i)
        hashOfI = hashlib.sha256(str(self.transactionToWork)+ str(i))
        print(str(self.transactionToWork))
        #print("tried: " + str(i) + "found: " + hashOfI.hexdigest())
        if(hashOfI.hexdigest()[0:4] == "0000"):
            print("tried: " + str(i) + "found: " + hashOfI.hexdigest())
            print("successful!")

