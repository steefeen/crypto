import time
import hashlib


class transaction:
    inputs = []
    outputs = []
    timestamp = 0
    nonce = 3
    hash = 0

    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.timestamp = time.time()
        self.hash = hashlib.sha512(str(''.join(str(x.transacion + str(x.position)) for x in self.inputs) + ''.join(
            str(str(x.reciver) + str(x.value)) for x in self.outputs) + str(self.timestamp) + str(self.nonce))).hexdigest()
