import hashlib

import ecdsa

#every node has a name and a secret key for signing
persons = ["Alice", "Bob", "Carol", "Doris", "Eve"]
nodes = {}

for element in persons:
    nodes.update({element: ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)})

transactions = []

def generateTransaction(fromWho, toWho, transActionNumber, type):
    #fromWho: list of Names
    #toWho: dictionary of Name/Value pairs
    signatures = None#[nodes[x].sign("message") for x in fromWho] #ToDo: has to sign transaction from before
    transActionNumber = makeHash(fromWho, toWho)
    return {"transActionNumber": transActionNumber,
            "type": type,
            "signatures": signatures,
            "output": toWho,
            "input": fromWho}

def makeHash(input, output):
    inputString = ""
    outputString = ""
    if input[0] != None:
        inputString = str(input)
    if output[0] != None:
        outputString = str(output)
    return hashlib.sha256(inputString + outputString).hexdigest()

def generateBlock(transaction, nounce, previousBlock):

    block = {
        "previousBlock": previousBlock,
        "nounce": nounce,
        "transaction": transaction
    }
    return block
