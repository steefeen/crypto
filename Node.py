import threading
import time
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

        print threading.currentThread().getName(), self.receive_messages

        val = self.queue.get()
        for t in val:
            if t != self:
                self.allThreads.append(t)

        print('[%s]' % ', '.join(map(str, self.allThreads)))

        while True:
            time.sleep(2)
            val = self.queue.get()
            self.do_thing_with_message(val)

    def do_thing_with_message(self, message):
        if self.receive_messages:
            self.unverifiedTransacton.append(message)
            print threading.currentThread().getName(), "Received {}".format(message)
            print threading.currentThread().getName(), ('[%s]' % ', '.join(map(str, self.unverifiedTransacton)))


