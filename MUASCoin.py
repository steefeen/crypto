import hashlib
from person import person

#every node has a name and a secret key for signing



def generateTransaction(fromWho, toWho, type):
    #fromWho: list of Names
    #toWho: dictionary of Name/Value pairs
    signatures = {}#[nodes[x].sign("message") for x in fromWho] #ToDo: has to sign transaction from before
    transActionNumber = makeHash(fromWho, toWho)
    for p in toWho:
            signatures[p[0].getName()] = p[0].sign(transActionNumber)
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
